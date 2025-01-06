// Copyright (c) 2025, UNEM and contributors
// For license information, please see license.txt

frappe.ui.form.on('UNEM_Structure', {
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
    },
    
    position_type: function(frm) {
        // Clear role when position type changes
        frm.set_value('role', '');
        
        // Set role options based on position type
        if (frm.doc.position_type === 'المكتب التنفيذي') {
            frm.set_df_property('role', 'options', [
                'الكاتب الوطني',
                'نائب الكاتب الوطني',
                'الكاتب العام',
                'نائب الكاتب العام',
                'أمين المال',
                'نائب أمين المال',
                'مستشار',
                'مكلف بمهمة'
            ].join('\n'));
        } else {
            frm.set_df_property('role', 'options', [
                'الكاتب العام',
                'نائب الكاتب العام',
                'أمين المال',
                'نائب أمين المال',
                'مستشار'
            ].join('\n'));
        }
    }
});
