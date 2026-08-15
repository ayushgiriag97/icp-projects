# =============================================
#   CLASS 3: InvoiceGenerator
# =============================================

import os
import csv
import datetime
import uuid

TRANSACTION_FIELDS = [
    "timestamp", "type", "party", "medicine", "brand", "batch_no",
    "unit", "qty", "tabs_count", "rate", "discount", "subtotal",
    "cost_price", "rx_ref",
]


class InvoiceError(Exception):
    """Custom exception for invoice generation errors."""
    pass


class InvoiceGenerator:
    def __init__(self, log_file="audit_log.txt", transactions_file="transactions.csv"):
        if not isinstance(log_file, str) or not log_file.strip():
            raise InvoiceError("Log file path must be a non-empty string.")
        if not isinstance(transactions_file, str) or not transactions_file.strip():
            raise InvoiceError("Transactions file path must be a non-empty string.")
        self.log_file = log_file
        self.transactions_file = transactions_file

    def log_action(self, action_type, identifier, filename):
        """Log invoice/restock creation for audit purposes. Never blocks the caller."""
        try:
            with open(self.log_file, "a", encoding="utf-8") as log:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log.write(f"{timestamp} | {action_type} | {identifier} | {filename}\n")
        except OSError as e:
            print(f"[Warning] Audit log failed: {e}")

    def unique_name(self, prefix, identifier):
        """Build a filesystem-safe, collision-free filename like prefix_identifier[_N].txt."""
        if not isinstance(prefix, str) or not prefix.strip():
            raise InvoiceError("Prefix must be a non-empty string.")
        if not isinstance(identifier, str) or not identifier.strip():
            raise InvoiceError("Identifier must be a non-empty string.")

        safe_identifier = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in identifier.strip())
        base = f"{prefix.strip()}_{safe_identifier}"
        filename = f"{base}.txt"
        counter = 1
        while os.path.exists(filename):
            filename = f"{base}_{counter}.txt"
            counter += 1
        return filename

    def _format_lines(self, lines):
        """Format pipe-delimited invoice/restock lines into neat fixed-width columns."""
        formatted = ""
        for line in lines:
            if not isinstance(line, str) or not line.strip():
                raise InvoiceError("Line must be a non-empty string.")
            parts = line.split("|")
            formatted += "".join(part.strip().ljust(22) for part in parts) + "\n"
        return formatted

    def _build_document(self, doc_title, id_label, entity_label, entity_name, lines, total, action_type):
        """Shared layout/validation for both sale invoices and restock notes."""
        if not isinstance(entity_name, str) or not entity_name.strip():
            raise InvoiceError(f"{entity_label} name must be a non-empty string.")
        if not isinstance(lines, list) or not lines:
            raise InvoiceError("Lines must be a non-empty list.")
        if not isinstance(total, (int, float)) or isinstance(total, bool) or total < 0:
            raise InvoiceError("Total must be a non-negative number.")

        doc_id = str(uuid.uuid4())[:8]
        date_str = datetime.datetime.now().strftime("%d-%b-%Y %H:%M")

        content = (
            "============================\n"
            "   MEDSTORE PVT. LTD.\n"
            f"   {doc_title}\n"
            "============================\n"
            f"{id_label:<10}: {doc_id}\n"
            f"{'Date':<10}: {date_str}\n"
            f"{entity_label:<10}: {entity_name.strip()}\n"
            "----------------------------\n"
        )
        content += self._format_lines(lines)
        content += "----------------------------\n"
        content += f"TOTAL : Rs.{round(total, 2)}\n"
        content += "============================\n"

        self.log_action(action_type, entity_name, f"{action_type.lower()}_{entity_name}.txt")
        return content

    def make_sale_invoice(self, customer, invoice_lines, total):
        return self._build_document(
            "SALES INVOICE", "Invoice ID", "Customer", customer, invoice_lines, total, "SALE_INVOICE"
        )

    def make_restock_note(self, supplier, note_lines, total):
        return self._build_document(
            "RESTOCK NOTE", "Note ID", "Supplier", supplier, note_lines, total, "RESTOCK_NOTE"
        )

    # ---------- transaction log (backs reports + customer/supplier history) ----------
    def record_transaction(self, txn_type, party, medicine, unit, qty, tabs_count,
                            rate, discount, subtotal, rx_ref=""):
        """Append one line-item transaction to transactions.csv. Never blocks the caller."""
        if txn_type not in ("SALE", "RESTOCK"):
            raise InvoiceError("Transaction type must be 'SALE' or 'RESTOCK'.")
        if not isinstance(party, str) or not party.strip():
            raise InvoiceError("Party name must be a non-empty string.")

        file_exists = os.path.exists(self.transactions_file)
        try:
            with open(self.transactions_file, "a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(TRANSACTION_FIELDS)
                writer.writerow([
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    txn_type, party.strip(), medicine.name, medicine.brand, medicine.batch_no,
                    unit, qty, tabs_count, rate, discount, round(subtotal, 2),
                    medicine.cost_price, rx_ref,
                ])
        except OSError as e:
            print(f"[Warning] Could not record transaction: {e}")

    def _read_transactions(self):
        if not os.path.exists(self.transactions_file):
            return []
        try:
            with open(self.transactions_file, "r", encoding="utf-8", newline="") as f:
                return list(csv.DictReader(f))
        except OSError as e:
            print(f"[Warning] Could not read transaction history: {e}")
            return []

    @staticmethod
    def _within_range(timestamp_str, start_date, end_date):
        ts = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").date()
        if start_date and ts < start_date:
            return False
        if end_date and ts > end_date:
            return False
        return True

    def sales_report(self, start_date=None, end_date=None):
        """Aggregate totals for SALE transactions within an optional date range."""
        rows = self._read_transactions()
        total_sales = total_discount = total_profit = 0.0
        count = 0
        for row in rows:
            if row.get("type") != "SALE":
                continue
            if not self._within_range(row["timestamp"], start_date, end_date):
                continue
            subtotal = float(row["subtotal"])
            discount = float(row["discount"])
            cost = float(row["cost_price"]) * float(row["tabs_count"])
            total_sales += subtotal
            total_discount += discount
            total_profit += subtotal - cost
            count += 1
        return {
            "transactions": count,
            "total_sales": round(total_sales, 2),
            "total_discount": round(total_discount, 2),
            "total_profit": round(total_profit, 2),
        }

    def top_selling(self, n=5, start_date=None, end_date=None):
        """Return up to n (medicine, brand) -> tablets-sold pairs, most sold first."""
        rows = self._read_transactions()
        totals = {}
        for row in rows:
            if row.get("type") != "SALE":
                continue
            if not self._within_range(row["timestamp"], start_date, end_date):
                continue
            key = (row["medicine"], row["brand"])
            totals[key] = totals.get(key, 0) + int(row["tabs_count"])
        ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
        return ranked[:n]

    def party_history(self, party_name, txn_type=None):
        """All transaction rows for a given customer/supplier name (case-insensitive)."""
        if not isinstance(party_name, str) or not party_name.strip():
            raise InvoiceError("Party name must be a non-empty string.")
        rows = self._read_transactions()
        target = party_name.strip().lower()
        return [r for r in rows if r.get("party", "").strip().lower() == target
                and (txn_type is None or r.get("type") == txn_type)]