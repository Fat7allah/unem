frappe.ready(function() {
    // Setup RTL for Arabic
    if (frappe.boot && frappe.boot.lang === 'ar') {
        $('body').attr('dir', 'rtl');
    }
    
    // Setup membership card view
    setup_membership_view();
    
    // Setup profile updates
    setup_profile_updates();
});

function setup_membership_view() {
    if($('.membership-status').length) {
        frappe.call({
            method: 'unem.api.get_member_details',
            args: {
                member_id: frappe.user_id
            },
            callback: function(r) {
                if(r.message) {
                    update_membership_display(r.message);
                }
            }
        });
    }
}

function setup_profile_updates() {
    $('.update-profile-btn').on('click', function() {
        frappe.call({
            method: 'unem.api.update_member_profile',
            args: {
                member_id: frappe.user_id,
                data: get_form_data()
            },
            callback: function(r) {
                if(r.message) {
                    frappe.show_alert({
                        message: __('Profile updated successfully'),
                        indicator: 'green'
                    });
                }
            }
        });
    });
}

function update_membership_display(data) {
    const membership = data.membership;
    if (membership) {
        $('.membership-status').html(`
            <div class="membership-card">
                <h3>${__("Membership Status")}</h3>
                <p>${__("Card Number")}: ${membership.name}</p>
                <p>${__("Valid Until")}: ${membership.expiry_date}</p>
                <p>${__("Status")}: ${membership.card_status}</p>
            </div>
        `);
    }
}

function get_form_data() {
    return {
        phone: $('#phone').val(),
        email: $('#email').val()
    };
}
