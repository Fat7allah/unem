frappe.ui.form.on('Province', {
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
        
        // Also set the module to ensure correct breadcrumb
        frm.doc.module = 'member-management';
    }
});
