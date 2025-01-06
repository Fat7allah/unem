// Copyright (c) 2025, UNEM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expense_Entry', {
    refresh: function(frm) {
        // Set RTL for Arabic
        $('body').attr('dir', 'rtl');
        
        // Add custom buttons
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__('طباعة الإيصال'), function() {
                frappe.route_options = {
                    "name": frm.doc.name
                };
                frappe.set_route("Form", "Expense_Entry", "receipt");
            });
        }
    },
    
    validate: function(frm) {
        // Validate amount
        if (frm.doc.amount <= 0) {
            frappe.msgprint(__("المبلغ يجب أن يكون أكبر من صفر"));
            frappe.validated = false;
        }
        
        // Validate attachments for large amounts
        if (frm.doc.amount > 1000 && !frm.doc.attachments) {
            frappe.msgprint(__("المرفقات مطلوبة للمصاريف التي تتجاوز 1000 درهم"));
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
    
    setup: function(frm) {
        // Set query filters for academic year
        frm.set_query('academic_year', function() {
            return {
                filters: {
                    'status': 'Active'
                }
            };
        });
    },
    
    amount: function(frm) {
        // Show warning for large amounts
        if (frm.doc.amount > 1000) {
            frappe.show_alert({
                message: __("تذكير: المرفقات مطلوبة للمصاريف التي تتجاوز 1000 درهم"),
                indicator: 'orange'
            }, 5);
        }
    }
});
