import frappe
from frappe.model.naming import make_autoname
from frappe.utils import getdate

def autoname_sales_invoice(doc, method=None):
    if doc.get('invoice_series'):
        doc.naming_series = '{}/.FY./.###'.format(doc.invoice_series)

    doc.name = make_autoname(doc.naming_series, 'Sales Invoice', doc)

def after_insert_customer(doc, method=None):
    frappe.enqueue("jmkfood.utils.customer_pricing", {'docname': doc.name}, queue='default')

def customer_pricing(docname):
    item_price_list = frappe.get_all('Item Price', filters={'selling': 1, 'customer': ''})
    for item in item_price_list:
        price = frappe.get_doc('Item Price', item.name)
        new_doc = frappe.copy_doc(price)
        new_doc.name = None
        new_doc.customer = docname
        new_doc.valid_from = getdate()
        new_doc.insert()