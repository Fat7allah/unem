from frappe import _

def get_data():
    return [
        {
            "label": _("Members"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Member",
                    "description": _("Member records")
                },
                {
                    "type": "doctype",
                    "name": "Membership_Card",
                    "description": _("Membership Cards")
                }
            ]
        },
        {
            "label": _("Structure"),
            "items": [
                {
                    "type": "doctype",
                    "name": "UNEM_Structure",
                    "description": _("UNEM Organizational Structure")
                },
                {
                    "type": "doctype",
                    "name": "Mutual_Structure",
                    "description": _("Mutual Organization Structure")
                }
            ]
        },
        {
            "label": _("Finance"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Income_Entry",
                    "description": _("Income Records")
                },
                {
                    "type": "doctype",
                    "name": "Expense_Entry",
                    "description": _("Expense Records")
                }
            ]
        }
    ]
