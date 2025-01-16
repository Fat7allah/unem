import frappe
import json
import os

def after_install():
    """Install initial data after app installation"""
    try:
        # Install professions
        install_professions()
        
        # Install teaching specialties
        install_teaching_specialties()
        
        # Commit changes
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(str(e), "Data Installation Error")

def install_professions():
    """Install profession data"""
    fixture_path = os.path.join(frappe.get_app_path('unem'), 'unem', 'fixtures', 'profession.json')
    
    with open(fixture_path, 'r', encoding='utf-8') as f:
        professions = json.load(f)
        
    for profession in professions:
        if not frappe.db.exists('Profession', profession['name']):
            doc = frappe.get_doc({
                'doctype': 'Profession',
                'profession_name': profession['profession_name'],
                'name': profession['name']
            })
            doc.insert(ignore_permissions=True)

def install_teaching_specialties():
    """Install teaching specialty data"""
    fixture_path = os.path.join(frappe.get_app_path('unem'), 'unem', 'fixtures', 'teaching_specialty.json')
    
    with open(fixture_path, 'r', encoding='utf-8') as f:
        specialties = json.load(f)
        
    for specialty in specialties:
        if not frappe.db.exists('Teaching Specialty', specialty['name']):
            doc = frappe.get_doc({
                'doctype': 'Teaching Specialty',
                'specialty_name': specialty['specialty_name'],
                'name': specialty['name'],
                'profession': specialty['profession']
            })
            doc.insert(ignore_permissions=True)
