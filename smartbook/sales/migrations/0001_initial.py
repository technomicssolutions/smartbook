# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Quotation'
        db.create_table(u'sales_quotation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Customer'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('attention', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('reference_id', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('prefix', self.gf('django.db.models.fields.CharField')(default='QO', max_length=20, null=True, blank=True)),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('net_total', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('is_sales_invoice_created', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delivery', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('proof', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('payment', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('validity', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'sales', ['Quotation'])

        # Adding model 'QuotationItem'
        db.create_table(u'sales_quotationitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'], null=True, blank=True)),
            ('quotation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.Quotation'], null=True, blank=True)),
            ('net_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('quantity_sold', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('discount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('selling_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'sales', ['QuotationItem'])

        # Adding model 'DeliveryNote'
        db.create_table(u'sales_deliverynote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quotation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.Quotation'], null=True, blank=True)),
            ('salesman', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('delivery_note_number', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('lpo_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('net_total', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('is_pending', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'sales', ['DeliveryNote'])

        # Adding model 'DeliveryNoteItem'
        db.create_table(u'sales_deliverynoteitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'], null=True, blank=True)),
            ('delivery_note', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.DeliveryNote'], null=True, blank=True)),
            ('net_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('quantity_sold', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('discount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('total_quantity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('selling_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'sales', ['DeliveryNoteItem'])

        # Adding model 'Sales'
        db.create_table(u'sales_sales', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sales_invoice_number', self.gf('django.db.models.fields.CharField')(max_length=10, unique=True, null=True, blank=True)),
            ('sales_invoice_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Customer'], null=True, blank=True)),
            ('salesman', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('payment_mode', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('card_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('net_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('round_off', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('grant_total', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('discount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('delivery_note', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.DeliveryNote'], null=True, blank=True)),
            ('lpo_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('is_processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=14, decimal_places=2, blank=True)),
            ('paid', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=14, decimal_places=2, blank=True)),
            ('discount_for_sale', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('discount_percentage_for_sale', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'sales', ['Sales'])

        # Adding model 'SalesItem'
        db.create_table(u'sales_salesitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'])),
            ('sales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.Sales'])),
            ('quantity_sold', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('discount_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('discount_percentage', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('selling_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('net_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'sales', ['SalesItem'])

        # Adding model 'SalesReturn'
        db.create_table(u'sales_salesreturn', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.Sales'])),
            ('return_invoice_number', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('net_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'sales', ['SalesReturn'])

        # Adding model 'SalesReturnItem'
        db.create_table(u'sales_salesreturnitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sales_return', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.SalesReturn'], null=True, blank=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'], null=True, blank=True)),
            ('return_quantity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'sales', ['SalesReturnItem'])

        # Adding model 'ReceiptVoucher'
        db.create_table(u'sales_receiptvoucher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sales_invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.Sales'], null=True, blank=True)),
            ('receipt_voucher_no', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('total_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('paid_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('cheque_no', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('bank', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('dated', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('payment_mode', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
        ))
        db.send_create_signal(u'sales', ['ReceiptVoucher'])

        # Adding model 'CustomerAccount'
        db.create_table(u'sales_customeraccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice_no', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.Sales'], null=True, blank=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Customer'], null=True, blank=True)),
            ('total_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('paid', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('is_complted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'sales', ['CustomerAccount'])

    def backwards(self, orm):
        # Deleting model 'Quotation'
        db.delete_table(u'sales_quotation')

        # Deleting model 'QuotationItem'
        db.delete_table(u'sales_quotationitem')

        # Deleting model 'DeliveryNote'
        db.delete_table(u'sales_deliverynote')

        # Deleting model 'DeliveryNoteItem'
        db.delete_table(u'sales_deliverynoteitem')

        # Deleting model 'Sales'
        db.delete_table(u'sales_sales')

        # Deleting model 'SalesItem'
        db.delete_table(u'sales_salesitem')

        # Deleting model 'SalesReturn'
        db.delete_table(u'sales_salesreturn')

        # Deleting model 'SalesReturnItem'
        db.delete_table(u'sales_salesreturnitem')

        # Deleting model 'ReceiptVoucher'
        db.delete_table(u'sales_receiptvoucher')

        # Deleting model 'CustomerAccount'
        db.delete_table(u'sales_customeraccount')

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'barcode': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tax': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'uom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.UnitOfMeasure']", 'null': 'True', 'blank': 'True'})
        },
        u'inventory.unitofmeasure': {
            'Meta': {'object_name': 'UnitOfMeasure'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'sales.customeraccount': {
            'Meta': {'object_name': 'CustomerAccount'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Customer']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_no': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.Sales']", 'null': 'True', 'blank': 'True'}),
            'is_complted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        },
        u'sales.deliverynote': {
            'Meta': {'object_name': 'DeliveryNote'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'delivery_note_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_pending': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lpo_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'net_total': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'quotation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.Quotation']", 'null': 'True', 'blank': 'True'}),
            'salesman': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'sales.deliverynoteitem': {
            'Meta': {'object_name': 'DeliveryNoteItem'},
            'delivery_note': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.DeliveryNote']", 'null': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']", 'null': 'True', 'blank': 'True'}),
            'net_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'quantity_sold': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'selling_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'total_quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'sales.quotation': {
            'Meta': {'object_name': 'Quotation'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'delivery': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sales_invoice_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'net_total': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'payment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'default': "'QO'", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'proof': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'reference_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Customer']", 'null': 'True', 'blank': 'True'}),
            'validity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'sales.quotationitem': {
            'Meta': {'object_name': 'QuotationItem'},
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']", 'null': 'True', 'blank': 'True'}),
            'net_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'quantity_sold': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'quotation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.Quotation']", 'null': 'True', 'blank': 'True'}),
            'selling_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        },
        u'sales.receiptvoucher': {
            'Meta': {'object_name': 'ReceiptVoucher'},
            'bank': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cheque_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'payment_mode': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'receipt_voucher_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'sales_invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.Sales']", 'null': 'True', 'blank': 'True'}),
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        },
        u'sales.sales': {
            'Meta': {'object_name': 'Sales'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'card_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Customer']", 'null': 'True', 'blank': 'True'}),
            'delivery_note': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.DeliveryNote']", 'null': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'discount_for_sale': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'discount_percentage_for_sale': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'grant_total': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lpo_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'net_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'payment_mode': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'round_off': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'sales_invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'sales_invoice_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'salesman': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'sales.salesitem': {
            'Meta': {'object_name': 'SalesItem'},
            'discount_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'discount_percentage': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'net_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'quantity_sold': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.Sales']"}),
            'selling_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        },
        u'sales.salesreturn': {
            'Meta': {'object_name': 'SalesReturn'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'net_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'return_invoice_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'sales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.Sales']"})
        },
        u'sales.salesreturnitem': {
            'Meta': {'object_name': 'SalesReturnItem'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']", 'null': 'True', 'blank': 'True'}),
            'return_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sales_return': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.SalesReturn']", 'null': 'True', 'blank': 'True'})
        },
        u'web.customer': {
            'Meta': {'object_name': 'Customer'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'customer_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'house_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_line': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sales']