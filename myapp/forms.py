
from django import forms
from .models import UserRegistration, Expenditure

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = '__all__'
        labels = {
            'unit_id': 'a. Unique Unit ID (14 digit)',
            'unit_name': 'b. Unit name',
            'unit_address': 'c. Unit Address',
            'dak_id': 'd. Dak ID (if Resubmitted Bill)',
            'codehead': 'a. Codehead',
            'ifa_cfa': 'b. IFA Con / CFA Inherited',
            'amount_allotment': 'c. Amount of Allotment',
            'amount_expended': 'd. Amount Expended and for which bills have been submitted for payment',
            'balance_allotment': 'e. Balance of Allotment Excluding the amount of this bill',
            'expenditure_account': 'a. Expenditure on account of',
            'incurred_by': 'b. Incurred by',
            'during_month': 'c. During Month',
            'authority': 'd. Authority',
            'sanction_no': 'e. Sanction No.',
            'sanction_date': 'f. Sanction Date',
            'supply_order_no': 'g. Supply Order No.',
            'supply_order_date': 'h. Supply Order Date',
            'sanction_amount': 'f. Sanction Amount',
            'supply_order_amount': 'j. Supply Order Amount',
            'bill_no': 'a. Bill No',
            'bill_date': 'b. Bill Date',
            'invoice_no': 'c. Invoice No.',
            'invoice_date': 'd. Invoice Date',
            'disallowed_amount': 'e. Disallowed Amount',
            'total_bill_amount': 'f. Total Bill Amount',
            'crv_esic_epfo_no': 'g. CRV / ESIC/EPFO Challan /CRAC no.',
            'crv_esic_epfo_date': 'h. CRV / ESIC/EPFO /CRAC Date',
            'vendor_name': 'a. Unit / Vendor name',
            'msme_nonmsme': 'b. MSME / Non-MSME',
            'vendor_bank_account': 'c. Unit / Vendor bank a/c no',
            'ifsc': 'd. IFSC',
            'gstin': 'e. GSTIN',
            'pan': 'f. PAN',
            'paying_authority': 'PCDA / CDA / AAO',
        }
        widgets = {
            'bill_date': forms.DateInput(attrs={'type': 'date'}),
            'supply_order_date': forms.DateInput(attrs={'type': 'date'}),
            'sanction_date': forms.DateInput(attrs={'type': 'date'}),
            'invoice_date': forms.DateInput(attrs={'type': 'date'}),
            'crv_esic_epfo_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ['sl_no', 'item_description', 'qty', 'qty_type', 'tax_type', 'base_amount', 'tax_amount', 'amount']
        labels = {
            'sl_no': 'Sl. No.',
            'item_description': 'Item Description',
            'qty': 'Qty',
            'qty_type': 'Qty Type',
            'tax_type': 'Tax Type',
            'base_amount': 'Base Amount',
            'tax_amount': 'Tax Amount',
            'amount': 'Amount',
        }
