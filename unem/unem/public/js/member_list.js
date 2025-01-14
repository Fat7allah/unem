frappe.listview_settings['Member'] = {
    onload: function(listview) {
        // Set workspace for breadcrumb
        frappe.breadcrumbs.set_workspace('member-management');
    }
};
