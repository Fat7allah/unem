frappe.ui.form.on('Member', {
    refresh: function(frm) {
        frm.doc.module = 'member-management';
        frm.meta.module = 'member-management';
    }
});
