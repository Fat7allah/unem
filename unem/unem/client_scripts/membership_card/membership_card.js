frappe.ui.form.on('Membership_Card', {
    onload: function(frm) {
        // Set workspace for breadcrumb
        frappe.breadcrumbs.set_workspace('member-management');
    },
    refresh: function(frm) {
        unem.utils.fix_breadcrumb();
    },
    setup: function(frm) {
        // Override the module to ensure correct breadcrumb
        frm.meta.module = 'member-management';
    },
    before_load: function(frm) {
        // Also set the module to ensure correct breadcrumb
        frm.doc.module = 'member-management';
    }
});
