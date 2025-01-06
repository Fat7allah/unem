frappe.ui.form.on('Member', {
    refresh: function(frm) {
        // Add custom buttons
        frm.add_custom_button(__('إصدار بطاقة العضوية'), function() {
            create_membership_card(frm);
        }, __('إجراءات'));

        // Set RTL for Arabic
        $('body').attr('dir', 'rtl');
    },

    validate: function(frm) {
        // Custom client-side validations
        if (frm.doc.email && !validate_email(frm.doc.email)) {
            frappe.msgprint(__('عنوان البريد الإلكتروني غير صالح'));
            frappe.validated = false;
        }
    },

    profession: function(frm) {
        // Handle teaching specialty visibility
        const teaching_professions = ['التدريس الابتدائي', 'الإعدادي', 'التأهيلي'];
        if (teaching_professions.includes(frm.doc.profession)) {
            frm.set_df_property('teaching_specialty', 'hidden', 0);
            frm.set_df_property('teaching_specialty', 'reqd', 1);
        } else {
            frm.set_df_property('teaching_specialty', 'hidden', 1);
            frm.set_df_property('teaching_specialty', 'reqd', 0);
            frm.set_value('teaching_specialty', '');
        }
    },

    setup: function(frm) {
        // Set up filters and defaults
        frm.set_query('institution', function() {
            return {
                filters: {
                    'province': frm.doc.province
                }
            };
        });
    }
});

// Helper function to create membership card
function create_membership_card(frm) {
    frappe.call({
        method: 'unem.unem.doctype.member.member.create_membership_card',
        args: {
            'member': frm.doc.name
        },
        callback: function(r) {
            if (!r.exc) {
                frappe.msgprint(__('تم إنشاء بطاقة العضوية بنجاح'));
                frm.reload_doc();
            }
        }
    });
}

// Helper function to validate email
function validate_email(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
