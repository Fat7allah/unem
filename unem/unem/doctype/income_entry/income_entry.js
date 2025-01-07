// Copyright (c) 2025, UNEM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Income_Entry', {
    refresh: function(frm) {
        // Set RTL for Arabic
        $('body').attr('dir', 'rtl');
        
        // Add custom buttons
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__('طباعة الإيصال'), function() {
                frappe.route_options = {
                    "name": frm.doc.name
                };
                frappe.set_route("Form", "Income_Entry", "receipt");
            });
        }
    },
    
    setup: function(frm) {
        // Set query for academic year field to show only active years
        frm.set_query('academic_year', function() {
            return {
                filters: {
                    'is_active': 1
                }
            };
        });
    },
    
    validate: function(frm) {
        // Validate amount
        if (frm.doc.amount <= 0) {
            frappe.msgprint(__("المبلغ يجب أن يكون أكبر من صفر"));
            frappe.validated = false;
        }
        
        // Validate date within academic year
        if (frm.doc.date && frm.doc.academic_year) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Academic Year',
                    name: frm.doc.academic_year
                },
                callback: function(r) {
                    if (r.message) {
                        let start_date = r.message.start_date;
                        let end_date = r.message.end_date;
                        let entry_date = frappe.datetime.str_to_obj(frm.doc.date);
                        
                        if (entry_date < frappe.datetime.str_to_obj(start_date) ||
                            entry_date > frappe.datetime.str_to_obj(end_date)) {
                            frappe.msgprint(__("التاريخ يجب أن يكون ضمن السنة الدراسية المحددة"));
                            frappe.validated = false;
                        }
                    }
                }
            });
        }
    },
    
    type: function(frm) {
        // Handle type change
        if (frm.doc.type === 'بطاقة الإنخراط') {
            frm.set_value('amount', 100); // Set default amount for membership card
        } else {
            frm.set_value('amount', ''); // Clear amount for other types
        }
    }
});
