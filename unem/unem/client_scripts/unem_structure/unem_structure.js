frappe.ui.form.on('UNEM_Structure', {
    onload: function(frm) {
        unem.utils.fix_breadcrumb();
    },
    refresh: function(frm) {
        unem.utils.fix_breadcrumb();
    },
    setup: function(frm) {
        // Override the module to ensure correct breadcrumb
        frm.meta.module = 'member-management';
        
        // Force a breadcrumb update
        frappe.breadcrumbs.clear_breadcrumbs();
        frappe.breadcrumbs.add(frm.meta.module, frm.doctype);
    }
});
