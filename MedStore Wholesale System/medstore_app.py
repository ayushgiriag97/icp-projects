# =============================================
#   CLASS 4: MedStoreApp (Main Application)
# =============================================

import os
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
            if customer == "":
                print("[Error] Customer name cannot be empty.")
                return
            if not all(ch.isalpha() or ch.isspace() for ch in customer):
                print("[Error] Customer name must contain only letters.")
                return

            total = 0.0
            invoice_lines = []


            while True:
                self.show_inventory(self.medicines)
                choice = self.get_int("Enter medicine number to sell (0 to finish): ")
                if choice == 0:
                    break
                if choice < 1 or choice > len(self.medicines):
                    print("[Error] Invalid number. Try again.")
                    continue

                m = self.medicines[choice - 1]

                unit = input("Sell by (T)ablet or (S)trip? ").strip().upper()
                if unit not in ["T", "S"]:
                    print("[Error] Enter T or S only.")
                    continue

                qty = self.get_int("Quantity: ")
                if qty == 0:
                    print("[Error] Quantity must be at least 1.")
                    continue

                if unit == "T":
                    tabs_needed = qty
                    rate        = m.rate_tablet
                    unit_name   = "Tablet(s)"
                else:
                    tabs_needed = qty * m.tabs_per_strip
                    rate        = m.rate_strip
                    unit_name   = "Strip(s)"

                if tabs_needed > m.qty:
                    print("[Error] Not enough stock. Available: " + str(m.qty) + " tablets.")
                    continue

                subtotal = rate * qty
                discount = 0.0

                if unit == "S" and qty >= 2:
                    discount = subtotal * 0.05
                    subtotal -= discount

                m.qty  -= tabs_needed
                total += subtotal

                line = (m.name + " | " + unit_name + " x" + str(qty) +
                        " | Rate: Rs." + str(rate) +
                        " | Discount: Rs." + str(round(discount, 2)) +
                        " | Subtotal: Rs." + str(round(subtotal, 2)))
                invoice_lines.append(line)
                print("Added to cart: " + line)

            if not invoice_lines:
                print("No items sold.")
                return

            invoice_content  = self.invoice_gen.make_sale_invoice(customer, invoice_lines, total)
            invoice_filename = self.invoice_gen.unique_name("invoice", customer)

            self.file_mgr.write_file(invoice_filename, invoice_content)
            self.file_mgr.save_inventory(self.medicines)

            print("Invoice saved as: " + invoice_filename)
            print("Total: Rs." + str(round(total, 2)))

        except Exception as e:
            print("[Error] Sell process failed:", e)

    # ---------- Restock medicines ----------
    def restock(self):
        try:
            print("\n===== RESTOCK MEDICINE =====")
            supplier = input("Supplier name: ").strip()
            if supplier == "":
                print("[Error] Supplier name cannot be empty.")
                return
            if not all(ch.isalpha() or ch.isspace() for ch in supplier):
                print("[Error] Supplier name must contain only letters.")
                return

            total      = 0.0
            note_lines = []

            while True:
                self.show_inventory(self.medicines)
                choice = self.get_int("Enter medicine number to restock (0 to finish): ")
                if choice == 0:
                    break
                if choice < 1 or choice > len(self.medicines):
                    print("[Error] Invalid number. Try again.")
                    continue

                m = self.medicines[choice - 1]

                unit = input("Restock by (T)ablet or (S)trip? ").strip().upper()
                if unit not in ["T", "S"]:
                    print("[Error] Enter T or S only.")
                    continue

                qty = self.get_int("Quantity: ")
                if qty == 0:
                    print("[Error] Quantity must be at least 1.")
                    continue

                if unit == "T":
                    tabs_added = qty
                    rate       = m.rate_tablet
                    unit_name  = "Tablet(s)"
                else:
                    tabs_added = qty * m.tabs_per_strip
                    rate       = m.rate_strip
                    unit_name  = "Strip(s)"

                subtotal  = rate * qty
                m.qty    += tabs_added
                total    += subtotal

                line = (m.name + " | " + unit_name + " x" + str(qty) +
                        " | Rate: Rs." + str(rate) +
                        " | Subtotal: Rs." + str(round(subtotal, 2)))
                note_lines.append(line)
                print("Restocked: " + line)

            if not note_lines:
                print("No items restocked.")
                return

            note_content  = self.invoice_gen.make_restock_note(supplier, note_lines, total)
            note_filename = self.invoice_gen.unique_name("restock", supplier)

            self.file_mgr.write_file(note_filename, note_content)
            self.file_mgr.save_inventory(self.medicines)

            print("Restock note saved as: " + note_filename)
            print("Total: Rs." + str(round(total, 2)))

        except Exception as e:
            print("[Error] Restock process failed:", e)

    # ---------- Search medicine ----------
    def search(self):
        try:
            keyword = input("Enter medicine name to search: ").strip().lower()
            found = [m for m in self.medicines if keyword in m.name.lower()]
            if not found:
                print("No medicine found with that name.")
            else:
                self.show_inventory(found)
        except Exception as e:
            print("[Error] Search failed:", e)

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