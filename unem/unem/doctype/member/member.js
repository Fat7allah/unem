// Copyright (c) 2025, UNEM and contributors
// For license information, please see license.txt

/**
 * Client-side form controller for Member DocType.
 * Handles province field validation and filtering based on selected region.
 */
frappe.ui.form.on('Member', {
    refresh: function(frm) {
        // Set RTL for Arabic interface
        $('body').attr('dir', 'rtl');
        
        // Initialize province field filtering if region exists
        if (frm.doc.region) {
            setupProvinceField(frm);
        }
    },
    
    onload: function(frm) {
        // Initialize province field filtering on form load
        if (frm.doc.region) {
            setupProvinceField(frm);
        }
    },
    
    region: function(frm) {
        // Reset and reinitialize province when region changes
        frm.set_value('province', '');
        
        if (frm.doc.region) {
            setupProvinceField(frm);
        }
    },
    
    province: function(frm) {
        validateProvince(frm);
    },
    
    profession: function(frm) {
        // Set up teaching_specialty filtering based on profession
        frm.set_query('teaching_specialty', function() {
            return {
                filters: {
                    'profession': frm.doc.profession
                }
            };
        });
        
        // Clear teaching_specialty if profession changes
        if (frm.doc.teaching_specialty) {
            frm.set_value('teaching_specialty', '');
        }
        
        // Refresh the field to ensure dependencies are re-evaluated
        frm.refresh_field('teaching_specialty');
        
        // Debug teaching_specialty visibility
        console.log('Profession changed:', {
            profession: frm.doc.profession,
            isTeaching: ['التدريس الابتدائي', 'التدريس الإعدادي', 'التدريس التأهيلي'].includes(frm.doc.profession),
            teachingSpecialty: frm.doc.teaching_specialty
        });
    }
});

/**
 * Sets up province field filtering based on selected region.
 * @param {Object} frm - The form object
 */
function setupProvinceField(frm) {
    frm.set_query('province', function() {
        return {
            filters: {
                'region': frm.doc.region
            }
        };
    });
}

/**
 * Validates that selected province belongs to selected region.
 * Clears province and shows error if validation fails.
 * @param {Object} frm - The form object
 */
function validateProvince(frm) {
    if (!frm.doc.province) return;
    
    // Ensure region is selected before province
    if (!frm.doc.region) {
        frm.set_value('province', '');
        frappe.throw(__('يجب تحديد الجهة أولاً'));
        return;
    }
    
    // Validate province belongs to selected region
    frappe.db.get_value('Province', frm.doc.province, 'region')
        .then(r => {
            if (r.message && r.message.region !== frm.doc.region) {
                frm.set_value('province', '');
                frappe.throw(__(`الإقليم المحدد لا ينتمي إلى ${frm.doc.region}`));
            }
        });
}
