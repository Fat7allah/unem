import frappe
from frappe import _

def get_context(context):
    """Add members list data to the context"""
    try:
        # Get filters from query parameters
        filters = {
            'name': frappe.form_dict.get('name'),
            'status': frappe.form_dict.get('status'),
            'region': frappe.form_dict.get('region')
        }
        
        # Get pagination parameters
        page = int(frappe.form_dict.get('page', 1))
        page_size = 20
        start = (page - 1) * page_size
        
        # Get members list
        members = get_members_list(filters, start, page_size)
        total_members = get_total_members(filters)
        
        # Calculate pagination
        total_pages = (total_members + page_size - 1) // page_size
        pages = get_pagination_info(page, total_pages)
        
        # Add data to context
        context.members = members
        context.regions = get_regions_list()
        context.show_pagination = total_pages > 1
        context.pages = pages
        context.prev_page = f'/members?page={page-1}' if page > 1 else None
        context.next_page = f'/members?page={page+1}' if page < total_pages else None
        
        return context
        
    except Exception as e:
        frappe.log_error(f"Error in members list: {str(e)}")
        context.error = _("Error loading members list")
        return context

def get_members_list(filters, start=0, page_size=20):
    """Get filtered list of members"""
    conditions = []
    values = {}
    
    if filters.get('name'):
        conditions.append("(m.first_name LIKE %(name)s OR m.last_name LIKE %(name)s)")
        values['name'] = f"%{filters['name']}%"
    
    if filters.get('status'):
        conditions.append("m.status = %(status)s")
        values['status'] = filters['status']
    
    if filters.get('region'):
        conditions.append("m.region = %(region)s")
        values['region'] = filters['region']
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = f"""
        SELECT 
            m.name,
            m.member_id,
            m.first_name,
            m.last_name,
            CONCAT(m.first_name, ' ', m.last_name) as full_name,
            m.region,
            m.status,
            m.join_date,
            m.image
        FROM 
            `tabUNEM Member` m
        WHERE 
            {where_clause}
        ORDER BY 
            m.creation DESC
        LIMIT 
            {start}, {page_size}
    """
    
    members = frappe.db.sql(query, values=values, as_dict=1)
    return members

def get_total_members(filters):
    """Get total number of members with applied filters"""
    conditions = []
    values = {}
    
    if filters.get('name'):
        conditions.append("(first_name LIKE %(name)s OR last_name LIKE %(name)s)")
        values['name'] = f"%{filters['name']}%"
    
    if filters.get('status'):
        conditions.append("status = %(status)s")
        values['status'] = filters['status']
    
    if filters.get('region'):
        conditions.append("region = %(region)s")
        values['region'] = filters['region']
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    return frappe.db.sql(
        f"SELECT COUNT(*) FROM `tabUNEM Member` WHERE {where_clause}",
        values=values
    )[0][0]

def get_regions_list():
    """Get list of unique regions"""
    regions = frappe.db.sql("""
        SELECT DISTINCT region 
        FROM `tabUNEM Member` 
        WHERE region IS NOT NULL 
        ORDER BY region
    """)
    return [r[0] for r in regions]

def get_pagination_info(current_page, total_pages):
    """Generate pagination information"""
    pages = []
    
    # Always show first page, last page, current page, and one page before and after current page
    show_pages = {1, total_pages, current_page, current_page - 1, current_page + 1}
    show_pages = {p for p in show_pages if p > 0 and p <= total_pages}
    
    for page in sorted(show_pages):
        if pages and page - pages[-1]['number'] > 1:
            # Add ellipsis if there's a gap
            pages.append({'number': '...', 'url': '#', 'active': False})
        pages.append({
            'number': page,
            'url': f'/members?page={page}',
            'active': page == current_page
        })
    
    return pages
