frappe.provide('frappe.workspaces');
frappe.provide('frappe.workspaces.doctypes');

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

    // Set up workspace routes for all member management doctypes
    member_management_doctypes.forEach(doctype => {
        frappe.workspaces.doctypes[doctype] = 'member-management';
    });
});
