frappe.ui.form.on('Membership_Card_Management', {
    onload: function(frm) {
        unem.utils.fix_breadcrumb();
    },
    refresh: function(frm) {
        unem.utils.fix_breadcrumb();
    }
});
