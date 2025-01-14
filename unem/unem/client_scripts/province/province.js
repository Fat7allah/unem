frappe.ui.form.on('Province', {
    onload: function(frm) {
        unem.utils.fix_breadcrumb();
    },
    refresh: function(frm) {
        unem.utils.fix_breadcrumb();
    }
});
