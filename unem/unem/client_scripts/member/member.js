frappe.ui.form.on('Member', {
    refresh: function(frm) {
        frm.doc.module = 'member-management';
        frm.meta.module = 'member-management';
        
        // Initialize teaching specialty filtering if profession exists
        if (frm.doc.profession) {
            setupTeachingSpecialtyField(frm);
        }
    },
    
    onload: function(frm) {
        // Initialize teaching specialty filtering on form load
        if (frm.doc.profession) {
            setupTeachingSpecialtyField(frm);
        }
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
 * Validates that selected teaching specialty belongs to selected profession.
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
