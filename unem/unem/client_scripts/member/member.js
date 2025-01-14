frappe.ui.form.on('Member', {
    onload: function(frm) {
        unem.utils.fix_breadcrumb();
    },
    refresh: function(frm) {
        unem.utils.fix_breadcrumb();
    }
});
