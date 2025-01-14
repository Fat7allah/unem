frappe.ui.form.on('Membership_Card_Management', {
    refresh: function(frm) {
        frm.doc.module = 'member-management';
        frm.meta.module = 'member-management';
    }
});
