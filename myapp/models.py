from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserRegistration(models.Model):
    unit_id = models.CharField(max_length=14,validators=[MinLengthValidator(14)],help_text="Unit ID must be exactly 14 characters long.")
    unit_name = models.CharField(max_length=100)
    unit_address = models.TextField()
    dak_id = models.CharField(max_length=100, blank=True, null=True)
    
    codehead = models.CharField(max_length=10)
    # ifa_cfa = models.CharField(max_length=100, blank=True, null=True)
    ifa_cfa = models.CharField(max_length=100,choices=[('IFA CON','IFA CON'), ('CFA INHERITED', 'CFA INHERITED')], blank=True, null=True)
    amount_allotment = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    amount_expended = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    balance_allotment = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    
    expenditure_account = models.CharField(max_length=100, blank=True, null=True)
    incurred_by = models.CharField(max_length=100)
    # during_month = models.PositiveSmallIntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(12)],
    #     help_text="Enter a valid month (1-12)."
    # )
    during_month = models.CharField(max_length=7,validators=[MaxLengthValidator(7)],help_text="during_month must be exactly 7 characters long mm/yyyy.")
    authority = models.CharField(max_length=100, blank=True, null=True)
    sanction_no = models.CharField(max_length=100)
    sanction_date = models.DateField()
    sanction_amount = models.DecimalField(max_digits=15, decimal_places=2)
    supply_order_no = models.CharField(max_length=100)
    supply_order_date = models.DateField()
    supply_order_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    bill_no = models.CharField(max_length=100)
    bill_date = models.DateField()
    invoice_no = models.CharField(max_length=100)
    invoice_date = models.DateField()
    disallowed_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    total_bill_amount = models.DecimalField(max_digits=15, decimal_places=2)
    crv_esic_epfo_no = models.CharField(max_length=100)
    crv_esic_epfo_date = models.DateField()
    
    vendor_name = models.CharField(max_length=100)
    msme_nonmsme = models.CharField(max_length=20, choices=[('msme', 'MSME'), ('non-msme', 'Non-MSME')],blank=True, null=True)
    vendor_bank_account = models.CharField(max_length=12)
    ifsc = models.CharField(max_length=11)
    gstin = models.CharField(max_length=15, blank=True, null=True)
    pan = models.CharField(max_length=10, blank=True, null=True)
    Make = models.CharField(
    max_length=30, 
    choices=[
            
            ('DPSU', 'MAKE IN INDIA(DPSU)'),
            ('PSU', 'MAKE IN INDIA(PSU)'),
            ('STARTUP', 'MAKE IN INDIA(STARTUP)'),
            ('RAKSHA RATNAM', 'MAKE IN INDIA(RAKSHA RATNAM)'),
            ('PRIVATE', 'MAKE IN INDIA(PRIVATE)'),
            ('DBT', 'MAKE IN INDIA(DBT)'),
            ('LC', 'FOREIGN PROCUREMENT(LC)')
    ],
    blank=True, 
    null=True
    )    
    paying_authority = models.CharField(max_length=100)


    def __str__(self):
        return self.unit_name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
 
class Expenditure(models.Model):
    user_registration = models.ForeignKey('UserRegistration', related_name='expenditures', on_delete=models.CASCADE)
    sl_no = models.IntegerField()
    item_description = models.CharField(max_length=255)
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    qty_type = models.CharField(max_length=50)
    tax_type = models.CharField(max_length=50)
    base_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Expenditure {self.sl_no} for {self.user_registration.unit_name}"


