# =============================================
#   CLASS 1: Medicine (data only)
# =============================================


class Medicine:
    def __init__(self, name, brand, qty, rate_tablet, rate_strip, tabs_per_strip):

        # --- Validation (Error Handling) ---
        
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Medicine name must be a non-empty string.")

        if not isinstance(brand, str) or brand.strip() == "":
            raise ValueError("Brand must be a non-empty string.")

        if not isinstance(qty, int) or qty < 0:
            raise ValueError("Quantity must be a non-negative integer (tablets).")

        if not (isinstance(rate_tablet, int) or isinstance(rate_tablet, float)) or rate_tablet < 0:
            raise ValueError("Tablet rate must be a non-negative number.")

        if not (isinstance(rate_strip, int) or isinstance(rate_strip, float)) or rate_strip < 0:
            raise ValueError("Strip rate must be a non-negative number.")

        if not isinstance(tabs_per_strip, int) or tabs_per_strip <= 0:
            raise ValueError("Tabs per strip must be a positive integer.")

        # --- Assign values ---
        self.name           = name.strip()
        self.brand          = brand.strip()
        self.qty            = qty
        self.rate_tablet    = float(rate_tablet)
        self.rate_strip     = float(rate_strip)
        self.tabs_per_strip = tabs_per_strip

    def __str__(self):
        return (self.name + "  |  " + self.brand +
                "  |  " + str(self.qty) + " tabs  |  Rs." +
                str(self.rate_tablet) + "  |  Rs." + str(self.rate_strip))
