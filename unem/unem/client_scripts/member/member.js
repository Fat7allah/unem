frappe.ui.form.on('Member', {
    onload: function(frm) {
        // Set workspace for breadcrumb
        frappe.breadcrumbs.set_workspace('member-management');
    }
});
