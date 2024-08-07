
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.urls import reverse
# from django.core.files.base import ContentFile
# from io import BytesIO
# import qrcode
# from .forms import UserRegistrationForm
# from .models import UserProfile, UserRegistration

# @login_required
# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user_registration = form.save()
            
#             # Generate the QR code
#             profile_url = request.build_absolute_uri(reverse('user_profile', args=[user_registration.id]))
#             qr = qrcode.QRCode(
#                 version=1,
#                 error_correction=qrcode.constants.ERROR_CORRECT_L,
#                 box_size=10,
#                 border=4,
#             )
#             qr.add_data(profile_url)
#             qr.make(fit=True)
#             img = qr.make_image(fill='black', back_color='white')

#             # Save the QR code image to a BytesIO object
#             buffer = BytesIO()
#             img.save(buffer, format='PNG')
#             buffer.seek(0)

#             # Create or update the user's profile with the QR code image
#             user_profile, created = UserProfile.objects.get_or_create(user=request.user)
#             user_profile.qr_code.save(f'{user_registration.unit_name}_qr_code_{user_registration.unit_id}.png', ContentFile(buffer.getvalue()))

#             # Redirect to the user profile page
#             return render(request, 'register.html', {'form': form, 'user_profile': user_profile})
#     else:
#         form = UserRegistrationForm()

#     return render(request, 'register.html', {'form': form})


from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm
from .models import UserProfile
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

@login_required
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_registration = form.save()
            
            # Generate the QR code with user data in key-value pair format
            qr_data = request.build_absolute_uri(reverse('user_profile', args=[user_registration.id]))
            # qr_data = f"unit_id:{user_registration.unit_id},unit_name:{user_registration.unit_name},unit_address:{user_registration.unit_address},dak_id:{user_registration.dak_id}"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')

            # Save the QR code image to a BytesIO object
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)

            # Create or update the user's profile with the QR code image
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.qr_code.save(f'{user_registration.unit_name}_qr_code_{user_registration.unit_id}.png', ContentFile(buffer.getvalue()))

            return render(request, 'register.html', {'form': form, 'user_profile': user_profile})
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})



from django.shortcuts import render, get_object_or_404
from .models import UserRegistration, UserProfile

def user_profile(request, user_id):
    user_registration = get_object_or_404(UserRegistration, id=user_id)
    
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, 'user_profile.html', {
        'user_registration': user_registration,
        'user_profile': user_profile
    })


