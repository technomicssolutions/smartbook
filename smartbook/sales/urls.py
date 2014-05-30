from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from sales.views import *

urlpatterns = patterns('',

	url(r'^$', login_required(SalesDetails.as_view()), name='sales_details'),	
	url(r'^entry/$', login_required(SalesEntry.as_view()), name='sales'),
	url(r'^return/$', login_required(SalesReturnView.as_view()), name='return_entry'),	
	#url(r'sales_return_entry/$', SalesReturnView.as_view(), name='return_entry'),
	url(r'view_sales/$', login_required(ViewSales.as_view()), name='view_sales'),
	url(r'create_quotation/$', login_required(CreateQuotation.as_view()), name='create_quotation'),
	url(r'^create_quotation_pdf/(?P<quotation_id>\d+)/$', login_required(CreateQuotationPdf.as_view()), name='create_quotation_pdf'),
	url(r'create_delivery_note/$', login_required(CreateDeliveryNote.as_view()), name='create_delivery_note'),
	url(r'quotaion_deliverynote_sales/$', login_required(QuotationDeliverynoteSales.as_view()), name='create_sales_entry'),
	url(r'quotation_details/$', login_required(QuotationDetails.as_view()), name='quotation_details'),
	url(r'delivery_note_details/$', login_required(DeliveryNoteDetails.as_view()), name='delivery_note_details'),
	url(r'^delivery_note_pdf/(?P<delivery_note_id>\d+)/$', login_required(DeliveryNotePDF.as_view()), name='delivery_note_pdf'),
	url(r'^sales_invoice_pdf/(?P<sales_invoice_id>\d+)/$', login_required(CreateSalesInvoicePDF.as_view()), name='sales_invoice_pdf'),
	url(r'pdf_receipt_voucher/(?P<receipt_voucher_id>\d+)/$', login_required(PrintReceiptVoucher.as_view()), name="pdf_receipt_voucher"),
	url(r'receipt_voucher/$', login_required(ReceiptVoucherCreation.as_view()), name='receipt_voucher'),
	url(r'invoice_details/$', login_required(InvoiceDetails.as_view()), name='invoice_details'),
	url(r'direct_delivery_note/$', login_required(DirectDeliveryNote.as_view()), name='direct_delivery_note'),
	url(r'latest_sales_details/$',login_required(LatestSalesDetails.as_view()), name='latest_sales_details'),
	url(r'edit_sales_invoice/$', login_required(EditSalesInvoice.as_view()), name='edit_sales_invoice'),
	url(r'edit_quotation/$', login_required(EditQuotation.as_view()), name='edit_quotation'),
	url(r'edit_delivery_note/$', login_required(EditDeliveryNote.as_view()), name='edit_delivery_note'),
)