frappe.provide('unem');

unem = {
    init: function() {
        // Set RTL for Arabic
        if (frappe.boot.lang === 'ar') {
            $('body').attr('dir', 'rtl');
        }
    },
    
    setup_filters: function() {
        // Common filter setup for list views
        frappe.listview_settings['Member'] = {
            add_fields: ['name', 'email', 'phone', 'province'],
            get_indicator: function(doc) {
                // Return indicator color based on status
                return [__("Active"), "green", "status,=,Active"];
            }
        };
    },
    
    setup_dashboards: function() {
        // Setup custom dashboards
        frappe.dashboards.chart_sources["Members by Province"] = {
            method: "unem.api.get_members_by_province"
        };
    }
};

// Initialize on page load
$(document).ready(function() {
    unem.init();
    unem.setup_filters();
    unem.setup_dashboards();
});
