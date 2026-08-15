# =============================================
#   CLASS 2: FileManager
# =============================================

import os
from medicine import Medicine


class FileManagerError(Exception):
    """Custom exception for FileManager errors."""
    pass


class FileManager:
    def __init__(self, inventory_file):
        if not isinstance(inventory_file, str) or not inventory_file.strip():
            raise FileManagerError("Inventory file path must be a non-empty string.")
        self.inventory_file = inventory_file

    # ---------- reading ----------
    def read_inventory(self):
        """Load all medicines from the inventory file, skipping malformed lines."""
        medicines = []

        if not os.path.exists(self.inventory_file):
            print("[Info] Inventory file not found. Creating a new empty inventory file.")
            try:
                open(self.inventory_file, "w", encoding="utf-8").close()
            except OSError as e:
                raise FileManagerError(f"Could not create inventory file: {e}")
            return medicines

        try:
            with open(self.inventory_file, "r", encoding="utf-8") as file:
                for line_no, line in enumerate(file, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        medicines.append(Medicine.from_csv_line(line))
                    except ValueError as e:
                        print(f"[Warning] Skipping line {line_no}: {e}")
        except PermissionError:
            raise FileManagerError("Permission denied while reading inventory file.")
        except OSError as e:
            raise FileManagerError(f"Error while reading inventory file: {e}")

        return medicines

    # ---------- writing ----------
    def save_inventory(self, medicines):
        """Overwrite the inventory file with the given list of Medicine objects."""
        if not isinstance(medicines, list):
            raise FileManagerError("Medicines must be provided as a list.")

        lines = []
        for m in medicines:
            if not isinstance(m, Medicine):
                print(f"[Warning] Skipping non-Medicine entry: {m!r}")
                continue
            lines.append(m.to_csv_line())

        try:
            with open(self.inventory_file, "w", encoding="utf-8") as file:
                file.write("\n".join(lines))
                if lines:
                    file.write("\n")
            return True
        except PermissionError:
            raise FileManagerError("Permission denied while saving inventory file.")
        except OSError as e:
            raise FileManagerError(f"Error while saving inventory file: {e}")

    def write_file(self, filename, content):
        """Write arbitrary text content to a file (used for invoices/restock notes/reports)."""
        if not isinstance(filename, str) or not filename.strip():
            raise FileManagerError("Filename must be a non-empty string.")
        if not isinstance(content, str):
            raise FileManagerError("Content must be a string.")

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(content)
            return True
        except PermissionError:
            raise FileManagerError("Permission denied while writing to file.")
        except OSError as e:
            raise FileManagerError(f"Error while writing file {filename}: {e}")

    def append_medicine(self, medicine):
        """Append a single Medicine object to the inventory file without rewriting everything."""
        if not isinstance(medicine, Medicine):
            raise FileManagerError("append_medicine expects a Medicine object.")

        try:
            with open(self.inventory_file, "a", encoding="utf-8") as file:
                file.write(medicine.to_csv_line() + "\n")
            return True
        except PermissionError:
            raise FileManagerError("Permission denied while appending to inventory file.")
        except OSError as e:
            raise FileManagerError(f"Error while appending medicine: {e}")

    # ---------- mutation helpers (operate on in-memory list + persist) ----------
    # NOTE: medicines are identified by (name, brand) together, since the same
    # medicine name can now exist under multiple brands.

    def delete_medicine(self, medicines, name, brand):
        """Delete the medicine matching (name, brand) and persist the result."""
        if not isinstance(medicines, list):
            raise FileManagerError("Medicines must be provided as a list.")
        if not isinstance(name, str) or not name.strip():
            raise FileManagerError("Medicine name must be a non-empty string.")
        if not isinstance(brand, str) or not brand.strip():
            raise FileManagerError("Brand must be a non-empty string.")

        target_name = name.strip().lower()
        target_brand = brand.strip().lower()
        updated = [m for m in medicines
                   if not (m.name.lower() == target_name and m.brand.lower() == target_brand)]

        if len(updated) == len(medicines):
            print(f"[Info] No medicine found matching '{name}' ({brand}).")
            return medicines

        self.save_inventory(updated)
        print(f"[Success] Medicine '{name}' ({brand}) deleted.")
        return updated

    # field -> parser(raw_value) -> converted, validated value (raises ValueError on bad input)
    _FIELD_PARSERS = {
        "qty": lambda v: Medicine.validate_int(FileManager._to_int(v, "Quantity"), "Quantity", allow_zero=True),
        "rate_tablet": lambda v: Medicine.validate_number(FileManager._to_float(v, "Tablet rate"), "Tablet rate"),
        "rate_strip": lambda v: Medicine.validate_number(FileManager._to_float(v, "Strip rate"), "Strip rate"),
        "brand": lambda v: Medicine.validate_str(v, "Brand"),
        "tabs_per_strip": lambda v: Medicine.validate_int(
            FileManager._to_int(v, "Tabs per strip"), "Tabs per strip", allow_zero=False),
        "batch_no": lambda v: Medicine.validate_str(v, "Batch number"),
        "expiry_date": lambda v: Medicine.validate_date(v, "Expiry date"),
        "cost_price": lambda v: Medicine.validate_number(FileManager._to_float(v, "Cost price"), "Cost price"),
        "prescription_required": lambda v: Medicine.validate_bool(v, "Prescription required flag"),
    }

    @staticmethod
    def _to_int(value, field_name):
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValueError(f"{field_name} must be a whole number.")

    @staticmethod
    def _to_float(value, field_name):
        try:
            return float(value)
        except (TypeError, ValueError):
            raise ValueError(f"{field_name} must be a number.")

    def update_medicine(self, medicines, name, brand, **kwargs):
        """Update one or more fields of the medicine matching (name, brand) and persist."""
        if not isinstance(medicines, list):
            raise FileManagerError("Medicines must be provided as a list.")
        if not isinstance(name, str) or not name.strip():
            raise FileManagerError("Medicine name must be a non-empty string.")
        if not isinstance(brand, str) or not brand.strip():
            raise FileManagerError("Brand must be a non-empty string.")

        unknown = set(kwargs) - set(self._FIELD_PARSERS)
        if unknown:
            raise FileManagerError(f"Unknown field(s): {', '.join(sorted(unknown))}")

        target_name = name.strip().lower()
        target_brand = brand.strip().lower()
        target = next((m for m in medicines
                       if m.name.lower() == target_name and m.brand.lower() == target_brand), None)
        if target is None:
            print(f"[Info] No medicine found matching '{name}' ({brand}).")
            return medicines

        changed = False
        for field, raw_value in kwargs.items():
            try:
                setattr(target, field, self._FIELD_PARSERS[field](raw_value))
                changed = True
            except ValueError as e:
                print(f"[Error] Update failed for '{field}': {e}")

        if not changed:
            print(f"[Info] No valid fields to update for '{name}' ({brand}).")
            return medicines

        print(f"[Success] Medicine '{name}' ({brand}) updated.")
        self.save_inventory(medicines)
        return medicines