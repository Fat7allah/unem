from frappe import _

def get_data():
	return [
		{
			"module_name": "UNEM",
			"color": "grey",
			"icon": "octicon octicon-organization",
			"type": "module",
			"label": _("UNEM")
		},
		{
			"module_name": "Member Management",
			"color": "blue",
			"icon": "octicon octicon-organization",
			"type": "module",
			"label": _("إدارة الأعضاء")
		},
		{
			"module_name": "Financial Management",
			"color": "green",
			"icon": "octicon octicon-graph",
			"type": "module",
			"label": _("الإدارة المالية")
		}
	]
