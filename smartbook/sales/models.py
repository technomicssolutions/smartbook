from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

from inventory.models import Item
from inventory.models import Brand
from web.models import Customer, Staff


# Create your models here. 

class Quotation(models.Model):

    to = models.ForeignKey(Customer)
    date = models.DateField('Date', null=True, blank=True)
    attention = models.TextField('Attention', null=True, blank=True)
    subject = models.CharField('Subject', null=True, blank=True, max_length=20)
    reference_id = models.CharField('Reference no', null=True, blank=True, max_length=10)
    prefix = models.CharField('Prefix', null=True, blank=True, max_length=20, default='QO')
    item = models.ManyToManyField(Item, null=True, blank=True)
    processed = models.BooleanField('Is Processed', default=False)


    def __unicode__(self):

        return str(self.to.customer_name)

    class Meta:

        verbose_name = 'Quotation'
        verbose_name_plural = 'Quotation'

class DeliveryNote(models.Model):

    quotation = models.ForeignKey(Quotation)
    customer = models.ForeignKey(Customer)
    delivery_note_number = models.CharField('Delivery Note Serial number', max_length=50, null=True, blank=True)
    date = models.DateField('Date', null=True, blank=True)
    lpo_number = models.CharField('LPO Number', null=True, blank=True, max_length=20)
    prefix = models.CharField('Prefix', null=True, blank=True, max_length=20, default='DN')
    processed = models.BooleanField('Is Processed', default=False)


    def __unicode__(self):

        return str(self.to.customer_name)

    class Meta:

        verbose_name = 'Delivery Note'
        verbose_name_plural = 'Delivery Note'


class Sales(models.Model):  
    sales_invoice_number = models.IntegerField('Sales Invoice Number', default=0)
    sales_invoice_date = models.DateField('Sales Invoice Date', null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True)
    salesman = models.ForeignKey(Staff, null=True, blank=True)
    payment_mode = models.CharField('Payment Mode', null=True, blank=True, max_length=25)
    card_number = models.IntegerField('Crad Number',null=True, blank=True)
    bank_name = models.CharField('Bank Name',max_length=50,null=True, blank=True)
    net_amount = models.DecimalField('Net Amount',max_digits=14, decimal_places=3, default=0)
    round_off = models.DecimalField('Net Round Off',max_digits=14, decimal_places=3, default=0)
    grant_total = models.DecimalField('Grand Total',max_digits=14, decimal_places=3, default=0)
    discount = models.DecimalField('Total Discount',max_digits=14, decimal_places=3, default=0)
    quotation = models.ForeignKey(Quotation, null=True, blank=True)
    delivery_note = models.ForeignKey(DeliveryNote, null=True, blank=True)

    def __unicode__(self):

        return str(self.sales_invoice_number)

    class Meta:

        verbose_name = 'Sales'
        verbose_name_plural = 'Sales'


class SalesInvoice(models.Model):

    quotation = models.ForeignKey(Quotation)
    delivery_note = models.ForeignKey(DeliveryNote)
    sales = models.ForeignKey(Sales)
    customer = models.ForeignKey(Customer)
    date = models.DateField('Date', null=True, blank=True)
    invoice_no = models.CharField('Invoice Number',null=True, blank=True, max_length=20)
    prefix =  models.CharField('Prefix', max_length=20, default='SI')


    def __unicode__(self):

        return str(self.invoice_no)

    class Meta:

        verbose_name = 'Sales Invoice'
        verbose_name_plural = 'Sales Invoice'

class SalesItem(models.Model):

    item = models.ForeignKey(Item)
    sales = models.ForeignKey(Sales)
    quantity_sold = models.IntegerField('Quantity Sold', default=0)
    discount_given = models.DecimalField('Discount Given',max_digits=14, decimal_places=3, default=0)   
    
    
    def __unicode__(self):

        return str(self.sales.sales_invoice_number)

    class Meta:

        verbose_name = 'Sales Items'
        verbose_name_plural = 'Sales Items'

class SalesReturn(models.Model):
    sales = models.ForeignKey(Sales)
    return_invoice_number = models.IntegerField('Sales Return invoice number', unique=True)
    date = models.DateField('Date', null=True, blank=True)
    net_amount = models.IntegerField('Total', null=True, blank=True)
    

    def __unicode__(self):
        return str(self.sales.sales_invoice_number)

class SalesReturnItem(models.Model):
    sales_return = models.ForeignKey(SalesReturn, null=True, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True)
    return_quantity = models.IntegerField('Return Quantity', null=True, blank=True)
    amount = models.IntegerField('Amount', null=True, blank=True)

    def __unicode__(self):

        return str(self.sales_return.return_invoice_number)




        


