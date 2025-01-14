frappe.ui.form.on('Membership_Card_Management', {
    onload: function(frm) {
        // Set the workspace for breadcrumb
        if (!frappe.workspaces) frappe.workspaces = {};
        frappe.workspaces.current = 'member-management';
        
        // Force a breadcrumb update
        frappe.breadcrumbs.clear_breadcrumbs();
        frappe.breadcrumbs.add(frm.meta.module, frm.doctype);
        
        // Update the route
        let route = frappe.get_route();
        if (route[0] === 'Form' && route[1] === frm.doctype) {
            frappe.set_route('member-management', route[1], route[2]);
        }
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
        
        // Also set the module to ensure correct breadcrumb
        frm.doc.module = 'member-management';
    }
});
