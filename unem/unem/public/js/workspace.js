frappe.provide('frappe.workspaces');

$(document).on('app_ready', function() {
    // List of doctypes that should be in the member management workspace
    const member_management_doctypes = [
        'Member',
        'Membership_Card',
        'Membership_Card_Management',
        'UNEM_Structure',
        'Mutual_Structure',
        'Region',
        'Province'
    ];

    // Override the workspace route for these doctypes
    member_management_doctypes.forEach(doctype => {
        frappe.router.doctype_layout[doctype] = 'member-management';
    });

    // Override the get_breadcrumbs method
    const original_get_breadcrumbs = frappe.breadcrumbs.get_breadcrumbs;
    frappe.breadcrumbs.get_breadcrumbs = function() {
        let breadcrumbs = original_get_breadcrumbs();
        const route = frappe.get_route();
        
        if (route[0] === 'Form' && member_management_doctypes.includes(route[1])) {
            // Find the workspace breadcrumb and update it
            breadcrumbs = breadcrumbs.map(crumb => {
                if (crumb.label === 'financial-management') {
                    return {
                        ...crumb,
                        label: 'member-management',
                        route: '/app/member-management'
                    };
                }
                return crumb;
            });
        }
        
        return breadcrumbs;
    };
});
