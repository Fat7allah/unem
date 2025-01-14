frappe.ui.form.on('Province', {
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
    }
});
