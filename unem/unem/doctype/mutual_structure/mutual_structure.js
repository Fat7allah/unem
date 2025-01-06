// Copyright (c) 2025, UNEM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mutual_Structure', {
    refresh: function(frm) {
        // Set RTL for Arabic
        $('body').attr('dir', 'rtl');
    },
    
    validate: function(frm) {
        // Validate member has active membership
        if (frm.doc.member) {
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Membership_Card',
                    filters: {
                        'member': frm.doc.member,
                        'card_status': 'المؤداة',
                        'expiry_date': ['>', frappe.datetime.get_today()]
                    },
                    limit_page_length: 1
                },
                callback: function(r) {
                    if (!r.message || r.message.length === 0) {
                        frappe.msgprint(__("يجب أن يكون العضو لديه بطاقة عضوية سارية المفعول"));
                        frappe.validated = false;
                    }
                }
            });
        }
        
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
        // Set query filters for member link field
        frm.set_query('member', function() {
            return {
                filters: {
                    'name': ['in', function() {
                        return frappe.db.get_list('Membership_Card', {
                            filters: {
                                'card_status': 'المؤداة',
                                'expiry_date': ['>', frappe.datetime.get_today()]
                            },
                            fields: ['member']
                        }).then(r => r.map(d => d.member));
                    }]
                }
            };
        });
    }
});
