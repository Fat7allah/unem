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
            setupSpecialtyField(frm);
        }
    },
    
    onload: function(frm) {
        // Initialize fields filtering on form load
        if (frm.doc.region) {
            setupProvinceField(frm);
        }
        if (frm.doc.profession) {
            setupSpecialtyField(frm);
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
        // Reset specialty when profession changes
        frm.set_value('specialty', '');
        
        if (frm.doc.profession) {
            setupSpecialtyField(frm);
        }
    },
    
    specialty: function(frm) {
        validateSpecialty(frm);
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
 * Sets up specialty field filtering based on selected profession.
 * @param {Object} frm - The form object
 */
function setupSpecialtyField(frm) {
    if (['التدريس الابتدائي', 'التدريس الإعدادي', 'التدريس التأهيلي'].includes(frm.doc.profession)) {
        frm.set_query('specialty', function() {
            return {
                filters: {
                    'profession': frm.doc.profession
                }
            };
        });
    }
}

/**
 * Validates that selected province belongs to selected region.
 * Clears province and shows error if validation fails.
 * @param {Object} frm - The form object
 */
function validateProvince(frm) {
    if (frm.doc.province && frm.doc.region) {
        frappe.db.get_value('Province', frm.doc.province, 'region')
            .then(r => {
                if (r.message && r.message.region !== frm.doc.region) {
                    frm.set_value('province', '');
                    frappe.throw(__('Selected province does not belong to the selected region'));
                }
            });
    }
}

/**
 * Validates that selected specialty belongs to selected profession.
 * Clears specialty and shows error if validation fails.
 * @param {Object} frm - The form object
 */
function validateSpecialty(frm) {
    if (frm.doc.specialty && frm.doc.profession) {
        frappe.db.get_value('Specialty', frm.doc.specialty, 'profession')
            .then(r => {
                if (r.message && r.message.profession !== frm.doc.profession) {
                    frm.set_value('specialty', '');
                    frappe.throw(__('Selected specialty does not belong to the selected profession'));
                }
            });
    }
}
