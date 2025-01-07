// Copyright (c) 2025, UNEM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mutual_Structure', {
    refresh: function(frm) {
        // Set RTL for Arabic
        $('body').attr('dir', 'rtl');
    },
    
    validate: function(frm) {
        // Validate role requirements
        if (frm.doc.position_type === "المكتب التنفيذي" && !frm.doc.role) {
            frappe.msgprint(__("يجب تحديد المنصب للأعضاء في المكتب التنفيذي"));
            frappe.validated = false;
        }
    },
    
    position_type: function(frm) {
        // Clear role when position type changes
        frm.set_value('role', '');
        
        // Show/hide role field based on position type
        if (frm.doc.position_type === 'المكتب التنفيذي') {
            frm.set_df_property('role', 'hidden', 0);
            frm.set_df_property('role', 'reqd', 1);
        } else {
            frm.set_df_property('role', 'hidden', 1);
            frm.set_df_property('role', 'reqd', 0);
        }
    },
    
    setup: function(frm) {
        // Set query for member link field
        frm.set_query('member', function() {
            return {
                query: 'unem.unem.doctype.member.member.get_active_members'
            };
        });
    }
});
