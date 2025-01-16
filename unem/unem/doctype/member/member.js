// Copyright (c) 2025, UNEM and contributors
// For license information, please see license.txt

/**
 * Client-side form controller for Member DocType.
 * Handles field validation and filtering.
 */
frappe.ui.form.on('Member', {
    refresh: function(frm) {
        // Set RTL for Arabic interface
        $('body').attr('dir', 'rtl');
        
        // Initialize fields filtering
        if (frm.doc.region) {
            setupProvinceField(frm);
        }
        if (frm.doc.profession) {
            setupTeachingSpecialtyField(frm);
        }
    },
    
    onload: function(frm) {
        // Initialize fields filtering on form load
        if (frm.doc.region) {
            setupProvinceField(frm);
        }
        if (frm.doc.profession) {
            setupTeachingSpecialtyField(frm);
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
        // Reset and reinitialize teaching_specialty when profession changes
        frm.set_value('teaching_specialty', '');
        
        if (frm.doc.profession) {
            setupTeachingSpecialtyField(frm);
        }
    },
    
    teaching_specialty: function(frm) {
        validateTeachingSpecialty(frm);
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
 * Sets up teaching_specialty field filtering based on selected profession.
 * @param {Object} frm - The form object
 */
function setupTeachingSpecialtyField(frm) {
    frm.set_query('teaching_specialty', function() {
        return {
            filters: {
                'profession': frm.doc.profession
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

/**
 * Validates that selected teaching specialty belongs to selected profession.
 * Clears teaching_specialty and shows error if validation fails.
 * @param {Object} frm - The form object
 */
function validateTeachingSpecialty(frm) {
    if (!frm.doc.teaching_specialty) return;
    
    // Ensure profession is selected before teaching_specialty
    if (!frm.doc.profession) {
        frm.set_value('teaching_specialty', '');
        frappe.throw(__('يجب تحديد المهنة أولاً'));
        return;
    }
    
    // Validate teaching_specialty belongs to selected profession
    frappe.db.get_value('Teaching Specialty', frm.doc.teaching_specialty, 'profession')
        .then(r => {
            if (r.message && r.message.profession !== frm.doc.profession) {
                frm.set_value('teaching_specialty', '');
                frappe.throw(__(`التخصص المحدد لا ينتمي إلى ${frm.doc.profession}`));
            }
        });
}
