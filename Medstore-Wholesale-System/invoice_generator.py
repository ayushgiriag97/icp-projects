# =============================================
#   CLASS 3: InvoiceGenerator
# =============================================

import os
import datetime
import uuid

class InvoiceError(Exception):
    """Custom exception for invoice generation errors."""
    pass

class InvoiceGenerator:

    def __init__(self, log_file="audit_log.txt"):
        self.log_file = log_file

    def log_action(self, action_type, identifier, filename):
        """Log invoice/restock creation for audit purposes."""
        try:
            with open(self.log_file, "a", encoding="utf-8") as log:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log.write(f"{timestamp} | {action_type} | {identifier} | {filename}\n")
        except Exception as e:
            # Don’t block invoice creation if logging fails
            print(f"[Warning] Audit log failed: {str(e)}")

    def unique_name(self, prefix, identifier):
        if not isinstance(prefix, str) or not prefix.strip():
            raise InvoiceError("Prefix must be a non-empty string.")
        if not isinstance(identifier, str) or not identifier.strip():
            raise InvoiceError("Identifier must be a non-empty string.")

        safe_identifier = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in identifier.strip())
        base = prefix.strip() + "_" + safe_identifier
        filename = base + ".txt"
        counter = 1

        while os.path.exists(filename):
            filename = f"{base}_{counter}.txt"
            counter += 1

        return filename

    def _format_lines(self, lines):
        """Format invoice/restock lines into neat columns."""
        formatted = ""
        for line in lines:
            if not isinstance(line, str) or not line.strip():
                raise InvoiceError("Line must be a non-empty string.")
            parts = line.split("|")
            formatted += "".join(part.strip().ljust(20) for part in parts) + "\n"
        return formatted

    def make_sale_invoice(self, customer, invoice_lines, total):
        if not isinstance(customer, str) or not customer.strip():
            raise InvoiceError("Customer name must be a non-empty string.")
        if not isinstance(invoice_lines, list) or not invoice_lines:
            raise InvoiceError("Invoice lines must be a non-empty list.")
        if not isinstance(total, (int, float)) or total < 0:
            raise InvoiceError("Total must be a non-negative number.")

        invoice_id = str(uuid.uuid4())[:8]
        date_str = datetime.datetime.now().strftime("%d-%b-%Y %H:%M")

        content = (
            "============================\n"
            "   MEDSTORE PVT. LTD.\n"
            "   SALES INVOICE\n"
            "============================\n"
            f"Invoice ID : {invoice_id}\n"
            f"Date       : {date_str}\n"
            f"Customer   : {customer.strip()}\n"
            "----------------------------\n"
        )

        content += self._format_lines(invoice_lines)
        content += "----------------------------\n"
        content += f"TOTAL : Rs.{round(total, 2)}\n"
        content += "============================\n"

        self.log_action("SALE_INVOICE", customer, f"invoice_{customer}.txt")
        return content

    def make_restock_note(self, supplier, note_lines, total):
        if not isinstance(supplier, str) or not supplier.strip():
            raise InvoiceError("Supplier name must be a non-empty string.")
        if not isinstance(note_lines, list) or not note_lines:
            raise InvoiceError("Note lines must be a non-empty list.")
        if not isinstance(total, (int, float)) or total < 0:
            raise InvoiceError("Total must be a non-negative number.")

        note_id = str(uuid.uuid4())[:8]
        date_str = datetime.datetime.now().strftime("%d-%b-%Y %H:%M")

        content = (
            "============================\n"
            "   MEDSTORE PVT. LTD.\n"
            "   RESTOCK NOTE\n"
            "============================\n"
            f"Note ID   : {note_id}\n"
            f"Date      : {date_str}\n"
            f"Supplier  : {supplier.strip()}\n"
            "----------------------------\n"
        )

        content += self._format_lines(note_lines)
        content += "----------------------------\n"
        content += f"TOTAL : Rs.{round(total, 2)}\n"
        content += "============================\n"

        self.log_action("RESTOCK_NOTE", supplier, f"restock_{supplier}.txt")
        return content
