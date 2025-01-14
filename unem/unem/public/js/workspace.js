frappe.provide('frappe.workspaces');

// Override the original get_breadcrumbs method
const original_get_breadcrumbs = frappe.breadcrumbs.get_breadcrumbs;
frappe.breadcrumbs.get_breadcrumbs = function() {
    let breadcrumbs = original_get_breadcrumbs();
    
    // Check if we're in a doctype under member management
    const member_management_doctypes = [
        'Member',
        'Membership_Card',
        'Membership_Card_Management',
        'UNEM_Structure',
        'Mutual_Structure',
        'Region',
        'Province'
    ];
    
    const route = frappe.get_route();
    if (route[0] === 'Form' && member_management_doctypes.includes(route[1])) {
        // Replace any financial-management with member-management in breadcrumbs
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
