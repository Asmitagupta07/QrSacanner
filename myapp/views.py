from django.shortcuts import render, reverse
from .forms import UserRegistrationForm
from .models import UserProfile
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from .models import UserRegistration, UserProfile,Expenditure
from .models import UserRegistration
from django.views.decorators.csrf import csrf_exempt
import decimal
from django.core.exceptions import ValidationError


def convert_decimal_to_string(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_decimal_to_string(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = convert_decimal_to_string(data[i])
    elif isinstance(data, decimal.Decimal):
        return f"{data:.2f}"  
    return data

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                 
                if form.cleaned_data.get('during_month') not in range(1, 13):
                    form.add_error('during_month', 'Please enter a valid month (1-12).')
               
                user_registration = form.save()
                
                sl_no_list = request.POST.getlist('sl_no')
                item_desc_list = request.POST.getlist('item_description')
                qty_list = request.POST.getlist('qty')
                qty_type_list = request.POST.getlist('qty_type')
                tax_type_list = request.POST.getlist('tax_type')
                base_amount_list = request.POST.getlist('base_amount')
                tax_amount_list = request.POST.getlist('tax_amount')
                amount_list = request.POST.getlist('amount')

                print(f'user_registration {user_registration}')

                expenditures = []
                for i in range(len(sl_no_list)):
                    expenditure = Expenditure.objects.create(
                        user_registration=user_registration,
                        sl_no=sl_no_list[i],
                        item_description=item_desc_list[i],
                        qty=qty_list[i],
                        qty_type=qty_type_list[i],
                        tax_type=tax_type_list[i],
                        base_amount=base_amount_list[i],
                        tax_amount=tax_amount_list[i],
                        amount=amount_list[i]
                    )
                    expenditures.append({
                        'sl_no': sl_no_list[i],
                        'item_description': item_desc_list[i],
                        'qty': qty_list[i],
                        'qty_type': qty_type_list[i],
                        'tax_type': tax_type_list[i],
                        'base_amount': base_amount_list[i],
                        'tax_amount': tax_amount_list[i],
                        'amount': amount_list[i],
                    })
                    print(f"expenditures....................... {expenditures}")


                
                qr_data = {
                    'unit_id': user_registration.unit_id,
                    'unit_name': user_registration.unit_name,
                    'unit_address': user_registration.unit_address,
                    'dak_id': user_registration.dak_id,
                    'codehead': user_registration.codehead,
                    'ifa_cfa': user_registration.ifa_cfa,
                    'amount_allotment': user_registration.amount_allotment,
                    'amount_expended': user_registration.amount_expended,
                    'balance_allotment': user_registration.balance_allotment,
                    'expenditure_account': user_registration.expenditure_account,
                    'incurred_by': user_registration.incurred_by,
                    'during_month': user_registration.during_month,
                    'authority': user_registration.authority,
                    'sanction_no': user_registration.sanction_no,
                    'sanction_date': user_registration.sanction_date,
                    'sanction_amount': user_registration.sanction_amount,
                    'supply_order_no': user_registration.supply_order_no,
                    'supply_order_date': user_registration.supply_order_date,
                    'supply_order_amount': user_registration.supply_order_amount,
                    'expenditures' : expenditures,
                    'bill_no': user_registration.bill_no,
                    'bill_date': user_registration.bill_date,
                    'invoice_no': user_registration.invoice_no,
                    'invoice_date': user_registration.invoice_date,
                    'disallowed_amount': user_registration.disallowed_amount,
                    'total_bill_amount': user_registration.total_bill_amount,
                    'crv_esic_epfo_no': user_registration.crv_esic_epfo_no,
                    'crv_esic_epfo_date': user_registration.crv_esic_epfo_date,
                    'vendor_name': user_registration.vendor_name,
                    'msme_nonmsme': user_registration.msme_nonmsme,
                    'vendor_bank_account': user_registration.vendor_bank_account,
                    'ifsc': user_registration.ifsc,
                    'gstin': user_registration.gstin,
                    'pan': user_registration.pan,
                    'paying_authority': user_registration.paying_authority,
                }

                qr_data = convert_decimal_to_string(qr_data)
                qr_text = "\n".join([f"{key}: {value}" for key, value in qr_data.items()])
                print(f"QR Code Text: \n{qr_text}")
                qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=4)
                qr.add_data(qr_text)
                qr.make(fit=True)
                img = qr.make_image(fill='black', back_color='white')

                buffer = BytesIO()
                img.save(buffer, 'PNG')
                buffer.seek(0)

                user_profile = UserProfile.objects.create(
                    user=None 
                )

                user_profile.qr_code.save(f'{user_registration.unit_name}_{user_registration.unit_id}_qr_code.png', ContentFile(buffer.getvalue()))

                context = {
                    'form': form,
                    'user_registration': user_registration,
                    'user_profile': user_profile,
                    'qr_code': user_profile.qr_code.url,  
                }

                return render(request, 'user_profile.html', context)
            except IntegrityError as e:
                print(f"IntegrityError: {str(e)}")
                error_message = f"Error occurred while registering. Details: {str(e)}"
                return render(request, 'register.html', {'form': form, 'error_message': error_message})
            
            except ValidationError as e:
                print(f"Validation error: {str(e)}")
                error_message = f"Invalid input: {str(e)}"
                return render(request, 'register.html', {'form': form, 'error_message': error_message})
            
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                error_message = "An unexpected error occurred. Please try again."
                return render(request, 'register.html', {'form': form, 'error_message': error_message})

    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def user_profile(request, id):
    print(f"user_id .......................: {id}")
    
    user_registration = get_object_or_404(UserRegistration, id=id)
    print(f"user_registration .......................: {user_registration}")
    user = get_object_or_404(User, id=user_registration.id)  
    user_profile_instance = get_object_or_404(UserProfile, user=user)
    qr_code_url = user_profile_instance.qr_code.url if user_profile_instance.qr_code else None
    print(f"QR Code URL: {qr_code_url}")

    return render(request, 'user_profile.html', {
        'user_registration': user_registration,
        'user_profile': user_profile_instance,
        'qr_code': qr_code_url,  
    })

