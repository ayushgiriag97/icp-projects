# =============================================
#   CLASS 2: FileManager
# =============================================

import os
from medicine import Medicine

class FileManager:
    def __init__(self, inventory_file):
        self.inventory_file = inventory_file

    def read_inventory(self):
        medicines = []

        # File not found handling
        if not os.path.exists(self.inventory_file):
            print("Inventory file not found. Creating a new empty inventory file.")
            open(self.inventory_file, "w").close()
            return medicines

        try:
            with open(self.inventory_file, "r") as file:
                for line_no, line in enumerate(file, start=1):
                    line = line.strip()

                    if line == "":
                        continue

                    parts = line.split(",")

                    # Invalid line format handling
                    if len(parts) != 6:
                        print(f"Skipping invalid line {line_no}: Wrong number of values")
                        continue

                    try:
                        m = Medicine(
                            name           = parts[0].strip(),
                            brand          = parts[1].strip(),
                            qty            = int(parts[2].strip()),
                            rate_tablet    = float(parts[3].strip()),
                            rate_strip     = float(parts[4].strip()),
                            tabs_per_strip = int(parts[5].strip())
                        )
                        medicines.append(m)

                    except ValueError:
                        print(f"Skipping invalid line {line_no}: Data type conversion error")
                        continue

        except PermissionError:
            print("Error: Permission denied while reading inventory file.")
        except Exception as e:
            print("Error while reading inventory file:", e)

        return medicines


    def save_inventory(self, medicines):
        try:
            with open(self.inventory_file, "w") as file:
                for m in medicines:
                    line = (m.name + ", " + m.brand + ", " +
                            str(m.qty) + ", " + str(m.rate_tablet) + ", " +
                            str(m.rate_strip) + ", " + str(m.tabs_per_strip) + "\n")
                    file.write(line)

        except PermissionError:
            print("Error: Permission denied while saving inventory file.")
        except Exception as e:
            print("Error while saving inventory file:", e)


    def write_file(self, filename, content):
        try:
            with open(filename, "w") as file:
                file.write(content)

        except PermissionError:
            print("Error: Permission denied while writing to file.")
        except Exception as e:
            print("Error while writing file:", e)