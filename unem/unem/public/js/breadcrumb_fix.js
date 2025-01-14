frappe.provide('unem.utils');

unem.utils.fix_breadcrumb = function() {
    // Wait for breadcrumbs to be rendered
    setTimeout(() => {
        // Find the financial-management breadcrumb
        const breadcrumbs = document.querySelectorAll('.breadcrumb-item a');
        breadcrumbs.forEach(crumb => {
            if (crumb.textContent.includes('financial-management')) {
                // Update the text and href
                crumb.textContent = 'member-management';
                crumb.href = '/app/member-management';
            }
        });
    }, 100);
};
