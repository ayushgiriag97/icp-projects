# =============================================
#   CLASS 3: InvoiceGenerator
# =============================================

import os

class InvoiceGenerator:

    def unique_name(self, prefix, identifier):
        if not isinstance(prefix, str) or prefix.strip() == "":
            raise ValueError("Prefix must be a non-empty string.")

        if not isinstance(identifier, str) or identifier.strip() == "":
            raise ValueError("Identifier must be a non-empty string.")

        base = prefix.strip() + "_" + identifier.strip().replace(" ", "_")
        filename = base + ".txt"
        counter = 1

        try:
            while os.path.exists(filename):
                filename = base + "_" + str(counter) + ".txt"
                counter += 1
        except Exception as e:
            raise Exception("Error while checking file existence: " + str(e))

        return filename


    def make_sale_invoice(self, customer, invoice_lines, total):

        if not isinstance(customer, str) or customer.strip() == "":
            raise ValueError("Customer name must be a non-empty string.")

        if not isinstance(invoice_lines, list):
            raise ValueError("Invoice lines must be a list.")

        if not (isinstance(total, int) or isinstance(total, float)) or total < 0:
            raise ValueError("Total must be a non-negative number.")

        content = ""
        content += "============================\n"
        content += "   MEDSTORE PVT. LTD.\n"
        content += "   SALES INVOICE\n"
        content += "============================\n"
        content += "Customer : " + customer.strip() + "\n"
        content += "----------------------------\n"

        for line in invoice_lines:
            if not isinstance(line, str):
                raise ValueError("Invoice line must be a string.")
            content += line + "\n"

        content += "----------------------------\n"
        content += "TOTAL : Rs." + str(round(total, 2)) + "\n"
        content += "============================\n"

        return content


    def make_restock_note(self, supplier, note_lines, total):

        if not isinstance(supplier, str) or supplier.strip() == "":
            raise ValueError("Supplier name must be a non-empty string.")

        if not isinstance(note_lines, list):
            raise ValueError("Note lines must be a list.")

        if not (isinstance(total, int) or isinstance(total, float)) or total < 0:
            raise ValueError("Total must be a non-negative number.")

        content = ""
        content += "============================\n"
        content += "   MEDSTORE PVT. LTD.\n"
        content += "   RESTOCK NOTE\n"
        content += "============================\n"
        content += "Supplier : " + supplier.strip() + "\n"
        content += "----------------------------\n"

        for line in note_lines:
            if not isinstance(line, str):
                raise ValueError("Note line must be a string.")
            content += line + "\n"

        content += "----------------------------\n"
        content += "TOTAL : Rs." + str(round(total, 2)) + "\n"
        content += "============================\n"

        return content