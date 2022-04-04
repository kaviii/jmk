import frappe
from frappe.model.naming import make_autoname
from frappe.utils import getdate

def autoname_sales_invoice(doc, method=None):
    if doc.get('invoice_series'):
        doc.naming_series = '{}/.FY./.###'.format(doc.invoice_series)

    doc.name = make_autoname(doc.naming_series, 'Sales Invoice', doc)

def on_update_customer(doc, method=None):
    check_item_price = frappe.get_all('Item Price', filters={'customer': doc.name}, limit_page_length=1)
    if not check_item_price or len(check_item_price) == 0:
        frappe.enqueue(method=customer_pricing, queue='default', docname=doc.name)

def customer_pricing(docname):
    item_price_list = frappe.get_all('Item Price', filters={'selling': 1, 'customer': ''})
    for item in item_price_list:
        price = frappe.get_doc('Item Price', item.name)
        new_doc = frappe.copy_doc(price)
        new_doc.update({
            'customer': docname,
            'valid_from': getdate()
        })
        new_doc.save()