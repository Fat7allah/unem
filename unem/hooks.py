app_name = "unem"
app_title = "UNEM"
app_publisher = "UNEM"
app_description = "Union Nationale de l'Enseignement au Maroc Management System"
app_email = "admin@unem.ma"
app_license = "MIT"

# Document Events
doc_events = {
    "Member": {
        "after_insert": "unem.unem.doctype.member.member.after_member_insert",
        "on_update": "unem.unem.doctype.member.member.on_member_update"
    }
}

# Fixtures
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            ["dt", "in", (
                "Member",
                "Membership_Card",
                "UNEM_Structure",
                "Mutual_Structure",
                "Income_Entry",
                "Expense_Entry"
            )]
        ]
    },
    {
        "doctype": "Property Setter",
        "filters": [
            ["doc_type", "in", (
                "Member",
                "Membership_Card",
                "UNEM_Structure",
                "Mutual_Structure",
                "Income_Entry",
                "Expense_Entry"
            )]
        ]
    }
]

# Translation
translation_domains = ['unem']

# Supported Languages
supported_languages = ["ar", "fr"]
