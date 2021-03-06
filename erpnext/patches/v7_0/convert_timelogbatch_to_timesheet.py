import frappe
from frappe.utils import cint
from erpnext.manufacturing.doctype.production_order.production_order import add_timesheet_detail

def execute():	
	for tlb in frappe.get_all('Time Log Batch', fields=["*"], 
		filters = [["docstatus", "<", "2"]]):
		time_sheet = frappe.new_doc('Time Sheet')
		time_sheet.employee= ""
		time_sheet.company = frappe.db.get_single_value('Global Defaults', 'default_company')
		time_sheet.sales_invoice = tlb.sales_invoice
		if tlb.get('time_logs'):
			for data in tlb.time_logs:
				args = get_timesheet_data(data)
				add_timesheet_detail(time_sheet, args)

			time_sheet.docstatus = tlb.docstatus
			time_sheet.save(ignore_permissions=True)

def get_timesheet_data(data):
	time_log = frappe.get_doc('Time Log', data.time_log)

	return {
		'from_time': time_log.from_time,
		'hours': time_log.hours,
		'to_time': time_log.to_time,
		'project': time_log.project,
		'activity_type': time_log.activity_type,
		'operation': time_log.operation,
		'operation_id': time_log.operation_id,
		'workstation': time_log.workstation,
		'completed_qty': time_log.completed_qty
	}