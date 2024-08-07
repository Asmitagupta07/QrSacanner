from django.db import models

class UserRegistration(models.Model):
    unit_id = models.CharField(max_length=14)
    unit_name = models.CharField(max_length=100)
    unit_address = models.TextField()
    dak_id = models.CharField(max_length=100, blank=True, null=True)
    
    codehead = models.CharField(max_length=100)
    ifa_cfa = models.CharField(max_length=100)
    amount_allotment = models.DecimalField(max_digits=10, decimal_places=2)
    amount_expended = models.DecimalField(max_digits=10, decimal_places=2)
    balance_allotment = models.DecimalField(max_digits=10, decimal_places=2)
    
    expenditure_account = models.CharField(max_length=100)
    incurred_by = models.CharField(max_length=100)
    during_month = models.CharField(max_length=100)
    authority = models.CharField(max_length=100)
    sanction_no = models.CharField(max_length=100)
    sanction_date = models.DateField()
    sanction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    supply_order_no = models.CharField(max_length=100)
    supply_order_date = models.DateField()
    supply_order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    bill_no = models.CharField(max_length=100)
    bill_date = models.DateField()
    invoice_no = models.CharField(max_length=100)
    invoice_date = models.DateField()
    disallowed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    crv_esic_epfo_no = models.CharField(max_length=100)
    crv_esic_epfo_date = models.DateField()
    
    vendor_name = models.CharField(max_length=100)
    msme_nonmsme = models.CharField(max_length=20, choices=[('msme', 'MSME'), ('non-msme', 'Non-MSME')])
    vendor_bank_account = models.CharField(max_length=100)
    ifsc = models.CharField(max_length=11)
    gstin = models.CharField(max_length=15)
    pan = models.CharField(max_length=10)
    
    paying_authority = models.CharField(max_length=100)
    
    signature = models.CharField(max_length=100)
    countersigned = models.CharField(max_length=100)
    received_payment = models.CharField(max_length=100)

    def __str__(self):
        return self.unit_name
    


from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
