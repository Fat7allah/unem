frappe.ui.form.on('UNEM_Structure', {
    refresh: function(frm) {
        frm.doc.module = 'member-management';
        frm.meta.module = 'member-management';
    }
});
