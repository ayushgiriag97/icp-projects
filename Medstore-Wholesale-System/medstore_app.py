# =============================================
#   CLASS 4: MedStoreApp (Main Application)
# =============================================

import os
import re
import difflib
import datetime

from medicine import Medicine
from file_manager import FileManager, FileManagerError
from invoice_generator import InvoiceGenerator, InvoiceError

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(SCRIPT_FOLDER, "medicines.txt")

LOW_STOCK_THRESHOLD = 50
RESTOCK_BULK_THRESHOLD = 1000
EXPIRY_WARNING_DAYS = 30
NAME_PATTERN = re.compile(r"^[A-Za-z\s]+$")

SORT_KEYS = {
    ("rate", "asc"): lambda m: m.rate_tablet,
    ("rate", "desc"): lambda m: -m.rate_tablet,
    ("stock", "asc"): lambda m: m.qty,
    ("stock", "desc"): lambda m: -m.qty,
}
SORT_ALIASES = {
    "rate asc": ("rate", "asc"), "rate low": ("rate", "asc"), "rate min": ("rate", "asc"),
    "rate desc": ("rate", "desc"), "rate high": ("rate", "desc"), "rate max": ("rate", "desc"),
    "stock asc": ("stock", "asc"), "stock low": ("stock", "asc"), "stock min": ("stock", "asc"),
    "stock desc": ("stock", "desc"), "stock high": ("stock", "desc"), "stock max": ("stock", "desc"),
}


class MedStoreApp:
    def __init__(self):
        self.file_mgr = FileManager(INVENTORY_FILE)
        self.invoice_gen = InvoiceGenerator()
        self.medicines = []

    # ---------- generic input helpers ----------
    def get_int(self, prompt, min_value=None):
        while True:
            value = input(prompt).strip()
            if not value.lstrip("-").isdigit():
                print("  [Error] Please enter a whole number.")
                continue
            num = int(value)
            if min_value is not None and num < min_value:
                print(f"  [Error] Value must be at least {min_value}.")
                continue
            return num

    def get_float(self, prompt, min_value=0.0):
        while True:
            value = input(prompt).strip()
            try:
                num = float(value)
            except ValueError:
                print("  [Error] Please enter a valid number.")
                continue
            if num < min_value:
                print(f"  [Error] Value cannot be less than {min_value}.")
                continue
            return num

    def get_name(self, prompt):
        """Prompt for a letters/spaces-only, non-empty name (customer/supplier)."""
        while True:
            value = input(prompt).strip()
            if value and NAME_PATTERN.match(value):
                return value
            print("  [Error] Name must contain only letters and spaces, and cannot be empty.")

    def get_nonempty(self, prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("  [Error] This field cannot be empty.")

    def get_date(self, prompt):
        while True:
            value = input(prompt).strip()
            try:
                return Medicine.validate_date(value, "Date")
            except ValueError as e:
                print(f"  [Error] {e}")

    def get_yes_no(self, prompt):
        while True:
            value = input(prompt).strip().lower()
            if value in ("y", "yes"):
                return True
            if value in ("n", "no"):
                return False
            print("  [Error] Please enter y or n.")

    # ---------- display ----------
    def show_inventory(self, medicines):
        print("\n--------------------------------------------------------------------------------")
        print(" No.  Medicine           Brand        Stock   Tab-Rate  Strip-Rate  Batch     Expiry      Rx")
        print("--------------------------------------------------------------------------------")
        if not medicines:
            print(" (inventory is empty)")
        for i, m in enumerate(medicines, start=1):
            print(f"{i:>3}.  {m}")
        print("--------------------------------------------------------------------------------")

    def _print_low_stock_alerts(self, threshold=LOW_STOCK_THRESHOLD):
        low_stock = [m for m in self.medicines if m.qty <= threshold]
        if low_stock:
            print("\n[Low Stock Alerts]")
            for m in low_stock:
                print(f" - {m.name} ({m.brand}) has only {m.qty} tablets left. Consider restocking.")
        else:
            print("\n[Low Stock Alerts] None at the moment.")

    def _print_expiry_alerts(self, warning_days=EXPIRY_WARNING_DAYS):
        expired = [m for m in self.medicines if m.is_expired()]
        expiring = [m for m in self.medicines if 0 <= m.days_until_expiry() <= warning_days]
        if expired:
            print("\n[Expired Stock — remove from shelf]")
            for m in expired:
                print(f" - {m.name} ({m.brand}), Batch {m.batch_no}, expired on {m.expiry_date}")
        if expiring:
            print(f"\n[Expiring within {warning_days} days]")
            for m in expiring:
                print(f" - {m.name} ({m.brand}), Batch {m.batch_no}, expires on {m.expiry_date}")

    # ---------- discount rules ----------
    @staticmethod
    def _sell_discount(unit, qty, subtotal, tabs_count):
        if unit == "T":
            if 50 <= qty < 100:
                return round(subtotal * 0.02, 2)
            if qty >= 100:
                return round(subtotal * 0.05, 2)
        else:  # strips
            if 2 <= qty < 5:
                return round(subtotal * 0.05, 2)
            if qty >= 5:
                return round(subtotal * 0.10, 2)
        return 0.0

    @staticmethod
    def _restock_discount(unit, qty, subtotal, tabs_count):
        if tabs_count >= RESTOCK_BULK_THRESHOLD:
            return round(subtotal * 0.10, 2)
        return 0.0

    @staticmethod
    def _reverse_cart_entry(entry, is_sell):
        """Undo a cart line's effect on live stock (does NOT touch the transaction log,
        since transactions are only recorded once the cart is finalized)."""
        sign = 1 if is_sell else -1
        entry["medicine"].qty += sign * entry["tabs_count"]

    # ---------- shared sell/restock flow ----------
    def _transact(self, mode):
        """
        Shared interactive loop for selling and restocking medicines.
        mode must be "sell" or "restock".
        """
        is_sell = mode == "sell"
        title = "SELL MEDICINE" if is_sell else "RESTOCK MEDICINE"
        party_label = "Customer" if is_sell else "Supplier"
        discount_fn = self._sell_discount if is_sell else self._restock_discount
        txn_type = "SALE" if is_sell else "RESTOCK"

        try:
            if not self.medicines:
                print("[Error] Inventory is empty. Please add medicines first.")
                return

            print(f"\n===== {title} =====")
            party = self.get_name(f"{party_label} name: ")

            total = 0.0
            total_discount = 0.0
            cart_entries = []  # structured, so a line item can be undone before finalizing

            while True:
                self.show_inventory(self.medicines)
                if not is_sell:
                    self._print_low_stock_alerts()
                self._print_expiry_alerts()

                exit_number = len(self.medicines) + 1
                print(f"{exit_number}. Exit {title.title()}")
                print("Type 'undo' to remove the last cart item, or 'remove N' to remove cart item N.")

                choice = input("Enter medicine number (or 'exit'/'undo'/'remove N'): ").strip().lower()

                if choice in ("exit", str(exit_number)):
                    break

                if choice == "undo":
                    if not cart_entries:
                        print("Nothing to undo.")
                        continue
                    entry = cart_entries.pop()
                    self._reverse_cart_entry(entry, is_sell)
                    total -= entry["subtotal"]
                    total_discount -= entry["discount"]
                    print(f"Removed last item: {entry['text']}")
                    continue

                if choice.startswith("remove "):
                    idx_str = choice.split(" ", 1)[1].strip()
                    if not idx_str.isdigit() or not (1 <= int(idx_str) <= len(cart_entries)):
                        print("Invalid cart item number to remove.")
                        continue
                    entry = cart_entries.pop(int(idx_str) - 1)
                    self._reverse_cart_entry(entry, is_sell)
                    total -= entry["subtotal"]
                    total_discount -= entry["discount"]
                    print(f"Removed item: {entry['text']}")
                    continue

                if not choice.isdigit() or not (1 <= int(choice) <= len(self.medicines)):
                    print("Invalid choice. Try again.")
                    continue

                m = self.medicines[int(choice) - 1]

                if is_sell and m.is_expired():
                    print(f"[Error] '{m.name}' (Batch {m.batch_no}) expired on {m.expiry_date}. Cannot sell.")
                    continue

                if is_sell and 0 <= m.days_until_expiry() <= EXPIRY_WARNING_DAYS:
                    print(f"[Warning] '{m.name}' (Batch {m.batch_no}) expires on {m.expiry_date}.")

                unit = input(f"{'Sell' if is_sell else 'Restock'} by (T)ablet or (S)trip? ").strip().upper()
                if unit not in ("T", "S"):
                    print("Invalid unit. Enter T or S only.")
                    continue

                qty = self.get_int("Quantity: ", min_value=1)

                rate = m.rate_tablet if unit == "T" else m.rate_strip
                tabs_count = qty if unit == "T" else qty * m.tabs_per_strip
                unit_name = "Tablet(s)" if unit == "T" else "Strip(s)"

                if is_sell and tabs_count > m.qty:
                    print(f"Only {m.qty} tablets left. Try again.")
                    continue

                rx_ref = ""
                if is_sell and m.prescription_required:
                    rx_ref = self.get_nonempty(
                        "This medicine requires a prescription. Enter Rx reference: "
                    )

                subtotal = rate * qty
                discount = discount_fn(unit, qty, subtotal, tabs_count)
                subtotal -= discount

                m.qty += tabs_count if not is_sell else -tabs_count
                total += subtotal
                total_discount += discount

                line = (f"{m.name} | {unit_name} x{qty} | Rate: Rs.{rate} | "
                        f"Discount: Rs.{discount} | Subtotal: Rs.{round(subtotal, 2)}")
                if rx_ref:
                    line += f" | Rx Ref: {rx_ref}"

                cart_entries.append({
                    "medicine": m, "unit": unit, "qty": qty, "tabs_count": tabs_count,
                    "rate": rate, "discount": discount, "subtotal": subtotal,
                    "rx_ref": rx_ref, "text": line,
                })

                print(f"{'Added to cart' if is_sell else 'Restocked'}:", line)

                print(f"\n{'Your Medicine Cart' if is_sell else 'Restock Summary'}:")
                for i, entry in enumerate(cart_entries, start=1):
                    print(f" {i}. {entry['text']}")
                print(f"Total so far: Rs.{round(total, 2)}")
                print(f"Discount so far: Rs.{round(total_discount, 2)}\n")

            if not cart_entries:
                print(f"No items {'sold' if is_sell else 'restocked'}.")
                return

            lines = [entry["text"] for entry in cart_entries]

            if is_sell:
                content = self.invoice_gen.make_sale_invoice(party, lines, total)
                filename = self.invoice_gen.unique_name("invoice", party)
                doc_label = "Invoice"
            else:
                content = self.invoice_gen.make_restock_note(party, lines, total)
                filename = self.invoice_gen.unique_name("restock", party)
                doc_label = "Restock note"

            self.file_mgr.write_file(filename, content)
            self.file_mgr.save_inventory(self.medicines)

            # Only log transactions that survived to the finalized cart (undone
            # items were never recorded, so reports stay accurate).
            for entry in cart_entries:
                self.invoice_gen.record_transaction(
                    txn_type, party, entry["medicine"], entry["unit"], entry["qty"],
                    entry["tabs_count"], entry["rate"], entry["discount"],
                    entry["subtotal"], entry["rx_ref"],
                )

            print(f"{doc_label} saved as:", filename)
            print("Final Total: Rs.", round(total, 2))
            print("Total Discount Applied: Rs.", round(total_discount, 2))

        except (FileManagerError, InvoiceError) as e:
            print(f"[Error] {'Sell' if is_sell else 'Restock'} process failed: {e}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n[Info] {'Sell' if is_sell else 'Restock'} cancelled.")

    def sell(self):
        self._transact("sell")

    def restock(self):
        self._transact("restock")

    # ---------- search ----------
    def search(self):
        try:
            if not self.medicines:
                print("[Error] Inventory is empty. Please add medicines first.")
                return

            keyword = input("Enter search (name/brand, 'stock>N', 'rate<N', or a sort key): ").strip().lower()
            if not keyword:
                print("[Error] Search keyword cannot be empty.")
                return

            is_filter = any(op in keyword for op in ("<", ">"))
            is_sort = keyword in SORT_ALIASES
            if len(keyword) < 2 and not (is_filter or is_sort):
                print("[Error] Please enter at least 2 characters for search.")
                return

            if is_sort:
                field, direction = SORT_ALIASES[keyword]
                found = sorted(self.medicines, key=SORT_KEYS[(field, direction)])
                self._print_search_results(found, keyword, highlight=False)
                return

            stock_match = re.match(r"stock\s*([<>]=?)\s*(\d+)", keyword)
            rate_match = re.match(r"rate\s*([<>]=?)\s*(\d+(?:\.\d+)?)", keyword)

            if stock_match:
                found = self._apply_numeric_filter(self.medicines, "qty", *stock_match.groups(), cast=int)
            elif rate_match:
                found = self._apply_numeric_filter(self.medicines, "rate_tablet", *rate_match.groups(), cast=float)
            else:
                found = [m for m in self.medicines
                         if keyword in m.name.lower() or keyword in m.brand.lower()]
                if not found:
                    names_and_brands = [m.name for m in self.medicines] + [m.brand for m in self.medicines]
                    close_matches = difflib.get_close_matches(keyword, names_and_brands, cutoff=0.6)
                    if close_matches:
                        found = [m for m in self.medicines if m.name in close_matches or m.brand in close_matches]

            self._print_search_results(found, keyword, highlight=not (stock_match or rate_match))

        except Exception as e:
            print(f"[Error] Search failed: {e}")

    @staticmethod
    def _apply_numeric_filter(medicines, attr, op, val, cast):
        val = cast(val)
        ops = {
            "<": lambda x: x < val,
            "<=": lambda x: x <= val,
            ">": lambda x: x > val,
            ">=": lambda x: x >= val,
        }
        test = ops.get(op)
        if test is None:
            return []
        return [m for m in medicines if test(getattr(m, attr))]

    @staticmethod
    def _highlight(text, keyword):
        idx = text.lower().find(keyword)
        if idx == -1:
            return text
        return text[:idx] + "[" + text[idx:idx + len(keyword)] + "]" + text[idx + len(keyword):]

    def _print_search_results(self, found, keyword, highlight=True):
        if not found:
            print(f"No medicine found matching '{keyword}'.")
            return

        print(f"Found {len(found)} medicine(s) matching '{keyword}':")
        for m in found:
            name, brand = m.name, m.brand
            if highlight:
                if keyword in name.lower():
                    name = self._highlight(name, keyword)
                if keyword in brand.lower():
                    brand = self._highlight(brand, keyword)
            print(f"- {name} | {brand} | Stock: {m.qty} | Rate: Rs.{m.rate_tablet} | Strip Rate: Rs.{m.rate_strip} "
                  f"| Batch: {m.batch_no} | Expiry: {m.expiry_date}")

    # ---------- add ----------
    def add_medicine(self):
        try:
            print("\n===== ADD NEW MEDICINE =====")
            name = input("Medicine name        : ").strip()
            brand = input("Brand name           : ").strip()

            if not name or not brand:
                print("[Error] Name and brand are required.")
                return

            if any(m.name.lower() == name.lower() and m.brand.lower() == brand.lower()
                   for m in self.medicines):
                print(f"[Error] '{name}' ({brand}) already exists. Use Update Medicine instead.")
                return

            qty = self.get_int("Initial stock (tabs)      : ", min_value=0)
            rate_tablet = self.get_float("Rate per tablet (Rs)      : ", min_value=0)
            rate_strip = self.get_float("Rate per strip  (Rs)      : ", min_value=0)
            tabs_per_strip = self.get_int("Tablets per strip         : ", min_value=1)
            batch_no = self.get_nonempty("Batch number              : ")
            expiry_date = self.get_date("Expiry date (YYYY-MM-DD)  : ")
            cost_price = self.get_float("Cost price per tablet (Rs): ", min_value=0)
            prescription_required = self.get_yes_no("Prescription required? (y/n): ")

            new_med = Medicine(name, brand, qty, rate_tablet, rate_strip, tabs_per_strip,
                                batch_no, expiry_date, cost_price, prescription_required)
            self.medicines.append(new_med)
            self.file_mgr.save_inventory(self.medicines)
            print(f"{new_med.name} ({new_med.brand}) added to inventory.")

        except (ValueError, FileManagerError) as e:
            print(f"[Error] Failed to add medicine: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\n[Info] Add medicine cancelled.")

    # ---------- delete ----------
    def delete_medicine(self):
        try:
            if not self.medicines:
                print("[Error] Inventory is empty. Nothing to delete.")
                return

            self.show_inventory(self.medicines)
            choice = input("Enter medicine number to delete (or 'cancel'): ").strip().lower()
            if choice == "cancel":
                print("[Info] Deletion cancelled.")
                return
            if not choice.isdigit() or not (1 <= int(choice) <= len(self.medicines)):
                print("[Error] Invalid medicine number.")
                return

            target = self.medicines[int(choice) - 1]
            confirm = input(f"Are you sure you want to delete '{target.name}' ({target.brand})? (y/n): ").strip().lower()
            if confirm != "y":
                print("[Info] Deletion cancelled.")
                return

            self.medicines = self.file_mgr.delete_medicine(self.medicines, target.name, target.brand)

        except FileManagerError as e:
            print(f"[Error] Delete process failed: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\n[Info] Delete cancelled.")

    # ---------- update ----------
    def update_medicine(self):
        try:
            if not self.medicines:
                print("[Error] Inventory is empty. Nothing to update.")
                return

            self.show_inventory(self.medicines)
            choice = input("Enter medicine number to update (or 'cancel'): ").strip().lower()
            if choice == "cancel":
                print("[Info] Update cancelled.")
                return
            if not choice.isdigit() or not (1 <= int(choice) <= len(self.medicines)):
                print("[Error] Invalid medicine number.")
                return

            target = self.medicines[int(choice) - 1]
            print(f"Updating '{target.name}' ({target.brand}). Leave a field empty to keep its current value.")

            prompts = {
                "qty": f"New quantity [{target.qty}]: ",
                "rate_tablet": f"New tablet rate [{target.rate_tablet}]: ",
                "rate_strip": f"New strip rate [{target.rate_strip}]: ",
                "brand": f"New brand [{target.brand}]: ",
                "tabs_per_strip": f"New tabs per strip [{target.tabs_per_strip}]: ",
                "batch_no": f"New batch number [{target.batch_no}]: ",
                "expiry_date": f"New expiry date YYYY-MM-DD [{target.expiry_date}]: ",
                "cost_price": f"New cost price [{target.cost_price}]: ",
                "prescription_required": f"Prescription required? y/n "
                                          f"[{'y' if target.prescription_required else 'n'}]: ",
            }

            kwargs = {}
            for field, prompt in prompts.items():
                value = input(prompt).strip()
                if value:
                    kwargs[field] = value

            if not kwargs:
                print("[Info] No changes provided.")
                return

            self.medicines = self.file_mgr.update_medicine(self.medicines, target.name, target.brand, **kwargs)

        except FileManagerError as e:
            print(f"[Error] Update process failed: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\n[Info] Update cancelled.")

    # ---------- reports ----------
    def sales_report(self):
        try:
            print("\n===== SALES REPORT =====")
            print("1. Today  2. This month  3. All time  4. Custom range")
            choice = input("Choose range: ").strip()

            today = datetime.date.today()
            if choice == "1":
                start = end = today
            elif choice == "2":
                start, end = today.replace(day=1), today
            elif choice == "3":
                start = end = None
            elif choice == "4":
                start = self.get_date("From date (YYYY-MM-DD): ")
                end = self.get_date("To date (YYYY-MM-DD): ")
            else:
                print("[Error] Invalid choice.")
                return

            report = self.invoice_gen.sales_report(start, end)
            print(f"\nTransactions  : {report['transactions']}")
            print(f"Total Sales   : Rs.{report['total_sales']}")
            print(f"Total Discount: Rs.{report['total_discount']}")
            print(f"Total Profit  : Rs.{report['total_profit']}")

        except (KeyboardInterrupt, EOFError):
            print("\n[Info] Report cancelled.")

    def top_selling_report(self):
        try:
            print("\n===== TOP SELLING MEDICINES =====")
            n = self.get_int("How many to show: ", min_value=1)
            ranked = self.invoice_gen.top_selling(n)
            if not ranked:
                print("No sales recorded yet.")
                return
            for i, ((name, brand), tabs_sold) in enumerate(ranked, start=1):
                print(f"{i}. {name} ({brand}) — {tabs_sold} tablets sold")
        except (KeyboardInterrupt, EOFError):
            print("\n[Info] Report cancelled.")

    def party_history_report(self):
        try:
            print("\n===== CUSTOMER / SUPPLIER HISTORY =====")
            party = input("Enter customer/supplier name: ").strip()
            if not party:
                print("[Error] Name cannot be empty.")
                return

            rows = self.invoice_gen.party_history(party)
            if not rows:
                print(f"No transaction history found for '{party}'.")
                return

            print(f"\nHistory for '{party}':")
            for row in rows:
                print(f" - {row['timestamp']} | {row['type']:<7} | {row['medicine']} ({row['brand']}) | "
                      f"{row['unit']} x{row['qty']} | Subtotal: Rs.{row['subtotal']}")

        except (KeyboardInterrupt, EOFError):
            print("\n[Info] Lookup cancelled.")

    def export_low_stock_report(self):
        try:
            low_stock = [m for m in self.medicines if m.qty <= LOW_STOCK_THRESHOLD]
            expiring = [m for m in self.medicines if 0 <= m.days_until_expiry() <= EXPIRY_WARNING_DAYS]
            expired = [m for m in self.medicines if m.is_expired()]

            lines = ["===== LOW STOCK & EXPIRY REPORT =====",
                     f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ""]

            lines.append(f"Low stock (<= {LOW_STOCK_THRESHOLD} tabs):")
            lines += [f" - {m.name} ({m.brand}): {m.qty} tabs" for m in low_stock] or [" (none)"]

            lines.append(f"\nExpiring within {EXPIRY_WARNING_DAYS} days:")
            lines += [f" - {m.name} ({m.brand}), Batch {m.batch_no}, expires {m.expiry_date}"
                      for m in expiring] or [" (none)"]

            lines.append("\nAlready expired:")
            lines += [f" - {m.name} ({m.brand}), Batch {m.batch_no}, expired {m.expiry_date}"
                      for m in expired] or [" (none)"]

            content = "\n".join(lines) + "\n"
            filename = f"low_stock_report_{datetime.date.today().strftime('%Y%m%d')}.txt"
            self.file_mgr.write_file(filename, content)
            print(f"Report saved as: {filename}")

        except FileManagerError as e:
            print(f"[Error] Could not export report: {e}")

    # ---------- main menu ----------
    MENU = {
        "1": ("View Inventory", lambda self: self.show_inventory(self.medicines)),
        "2": ("Sell Medicine", lambda self: self.sell()),
        "3": ("Restock Medicine", lambda self: self.restock()),
        "4": ("Search Medicine", lambda self: self.search()),
        "5": ("Add New Medicine", lambda self: self.add_medicine()),
        "6": ("Delete Medicine", lambda self: self.delete_medicine()),
        "7": ("Update Medicine", lambda self: self.update_medicine()),
        "8": ("Sales Report", lambda self: self.sales_report()),
        "9": ("Top Selling Medicines", lambda self: self.top_selling_report()),
        "10": ("Customer / Supplier History", lambda self: self.party_history_report()),
        "11": ("Export Low Stock & Expiry Report", lambda self: self.export_low_stock_report()),
    }

    def run(self):
        print("Loading inventory...")
        try:
            self.medicines = self.file_mgr.read_inventory()
        except FileManagerError as e:
            print("[Error] Could not load inventory:", e)
            self.medicines = []

        while True:
            print("\n==============================")
            print("  MEDSTORE PVT. LTD.")
            print("==============================")
            for key, (label, _) in self.MENU.items():
                print(f"{key}. {label}")
            print("0. Exit")
            print("------------------------------")

            try:
                choice = input("Enter your choice: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break

            if choice == "0":
                print("Goodbye!")
                break

            action = self.MENU.get(choice)
            if action is None:
                print("[Error] Invalid choice. Please pick a number from the menu.")
                continue

            try:
                action[1](self)
            except Exception as e:
                # Last-resort safety net so one bad action never crashes the app.
                print(f"[Error] Unexpected failure in '{action[0]}': {e}")


if __name__ == "__main__":
    app = MedStoreApp()
    app.run()