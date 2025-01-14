frappe.ui.form.on('Province', {
    setup: function(frm) {
        // Override the module to ensure correct breadcrumb
        frm.meta.module = 'member-management';
        
        // Force a breadcrumb update
        frappe.breadcrumbs.clear_breadcrumbs();
        frappe.breadcrumbs.add(frm.meta.module, frm.doctype);
    }
});
