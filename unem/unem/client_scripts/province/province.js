frappe.ui.form.on('Province', {
    onload: function(frm) {
        // Set workspace for breadcrumb
        frappe.breadcrumbs.set_workspace('member-management');
    }
});
