# Generated by Django 5.0.7 on 2024-08-05 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_id', models.CharField(max_length=14)),
                ('unit_name', models.CharField(max_length=100)),
                ('unit_address', models.TextField()),
                ('dak_id', models.CharField(blank=True, max_length=100, null=True)),
                ('codehead', models.CharField(max_length=100)),
                ('ifa_cfa', models.CharField(max_length=100)),
                ('amount_allotment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_expended', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balance_allotment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expenditure_account', models.CharField(max_length=100)),
                ('incurred_by', models.CharField(max_length=100)),
                ('during_month', models.CharField(max_length=100)),
                ('authority', models.CharField(max_length=100)),
                ('sanction_no', models.CharField(max_length=100)),
                ('sanction_date', models.DateField()),
                ('sanction_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('supply_order_no', models.CharField(max_length=100)),
                ('supply_order_date', models.DateField()),
                ('supply_order_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bill_no', models.CharField(max_length=100)),
                ('bill_date', models.DateField()),
                ('invoice_no', models.CharField(max_length=100)),
                ('invoice_date', models.DateField()),
                ('disallowed_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_bill_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('crv_esic_epfo_no', models.CharField(max_length=100)),
                ('crv_esic_epfo_date', models.DateField()),
                ('vendor_name', models.CharField(max_length=100)),
                ('msme_nonmsme', models.CharField(choices=[('msme', 'MSME'), ('non-msme', 'Non-MSME')], max_length=20)),
                ('vendor_bank_account', models.CharField(max_length=100)),
                ('ifsc', models.CharField(max_length=11)),
                ('gstin', models.CharField(max_length=15)),
                ('pan', models.CharField(max_length=10)),
                ('paying_authority', models.CharField(max_length=100)),
                ('signature', models.CharField(max_length=100)),
                ('countersigned', models.CharField(max_length=100)),
                ('received_payment', models.CharField(max_length=100)),
            ],
        ),
    ]