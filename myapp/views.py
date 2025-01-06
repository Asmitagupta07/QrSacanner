
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm
from .models import UserProfile
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from .models import UserRegistration, UserProfile,Expenditure
from django.http import JsonResponse
from .models import UserRegistration
from django.views.decorators.csrf import csrf_exempt
import json
import decimal
import datetime
from django.core.exceptions import ValidationError

def convert_to_serializable(data):
    if isinstance(data, dict):
        return {key: convert_to_serializable(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_to_serializable(item) for item in data]
    elif isinstance(data, decimal.Decimal):
        return float(data)
    elif isinstance(data, datetime.date):
        return data.isoformat()  
    else:
        return data

# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             try:
#                 user_registration = form.save()

#                 # Handle Expenditure data
#                 sl_no_list = request.POST.getlist('sl_no')
#                 item_desc_list = request.POST.getlist('item_description')
#                 qty_list = request.POST.getlist('qty')
#                 qty_type_list = request.POST.getlist('qty_type')
#                 tax_type_list = request.POST.getlist('tax_type')
#                 base_amount_list = request.POST.getlist('base_amount')
#                 tax_amount_list = request.POST.getlist('tax_amount')
#                 amount_list = request.POST.getlist('amount')

#                 print(f'user_registration {user_registration}')

#                 expenditures = []
#                 for i in range(len(sl_no_list)):
#                     expenditure = Expenditure.objects.create(
#                         user_registration=user_registration,
#                         sl_no=sl_no_list[i],
#                         item_description=item_desc_list[i],
#                         qty=qty_list[i],
#                         qty_type=qty_type_list[i],
#                         tax_type=tax_type_list[i],
#                         base_amount=base_amount_list[i],
#                         tax_amount=tax_amount_list[i],
#                         amount=amount_list[i]
#                     )
#                     expenditures.append({
#                         'sl_no': sl_no_list[i],
#                         'item_description': item_desc_list[i],
#                         'qty': qty_list[i],
#                         'qty_type': qty_type_list[i],
#                         'tax_type': tax_type_list[i],
#                         'base_amount': base_amount_list[i],
#                         'tax_amount': tax_amount_list[i],
#                         'amount': amount_list[i],
#                     })

#                 # Convert the qr_data before dumping to JSON
#                 qr_data = {
#                     'unit_id': user_registration.unit_id,
#                     'unit_name': user_registration.unit_name,
#                     'unit_address': user_registration.unit_address,
#                     'dak_id': user_registration.dak_id,
#                     'codehead': user_registration.codehead,
#                     'ifa_cfa': user_registration.ifa_cfa,
#                     'amount_allotment': user_registration.amount_allotment,
#                     'amount_expended': user_registration.amount_expended,
#                     'expenditure_account': user_registration.expenditure_account,
#                     'incurred_by': user_registration.incurred_by,
#                     'during_month': user_registration.during_month,
#                     'authority': user_registration.authority,
#                     'sanction_no': user_registration.sanction_no,
#                     'sanction_date': user_registration.sanction_date,
#                     'sanction_amount': user_registration.sanction_amount,
#                     'supply_order_no': user_registration.supply_order_no,
#                     'supply_order_date': user_registration.supply_order_date,
#                     'supply_order_amount': user_registration.supply_order_amount,
#                     'expenditures': expenditures,
#                     'bill_no': user_registration.bill_no,
#                     'bill_date': user_registration.bill_date,
#                     'invoice_no': user_registration.invoice_no,
#                     'invoice_date': user_registration.invoice_date,
#                     'disallowed_amount': user_registration.disallowed_amount,
#                     'total_bill_amount': user_registration.total_bill_amount,
#                     'crv_esic_epfo_no': user_registration.crv_esic_epfo_no,
#                     'crv_esic_epfo_date': user_registration.crv_esic_epfo_date,
#                     'vendor_name': user_registration.vendor_name,
#                     'msme_nonmsme': user_registration.msme_nonmsme,
#                     'vendor_bank_account': user_registration.vendor_bank_account,
#                     'ifsc': user_registration.ifsc,
#                     'gstin': user_registration.gstin,
#                     'pan': user_registration.pan,
#                     'paying_authority': user_registration.paying_authority,
#                 }

#                 # Convert any Decimal values in qr_data to float
#                 qr_data = convert_to_serializable(qr_data)


#                 qr_data_json = json.dumps(qr_data)
#                 print(f"qr_data_json ---------------------------{qr_data_json}")

#                 # Generate the QR code
#                 qr = qrcode.QRCode(
#                     version=None,  
#                     error_correction=qrcode.constants.ERROR_CORRECT_L,  
#                     box_size=5,  
#                     border=4,
#                 )
#                 qr.add_data(qr_data_json)
#                 qr.make(fit=True)
#                 img = qr.make_image(fill='black', back_color='white')

#                 # Save the QR code image
#                 buffer = BytesIO()
#                 img.save(buffer, 'PNG')
#                 buffer.seek(0)

#                 # # Handle user profile creation
#                 # user = request.user if request.user.is_authenticated else None
#                 # if not user:
#                 #     user = User.objects.create(username=user_registration.unit_name, email=user_registration.unit_address)

#                 # user_profile, created = UserProfile.objects.get_or_create(user=user)
#                 # user_profile.qr_code.save(f'{user_registration.unit_name}_qr_code.png', ContentFile(buffer.getvalue()))
                
#                  # Handle user profile creation
#                 user = request.user if request.user.is_authenticated else None
#                 if not user:
#                     user = User.objects.create(username=user_registration.unit_name, email=user_registration.unit_address)

#                 # Create or get UserProfile
#                 user_profile, created = UserProfile.objects.get_or_create(user=user)
#                 user_profile.qr_code.save(f'{user_registration.unit_name}_{user_registration.unit_id}_qr_code.png', ContentFile(buffer.getvalue()))

#                 # Return a response
#                 context = {
#                     'form': form,
#                     'user_profile': user_profile,
#                     'user_registration': user_registration,
#                     'qr_data': qr_data_json,  
#                 }

#                 return render(request, 'user_profile.html', context)

#             except IntegrityError:
#                 error_message = "Username already exists. Please choose a different one."
#                 return render(request, 'register.html', {'form': form, 'error_message': error_message})

#     else:
#         form = UserRegistrationForm()

#     return render(request, 'register.html', {'form': form})


# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             try:
#                 # Save the user registration data
#                 user_registration = form.save()

#                 # Handle the expenditure data and other logic (same as before)
#                  # Handle Expenditure data
#                 sl_no_list = request.POST.getlist('sl_no')
#                 item_desc_list = request.POST.getlist('item_description')
#                 qty_list = request.POST.getlist('qty')
#                 qty_type_list = request.POST.getlist('qty_type')
#                 tax_type_list = request.POST.getlist('tax_type')
#                 base_amount_list = request.POST.getlist('base_amount')
#                 tax_amount_list = request.POST.getlist('tax_amount')
#                 amount_list = request.POST.getlist('amount')

#                 print(f'user_registration {user_registration}')

#                 expenditures = []
#                 for i in range(len(sl_no_list)):
#                     expenditure = Expenditure.objects.create(
#                         user_registration=user_registration,
#                         sl_no=sl_no_list[i],
#                         item_description=item_desc_list[i],
#                         qty=qty_list[i],
#                         qty_type=qty_type_list[i],
#                         tax_type=tax_type_list[i],
#                         base_amount=base_amount_list[i],
#                         tax_amount=tax_amount_list[i],
#                         amount=amount_list[i]
#                     )
#                     expenditures.append({
#                         'sl_no': sl_no_list[i],
#                         'item_description': item_desc_list[i],
#                         'qty': qty_list[i],
#                         'qty_type': qty_type_list[i],
#                         'tax_type': tax_type_list[i],
#                         'base_amount': base_amount_list[i],
#                         'tax_amount': tax_amount_list[i],
#                         'amount': amount_list[i],
#                     })


#                 # Prepare QR code data using the current registration details
#                 qr_data = {
#                     'unit_id': user_registration.unit_id,
#                     'unit_name': user_registration.unit_name,
#                     'unit_address': user_registration.unit_address,
#                     'dak_id': user_registration.dak_id,
#                     'codehead': user_registration.codehead,
#                     'ifa_cfa': user_registration.ifa_cfa,
#                     'amount_allotment': user_registration.amount_allotment,
#                     'amount_expended': user_registration.amount_expended,
#                     'balance_allotment': user_registration.balance_allotment,
#                     'expenditure_account': user_registration.expenditure_account,
#                     'incurred_by': user_registration.incurred_by,
#                     'during_month': user_registration.during_month,
#                     'authority': user_registration.authority,
#                     'sanction_no': user_registration.sanction_no,
#                     'sanction_date': user_registration.sanction_date,
#                     'sanction_amount': user_registration.sanction_amount,
#                     'supply_order_no': user_registration.supply_order_no,
#                     'supply_order_date': user_registration.supply_order_date,
#                     'supply_order_amount': user_registration.supply_order_amount,
#                     'bill_no': user_registration.bill_no,
#                     'bill_date': user_registration.bill_date,
#                     'invoice_no': user_registration.invoice_no,
#                     'invoice_date': user_registration.invoice_date,
#                     'disallowed_amount': user_registration.disallowed_amount,
#                     'total_bill_amount': user_registration.total_bill_amount,
#                     'crv_esic_epfo_no': user_registration.crv_esic_epfo_no,
#                     'crv_esic_epfo_date': user_registration.crv_esic_epfo_date,
#                     'vendor_name': user_registration.vendor_name,
#                     'msme_nonmsme': user_registration.msme_nonmsme,
#                     'vendor_bank_account': user_registration.vendor_bank_account,
#                     'ifsc': user_registration.ifsc,
#                     'gstin': user_registration.gstin,
#                     'pan': user_registration.pan,
#                     'paying_authority': user_registration.paying_authority,
#                 }

#                  # Convert any Decimal values in qr_data to float
#                 qr_data = convert_to_serializable(qr_data)

#                 # Generate the QR code
#                 qr_data_json = json.dumps(qr_data)
#                 qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=4)
#                 qr.add_data(qr_data_json)
#                 qr.make(fit=True)
#                 img = qr.make_image(fill='black', back_color='white')

#                 # Save the QR code image to a buffer
#                 buffer = BytesIO()
#                 img.save(buffer, 'PNG')
#                 buffer.seek(0)

#                 # Save QR code image to the UserRegistration record itself (no need for UserProfile)
#                 user_registration.qr_code.save(f'{user_registration.unit_name}_{user_registration.unit_id}_qr_code.png', ContentFile(buffer.getvalue()))

#                 # Return the context with the registration and QR code
#                 context = {
#                     'form': form,
#                     'user_registration': user_registration,
#                     'qr_code': user_registration.qr_code.url,  # Display the QR code
#                 }

#                 return render(request, 'user_profile.html', context)

#             except IntegrityError:
#                 # Handle any errors, such as duplicate unit name or ID
#                 error_message = "Error occurred while registering. Please try again."
#                 return render(request, 'register.html', {'form': form, 'error_message': error_message})

#     else:
#         form = UserRegistrationForm()

#     return render(request, 'register.html', {'form': form})

# Helper function to handle decimal-to-string conversion for QR code serialization
def convert_decimal_to_string(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_decimal_to_string(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = convert_decimal_to_string(data[i])
    elif isinstance(data, decimal.Decimal):
        return f"{data:.2f}"  # Convert Decimal to string with two decimal places
    return data

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                 # Custom validation for 'during_month'
                if form.cleaned_data.get('during_month') not in range(1, 13):
                    form.add_error('during_month', 'Please enter a valid month (1-12).')
                # Save the user registration data
                user_registration = form.save()
                # Handle Expenditure data
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


                # Prepare QR code data using the current registration details
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

                # Convert any Decimal values in qr_data to strings
                qr_data = convert_decimal_to_string(qr_data)

                # Create a text representation of the data (for QR code)
                qr_text = "\n".join([f"{key}: {value}" for key, value in qr_data.items()])
                print(f"QR Code Text: \n{qr_text}")

                # Generate the QR code with the text data
                qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=4)
                qr.add_data(qr_text)
                qr.make(fit=True)
                img = qr.make_image(fill='black', back_color='white')

                # Save the QR code image to a buffer
                buffer = BytesIO()
                img.save(buffer, 'PNG')
                buffer.seek(0)

                # Since there's no user login, we'll create a "dummy" user and profile
                user_profile = UserProfile.objects.create(
                    user=None  # No user, but the profile will still exist to save QR codes
                )

                # Save the generated QR code to the UserProfile
                user_profile.qr_code.save(f'{user_registration.unit_name}_{user_registration.unit_id}_qr_code.png', ContentFile(buffer.getvalue()))

                # Return the context with the registration and QR code
                context = {
                    'form': form,
                    'user_registration': user_registration,
                    'user_profile': user_profile,
                    'qr_code': user_profile.qr_code.url,  # Display the QR code
                }

                return render(request, 'user_profile.html', context)
            except IntegrityError as e:
                # Print out the error for debugging
                print(f"IntegrityError: {str(e)}")
                error_message = f"Error occurred while registering. Details: {str(e)}"
                return render(request, 'register.html', {'form': form, 'error_message': error_message})
            
            except ValidationError as e:
                # Handle specific validation errors
                print(f"Validation error: {str(e)}")
                error_message = f"Invalid input: {str(e)}"
                return render(request, 'register.html', {'form': form, 'error_message': error_message})
            
            except Exception as e:
                # Catch any other errors
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


# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             try:
#                 user_registration = form.save()

#                  # Handle Expenditure data
#                 expenditure_data = request.POST.getlist('sl-no')  
                
#                 # Save expenditures
#                 for i in range(len(expenditure_data)):
#                     Expenditure.objects.create(
#                         user_registration=user_registration,
#                         sl_no=request.POST.getlist('sl-no')[i],
#                         item_description=request.POST.getlist('item-description')[i],
#                         qty=request.POST.getlist('qty')[i],
#                         qty_type=request.POST.getlist('qty-type')[i],
#                         tax_type=request.POST.getlist('tax-type')[i],
#                         base_amount=request.POST.getlist('base-amount')[i],
#                         tax_amount=request.POST.getlist('tax-amount')[i],
#                         amount=request.POST.getlist('amount')[i]
#                     )

#                 # Generate the QR code with user data in key-value pair format
#                 qr_data = request.build_absolute_uri(reverse('user_profile', args=[user_registration.id]))
#                 qr = qrcode.QRCode(
#                     version=1,
#                     error_correction=qrcode.constants.ERROR_CORRECT_L,
#                     box_size=10,
#                     border=4,
#                 )
#                 qr.add_data(qr_data)
#                 qr.make(fit=True)
#                 img = qr.make_image(fill='black', back_color='white')

#                 # Save the QR code image to a BytesIO object
#                 buffer = BytesIO()
#                 img.save(buffer, 'PNG')
#                 buffer.seek(0)

#                 # Handle user profile creation
#                 user = request.user if request.user.is_authenticated else None
#                 if not user:
#                     # Create a temporary user if not logged in
#                     user = User.objects.create(username=user_registration.unit_name, email=user_registration.unit_address)

#                 user_profile, created = UserProfile.objects.get_or_create(user=user)
#                 user_profile.qr_code.save(f'{user_registration.unit_name}_qr_code_{user_registration.unit_id}.png', ContentFile(buffer.getvalue()))

#                 # Debugging: Check user_registration and user_profile
#                 print(f"user_registration: {user_registration}")
#                 print(f"user_profile: {user_profile}")

#                 context={
#                     'form': form,
#                     'user_profile': user_profile,
#                     'user_registration': user_registration
#                 }

#                 return render(request, 'user_profile.html', context)

#             except IntegrityError:
#                 error_message = "Username already exists. Please choose a different one."
#                 return render(request, 'register.html', {'form': form, 'error_message': error_message})

#     else:
#         form = UserRegistrationForm()

#     return render(request, 'register.html', {'form': form})

# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             try:
#                 user_registration = form.save()

#                  # Handle Expenditure data
#                 sl_no_list = request.POST.getlist('sl_no')
#                 item_desc_list = request.POST.getlist('item_description')
#                 qty_list = request.POST.getlist('qty')
#                 qty_type_list = request.POST.getlist('qty_type')
#                 tax_type_list = request.POST.getlist('tax_type')
#                 base_amount_list = request.POST.getlist('base_amount')
#                 tax_amount_list = request.POST.getlist('tax_amount')
#                 amount_list = request.POST.getlist('amount')

#                 # Save Expenditures
#                 for i in range(len(sl_no_list)):
#                     Expenditure.objects.create(
#                         user_registration=user_registration,
#                         sl_no=sl_no_list[i],
#                         item_description=item_desc_list[i],
#                         qty=qty_list[i],
#                         qty_type=qty_type_list[i],
#                         tax_type=tax_type_list[i],
#                         base_amount=base_amount_list[i],
#                         tax_amount=tax_amount_list[i],
#                         amount=amount_list[i]
#                     )
#                 print(f"expenditure -------------{ Expenditure.objects.all()}")

#                 # Generate the QR code with user data in key-value pair format
#                 # qr_data = request.build_absolute_uri(reverse('user_profile', args=[user_registration.id]))
#                 qr_data = request.build_absolute_uri(reverse('user_data_api', args=[user_registration.id]))
#                 print(f"qr_data -------------{ qr_data}")
#                 qr = qrcode.QRCode(
#                     version=1,
#                     error_correction=qrcode.constants.ERROR_CORRECT_L,
#                     box_size=10,
#                     border=4,
#                 )
#                 qr.add_data(qr_data)
#                 qr.make(fit=True)
#                 img = qr.make_image(fill='black', back_color='white')

#                 # Save the QR code image to a BytesIO object
#                 buffer = BytesIO()
#                 img.save(buffer, 'PNG')
#                 buffer.seek(0)

#                 # Handle user profile creation
#                 user = request.user if request.user.is_authenticated else None
#                 if not user:
#                     # Create a temporary user if not logged in
#                     user = User.objects.create(username=user_registration.unit_name, email=user_registration.unit_address)

#                 user_profile, created = UserProfile.objects.get_or_create(user=user)
#                 user_profile.qr_code.save(f'{user_registration.unit_name}_qr_code_{user_registration.unit_id}.png', ContentFile(buffer.getvalue()))

#                 # Debugging: Check user_registration and user_profile
#                 print(f"user_registration: {user_registration}")
#                 print(f"user_profile: {user_profile}")

#                 context={
#                     'form': form,
#                     'user_profile': user_profile,
#                     'user_registration': user_registration
#                 }

#                 return render(request, 'user_profile.html', context)

#             except IntegrityError:
#                 error_message = "Username already exists. Please choose a different one."
#                 return render(request, 'register.html', {'form': form, 'error_message': error_message})

#     else:
#         form = UserRegistrationForm()

#     return render(request, 'register.html', {'form': form})



# @csrf_exempt
# def user_data_api(request, user_id):
#     try:
#         user_registration = UserRegistration.objects.get(id=user_id)

#         # Using __dict__ to fetch all fields of the user_registration object
#         data = user_registration.__dict__

#         # Remove unnecessary fields like '_state' which are internal to Django models
#         data.pop('_state', None)

#         return JsonResponse(data)

#     except UserRegistration.DoesNotExist:
#         return JsonResponse({"error": "User not found"}, status=404)

@csrf_exempt
def user_data_api(request, user_id):
    try:
        # Fetch the UserRegistration object
        user_registration = UserRegistration.objects.get(id=user_id)

        # Fetch related Expenditure objects
        expenditures = Expenditure.objects.filter(user_registration=user_registration)

        # Prepare expenditure data as a list of dictionaries
        expenditure_data = list(expenditures.values(
            'sl_no',
            'item_description',
            'qty',
            'qty_type',
            'tax_type',
            'base_amount',
            'tax_amount',
            'amount',
        ))

        # Prepare response data
        data = user_registration.__dict__
        data.pop('_state', None)  # Remove Django's internal field

        # Add expenditure data to the response
        data['expenditures'] = expenditure_data

        return JsonResponse(data)

    except UserRegistration.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


