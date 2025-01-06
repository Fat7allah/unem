app_name = "unem"
app_title = "UNEM"
app_publisher = "UNEM"
app_description = "Union Nationale de l'Enseignement au Maroc Management System"
app_email = "admin@unem.ma"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/unem/css/unem.css"
app_include_js = "/assets/unem/js/unem.js"

# include js, css files in header of web template
web_include_css = "/assets/unem/css/unem_web.css"
web_include_js = "/assets/unem/js/unem_web.js"

# Website
# -------
website_route_rules = [
    {"from_route": "/members", "to_route": "Member"},
    {"from_route": "/members/<path:name>", "to_route": "members",
        "defaults": {
            "doctype": "Member",
            "parents": [{"label": "Members", "route": "members"}]
        }
    }
]

# Portal Menu Items
portal_menu_items = [
    {"title": "My Membership", "route": "/my-membership", "reference_doctype": "Member"}
]

# Document Events
doc_events = {
    "Member": {
        "after_insert": "unem.unem.doctype.member.member.after_member_insert",
        "on_update": "unem.unem.doctype.member.member.on_member_update"
    }
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "unem.tasks.daily",
    ],
    "monthly": [
        "unem.tasks.monthly"
    ]
}

# Translation
translation_domains = ['unem']
supported_languages = ["ar", "fr"]

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
