frappe.ui.form.on('Mutual_Structure', {
    refresh: function(frm) {
        frm.doc.module = 'member-management';
        frm.meta.module = 'member-management';
    }
});
