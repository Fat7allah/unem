frappe.ui.form.on('Mutual_Structure', {
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
    },
    before_load: function(frm) {
        // Override the workspace route for this doctype
        if (!frappe.workspaces) frappe.workspaces = {};
        if (!frappe.workspaces.doctypes) frappe.workspaces.doctypes = {};
        frappe.workspaces.doctypes[frm.doctype] = 'member-management';
    }
});
