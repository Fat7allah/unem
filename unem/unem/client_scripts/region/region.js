frappe.ui.form.on('Region', {
    onload: function(frm) {
        // Set workspace for breadcrumb
        frappe.breadcrumbs.set_workspace('member-management');
    }
});
