frappe.listview_settings['Membership_Card'] = {
    onload: function(listview) {
        // Set workspace for breadcrumb
        frappe.breadcrumbs.set_workspace('member-management');
    }
};
