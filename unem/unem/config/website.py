from __future__ import unicode_literals
import frappe

def get_context(context):
    context.brand_html = 'UNEM'
    context.home_page = 'unem'
    return context
