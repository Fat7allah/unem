frappe.listview_settings['Region'] = {
    onload: function(listview) {
        // Set workspace for breadcrumb
        frappe.breadcrumbs.set_workspace('member-management');
    }
};
