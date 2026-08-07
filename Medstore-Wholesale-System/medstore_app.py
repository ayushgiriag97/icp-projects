# =============================================
#   CLASS 4: MedStoreApp (Main Application)
# =============================================

import os
import difflib
import re
from medicine import Medicine
from file_manager import FileManager
from invoice_generator import InvoiceGenerator

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/"
INVENTORY_FILE = SCRIPT_FOLDER + "medicines.txt"

class MedStoreApp:
    def __init__(self):
        self.file_mgr    = FileManager(INVENTORY_FILE)
        self.invoice_gen = InvoiceGenerator()
        self.medicines   = []

    def get_int(self, prompt):
        while True:
            value = input(prompt).strip()
            if value.isdigit():
                return int(value)
            else:
                print("  [Error] Please enter a whole number.")

    def get_float(self, prompt):
        while True:
            value = input(prompt).strip()
            try:
                num = float(value)
                if num < 0:
                    print("  [Error] Value cannot be negative.")
                else:
                    return num
            except ValueError:
                print("  [Error] Please enter a valid number.")

    def show_inventory(self, medicines):
        print("\n----------------------------------------------------------")
        print(" No.  Medicine             Brand          Stock   Tab-Rate  Strip-Rate")
        print("----------------------------------------------------------")
        i = 1
        for m in medicines:
            print(str(i) + ".  " + str(m))
            i += 1
        print("----------------------------------------------------------")

    # ---------- Sell medicines ----------
    def sell(self):
        try:
            print("\n===== SELL MEDICINE =====")
            customer = input("Customer name: ").strip()

            # Validate customer name
            if not customer or not all(ch.isalpha() or ch.isspace() for ch in customer):
                print("[Error] Customer name must contain only letters and cannot be empty.")
                return

            total = 0.0
            total_discount = 0.0
            invoice_lines = []

            while True:
                # Show inventory with exit option
                self.show_inventory(self.medicines)
                exit_number = len(self.medicines) + 1
                print(f"{exit_number}. Exit Sell Medicine")

                choice = input("Enter medicine number (or type 'exit'): ").strip().lower()
                # Exit conditions
                if choice == "exit" or choice == str(exit_number):
                    break

                if not choice.isdigit():
                    print("Invalid input. Enter a number or 'exit'.")
                    continue

                choice = int(choice)
                if choice < 1 or choice > len(self.medicines):
                    print("Invalid choice. Try again.")
                    continue

                m = self.medicines[choice - 1]

                # Unit validation
                unit = input("Sell by (T)ablet or (S)trip? ").strip().upper()
                if unit not in ["T", "S"]:
                    print("Invalid unit. Enter T or S only.")
                    continue

                qty = self.get_int("Quantity: ")
                if qty <= 0:
                    print("Quantity must be at least 1.")
                    continue

                # Pricing logic
                if unit == "T":
                    tabs_needed = qty
                    rate = m.rate_tablet
                    unit_name = "Tablet(s)"
                else:
                    tabs_needed = qty * m.tabs_per_strip
                    rate = m.rate_strip
                    unit_name = "Strip(s)"

                # Stock validation
                if tabs_needed > m.qty:
                    print(f"Only {m.qty} tablets left. Try again.")
                    continue

                #discount logic
                discount = 0.0

                subtotal = rate * qty

                if unit == "T":
                    if qty >= 50 and qty < 100:
                        discount = round(subtotal * 0.02, 2)   # 2% discount
                    elif qty >= 100:
                        discount = round(subtotal * 0.05, 2)   # 5% discount

                elif unit == "S":
                    if qty >= 2 and qty < 5:
                        discount = round(subtotal * 0.05, 2)   # 5% discount
                    elif qty >= 5:
                        discount = round(subtotal * 0.10, 2)   # 10% discount

                subtotal -= discount


                # Update inventory and totals
                m.qty -= tabs_needed
                total += subtotal
                total_discount += discount

                line = f"{m.name} | {unit_name} x{qty} | Rate: Rs.{rate} | Discount: Rs.{discount} | Subtotal: Rs.{round(subtotal,2)}"
                invoice_lines.append(line)
                print("Added to cart:", line)

                # Cart preview
                print("\nYour Medicine Cart:")
                for item in invoice_lines:
                    print(" -", item)
                print(f"Total so far: Rs.{round(total,2)}")
                print(f"Discount received so far: Rs.{round(total_discount,2)}")
                print(f"Net total so far: Rs.{round(total,2)}\n")

            if not invoice_lines:
                print("No items sold.")
                return

            # Generate invoice
            invoice_content = self.invoice_gen.make_sale_invoice(customer, invoice_lines, total)
            invoice_filename = self.invoice_gen.unique_name("invoice", customer)

            self.file_mgr.write_file(invoice_filename, invoice_content)
            self.file_mgr.save_inventory(self.medicines)

            print("Invoice saved as:", invoice_filename)
            print("Final Total: Rs.", round(total, 2))
            print("Total Discount Applied: Rs.", round(total_discount, 2))

        except Exception as e:
            print(f"[Error] Sell process failed: {str(e)}")


    # ---------- Restock medicines ----------
    def restock(self):
        try:
            print("\n===== RESTOCK MEDICINE =====")
            supplier = input("Supplier name: ").strip()

            # Validate supplier name
            if not supplier or not all(ch.isalpha() or ch.isspace() for ch in supplier):
                print("[Error] Supplier name must contain only letters and cannot be empty.")
                return

            total = 0.0
            total_discount = 0.0
            note_lines = [] 

            while True:
                # Show inventory
                self.show_inventory(self.medicines)

                # Low stock alerts
                low_stock_found = False
                for m in self.medicines:
                    if m.qty <= 50:  # threshold
                        if not low_stock_found:
                            print("\n[Low Stock Alerts]")
                        print(f" - {m.name} ({m.brand}) has only {m.qty} tablets left. Consider restocking.")
                        low_stock_found = True

                if not low_stock_found:
                    print("\n[Low Stock Alerts] None at the moment.")


                # Exit option
                exit_number = len(self.medicines) + 1
                print(f"{exit_number}. Exit Restock Medicine")

                choice = input("Enter medicine number (or type 'exit'): ").strip().lower()

                # Exit conditions
                if choice == "exit" or choice == str(exit_number):
                    break

                if not choice.isdigit():
                    print("Invalid input. Enter a valid number or 'exit'.")
                    continue

                choice = int(choice)
                if choice < 1 or choice > len(self.medicines):
                    print("Invalid choice. Try again.")
                    continue

                m = self.medicines[choice - 1]

                # Unit validation
                unit = input("Restock by (T)ablet or (S)trip? ").strip().upper()
                if unit not in ["T", "S"]:
                    print("Invalid unit. Enter T or S only.")
                    continue

                qty = self.get_int("Quantity: ")
                if qty <= 0:
                    print("Quantity must be at least 1.")
                    continue

                # Pricing logic
                if unit == "T":
                    tabs_added = qty
                    rate = m.rate_tablet
                    unit_name = "Tablet(s)"
                else:
                    tabs_added = qty * m.tabs_per_strip
                    rate = m.rate_strip
                    unit_name = "Strip(s)"

                subtotal = rate * qty
                discount = 0.0

                # Restock bulk discount
                if tabs_added >= 1000:
                    discount = round(subtotal * 0.10, 2)  # 10% discount
                    subtotal -= discount

                # Update inventory
                m.qty += tabs_added
                total += subtotal
                total_discount += discount

                line = f"{m.name} | {unit_name} x{qty} | Rate: Rs.{rate} | Discount: Rs.{discount} | Subtotal: Rs.{round(subtotal,2)}"
                note_lines.append(line)
                print("Restocked:", line)

                # Restock summary
                print("\nRestock Summary:")
                for item in note_lines:
                    print(" -", item)
                print(f"Total restock value so far: Rs.{round(total,2)}")
                print(f"Supplier discount applied so far: Rs.{round(total_discount,2)}\n")

            if not note_lines:
                print("No items restocked.")
                return

            # Generate restock note
            note_content = self.invoice_gen.make_restock_note(supplier, note_lines, total)
            note_filename = self.invoice_gen.unique_name("restock", supplier)

            self.file_mgr.write_file(note_filename, note_content)
            self.file_mgr.save_inventory(self.medicines)

            print("Restock note saved as:", note_filename)
            print("Final Total Restock Value: Rs.", round(total, 2))
            print("Total Supplier Discount Applied: Rs.", round(total_discount, 2))

        except Exception as e:
            print(f"[Error] Restock process failed: {str(e)}")


    # ---------- Search medicine ----------
    def search(self):
        try:
            # Edge case: empty inventory
            if not self.medicines:
                print("[Error] Inventory is empty. Please add medicines first.")
                return

            keyword = input("Enter search (name/brand or filter): ").strip().lower()

            # Input validation
            if not keyword:
                print("[Error] Search keyword cannot be empty.")
                return
            if len(keyword) < 2 and not any(op in keyword for op in ["<", ">", "rate", "stock"]):
                print("[Error] Please enter at least 2 characters for search.")
                return

            found = []

            # --- Advanced filters ---
            stock_match = re.match(r"stock\s*([<>]=?)\s*(\d+)", keyword)
            rate_match = re.match(r"rate\s*([<>]=?)\s*(\d+)", keyword)

            if stock_match:
                op, val = stock_match.groups()
                val = int(val)
                if op == "<":
                    found = [m for m in self.medicines if m.qty < val]
                elif op == "<=":
                    found = [m for m in self.medicines if m.qty <= val]
                elif op == ">":
                    found = [m for m in self.medicines if m.qty > val]
                elif op == ">=":
                    found = [m for m in self.medicines if m.qty >= val]

            elif rate_match:
                op, val = rate_match.groups()
                val = float(val)
                if op == "<":
                    found = [m for m in self.medicines if m.rate_tablet < val]
                elif op == "<=":
                    found = [m for m in self.medicines if m.rate_tablet <= val]
                elif op == ">":
                    found = [m for m in self.medicines if m.rate_tablet > val]
                elif op == ">=":
                    found = [m for m in self.medicines if m.rate_tablet >= val]

            else:
                # --- Normal search by name/brand ---
                found = [m for m in self.medicines if keyword in m.name.lower() or keyword in m.brand.lower()]

                # Fuzzy matches if nothing found
                if not found:
                    names = [m.name for m in self.medicines]
                    brands = [m.brand for m in self.medicines]
                    close_matches = difflib.get_close_matches(keyword, names + brands, cutoff=0.6)
                    if close_matches:
                        found = [m for m in self.medicines if m.name in close_matches or m.brand in close_matches]

            # --- Sorting options ---
            if keyword in ["rate asc", "rate low", "rate min"]:
                found = sorted(self.medicines, key=lambda m: m.rate_tablet)
            elif keyword in ["rate desc", "rate high", "rate max"]:
                found = sorted(self.medicines, key=lambda m: m.rate_tablet, reverse=True)
            elif keyword in ["stock asc", "stock low", "stock min"]:
                found = sorted(self.medicines, key=lambda m: m.qty)
            elif keyword in ["stock desc", "stock high", "stock max"]:
                found = sorted(self.medicines, key=lambda m: m.qty, reverse=True)

            # --- Results handling ---
            if not found:
                print(f"No medicine found matching '{keyword}'.")
            else:
                print(f"Found {len(found)} medicine(s) matching '{keyword}':")
                for m in found:
                    name, brand = m.name, m.brand

                    # Highlight matches
                    if keyword in name.lower():
                        idx = name.lower().find(keyword)
                        name = name[:idx] + "[" + name[idx:idx+len(keyword)] + "]" + name[idx+len(keyword):]
                    if keyword in brand.lower():
                        idx = brand.lower().find(keyword)
                        brand = brand[:idx] + "[" + brand[idx:idx+len(keyword)] + "]" + brand[idx+len(keyword):]

                    print(f"- {name} | {brand} | Stock: {m.qty} | Rate: Rs.{m.rate_tablet} | Strip Rate: Rs.{m.rate_strip}")

        except Exception as e:
            print(f"[Error] Search failed: {str(e)}")

    # ---------- Add new medicine ----------
    def add_medicine(self):
        try:
            print("\n===== ADD NEW MEDICINE =====")
            name           = input("Medicine name        : ").strip()
            brand          = input("Brand name           : ").strip()
            qty            = self.get_int("Initial stock (tabs) : ")
            rate_tablet    = self.get_float("Rate per tablet (Rs) : ")
            rate_strip     = self.get_float("Rate per strip  (Rs) : ")
            tabs_per_strip = self.get_int("Tablets per strip    : ")

            if name == "" or brand == "" or tabs_per_strip == 0:
                print("[Error] Name, brand and tablets-per-strip are required.")
                return

            new_med = Medicine(name, brand, qty, rate_tablet, rate_strip, tabs_per_strip)
            self.medicines.append(new_med)

            self.file_mgr.save_inventory(self.medicines)
            print(name + " added to inventory.")

        except Exception as e:
            print("[Error] Failed to add medicine:", e)

    # ---------- Main menu ----------
    def run(self):
        try:
            print("Loading inventory...")
            self.medicines = self.file_mgr.read_inventory()
        except Exception as e:
            print("[Error] Could not load inventory:", e)
            self.medicines = []

        while True:
            print("\n==============================")
            print("  MEDSTORE PVT. LTD.")
            print("==============================")
            print("1. View Inventory")
            print("2. Sell Medicine")
            print("3. Restock Medicine")
            print("4. Search Medicine")
            print("5. Add New Medicine")
            print("0. Exit")
            print("------------------------------")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.show_inventory(self.medicines)
            elif choice == "2":
                self.sell()
            elif choice == "3":
                self.restock()
            elif choice == "4":
                self.search()
            elif choice == "5":
                self.add_medicine()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("[Error] Invalid choice. Please enter 0-5.")

if __name__ == "__main__":
    app = MedStoreApp()
    app.run()
