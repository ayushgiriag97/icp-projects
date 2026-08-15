# =============================================
#   CLASS 1: Medicine (data only)
# =============================================

import datetime

DATE_FORMAT = "%Y-%m-%d"


class Medicine:
    """A single medicine batch record. Uniquely identified by (name, brand)."""

    __slots__ = (
        "name", "brand", "qty", "rate_tablet", "rate_strip", "tabs_per_strip",
        "batch_no", "expiry_date", "cost_price", "prescription_required",
    )

    def __init__(self, name, brand, qty, rate_tablet, rate_strip, tabs_per_strip,
                 batch_no, expiry_date, cost_price=0.0, prescription_required=False):
        self.name = self.validate_str(name, "Medicine name")
        self.brand = self.validate_str(brand, "Brand")
        self.qty = self.validate_int(qty, "Quantity", allow_zero=True)
        self.rate_tablet = self.validate_number(rate_tablet, "Tablet rate")
        self.rate_strip = self.validate_number(rate_strip, "Strip rate")
        self.tabs_per_strip = self.validate_int(tabs_per_strip, "Tabs per strip", allow_zero=False)
        self.batch_no = self.validate_str(batch_no, "Batch number")
        self.expiry_date = self.validate_date(expiry_date, "Expiry date")
        self.cost_price = self.validate_number(cost_price, "Cost price")
        self.prescription_required = self.validate_bool(prescription_required, "Prescription required flag")

    # ---------- validation helpers (also reused by FileManager for updates) ----------
    @staticmethod
    def validate_str(value, field_name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string.")
        return value.strip()

    @staticmethod
    def validate_int(value, field_name, allow_zero=True):
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{field_name} must be an integer.")
        if allow_zero and value < 0:
            raise ValueError(f"{field_name} must be a non-negative integer.")
        if not allow_zero and value <= 0:
            raise ValueError(f"{field_name} must be a positive integer.")
        return value

    @staticmethod
    def validate_number(value, field_name):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{field_name} must be a non-negative number.")
        if value < 0:
            raise ValueError(f"{field_name} must be a non-negative number.")
        return float(value)

    @staticmethod
    def validate_bool(value, field_name):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            v = value.strip().lower()
            if v in ("true", "yes", "y", "1"):
                return True
            if v in ("false", "no", "n", "0", ""):
                return False
        raise ValueError(f"{field_name} must be yes/no.")

    @staticmethod
    def validate_date(value, field_name):
        if isinstance(value, datetime.date):
            return value
        if isinstance(value, str):
            try:
                return datetime.datetime.strptime(value.strip(), DATE_FORMAT).date()
            except ValueError:
                raise ValueError(f"{field_name} must be in {DATE_FORMAT} format.")
        raise ValueError(f"{field_name} must be a date string ({DATE_FORMAT}).")

    # ---------- expiry helpers ----------
    def is_expired(self, as_of=None):
        as_of = as_of or datetime.date.today()
        return self.expiry_date < as_of

    def days_until_expiry(self, as_of=None):
        as_of = as_of or datetime.date.today()
        return (self.expiry_date - as_of).days

    # ---------- (de)serialization ----------
    def to_csv_line(self):
        """Serialize this medicine to a single CSV line (no trailing newline)."""
        return (f"{self.name}, {self.brand}, {self.qty}, {self.rate_tablet}, {self.rate_strip}, "
                f"{self.tabs_per_strip}, {self.batch_no}, {self.expiry_date.strftime(DATE_FORMAT)}, "
                f"{self.cost_price}, {'yes' if self.prescription_required else 'no'}")

    @classmethod
    def from_csv_line(cls, line):
        """
        Parse a single CSV line into a Medicine instance.
        Raises ValueError with a human-readable reason if the line is malformed
        so callers (e.g. FileManager) can decide whether to skip or abort.
        """
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 10:
            raise ValueError(f"expected 10 fields, got {len(parts)}")

        (name, brand, qty, rate_tablet, rate_strip, tabs_per_strip,
         batch_no, expiry_date, cost_price, prescription_required) = parts
        try:
            qty = int(qty)
            rate_tablet = float(rate_tablet)
            rate_strip = float(rate_strip)
            tabs_per_strip = int(tabs_per_strip)
            cost_price = float(cost_price)
        except ValueError:
            raise ValueError("data type conversion error")

        return cls(name, brand, qty, rate_tablet, rate_strip, tabs_per_strip,
                    batch_no, expiry_date, cost_price, prescription_required)

    # ---------- display ----------
    def __str__(self):
        return (self.name + "  |  " + self.brand +
                "  |  " + str(self.qty) + " tabs  |  Rs." +
                str(self.rate_tablet) + "  |  Rs." + str(self.rate_strip))
