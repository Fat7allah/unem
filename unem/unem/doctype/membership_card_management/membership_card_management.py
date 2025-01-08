import frappe
from frappe.model.document import Document

class MembershipCardManagement(Document):
    def validate(self):
        """
        Calculate the remaining balance before saving:
        Remaining = Payment - (Region Share + University Share)
        """
        total_shares = (self.region_share or 0) + (self.university_share or 0)
        self.remaining_balance = (self.payment or 0) - total_shares
        
        # Validate that payment is sufficient to cover shares
        if self.remaining_balance < 0:
            frappe.throw(
                "المبلغ المدفوع غير كافٍ لتغطية حصص الجهة والجامعة"
            )
