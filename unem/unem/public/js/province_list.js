frappe.listview_settings['Province'] = {
    onload: function(listview) {
        // Set workspace for breadcrumb
        frappe.breadcrumbs.set_workspace('member-management');
    }
};
