frappe.listview_settings['Mutual_Structure'] = {
    onload: function(listview) {
        // Set workspace for breadcrumb
        frappe.breadcrumbs.set_workspace('member-management');
    }
};
