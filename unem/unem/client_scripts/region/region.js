frappe.ui.form.on('Region', {
    refresh: function(frm) {
        frm.doc.module = 'member-management';
        frm.meta.module = 'member-management';
    }
});
