from django.shortcuts import render, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Profile, PhoneNumber
from django.core.mail import send_mail
from decouple import config
from django.conf import settings
import random
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_gen
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .forms import ResetEmailForm

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

#africanstalking api
from decouple import config
import africastalking
username= config("username")
api_key = config("api_key")
africastalking.initialize(username, api_key)
sms_provider = africastalking.SMS

def LogInView(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        if username == "":
            messages.error(request, "Username required")
        if password == "":
            messages.error(request, "Password is required")
        
        user = authenticate(request, username=username, password=password)
            
        if user is not None:
            login(request, user)
            messages.info(request, "You have successfully logged in")
            
            # user_phone = PhoneNumber.objects.get(user = request.user)
            
            # #phone verification 
            # if user_phone.is_verified == False:
            #     phone_no = user_phone.phone
            #     sms = sms_provider
            #     sender_id = "DjangoAuth"
            #     sms_content = f"{user_phone.otp} is your verification code"
            #     recipients = [str(user_phone.phone)]
            #     response = sms.send(sms_content, recipients)
            #     return HttpResponseRedirect(reverse())
            return redirect('movies:index')
        else:
            messages.error(request,"Ivalid Login")
            return render(request,'auth/login.html')
    return render(request, 'auth/login.html', {})

def LogOutView(request, *args, **kwargs):
    logout(request)
    messages.success(request,"You have successfully Logged Out")
    return redirect('movies:index')

def RegisterView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        subscribe = request.POST.get('subscribe')
        
        if username == "":
            messages.error(request, "Username is required")
            return redirect('user:register')
        if email == "":
            messages.error(request, "Email is required")
            return redirect('user:register')
        if phone == "":
            messages.error(request, "Phone is required")
            return redirect('user:register')
        if password1 == "":
            messages.error(request, "Password is required")
            return redirect('user:register')
        if password2 == "":
            messages.error(request, "Repeat Password is required")
            return redirect('user:register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "A user with the username exists")
            return redirect('user:register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "The Email has already been taken")
            return redirect('user:register')
        if  Profile.objects.filter(phone=phone).exists():
            messages.error(request, "The phone number already exists")
            return redirect('user:register')

        
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('user:register')
        if len(password1)<6:
            messages.error(request,"Password is too short")
            return redirect('user:register') 
            
                
        else:
            user = User.objects.create_user(username=username, 
                                            email=email, 
                                            )
            user.set_password(password1)
            user.is_active=False
            user.save()
            
            profile = Profile.objects.get(user=user)
            profile.phone = phone
            phone_database = PhoneNumber(user=user,
                                     phone_number=phone,
                                     otp = random.randint(100000,999999),
                                     is_verified=False)
            phone_database.save()
            profile.save()

            
            
            
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain #gives us the domain
            link = reverse('user:activate', 
                            kwargs={
                                'uidb64':uidb64, 
                                'token':token_gen.make_token(user)
                                    })
            activate_url = f"http://{domain+link}"
            
            mail_subject = "Activate your account"
            
            """
            message = render_to_string('auth/activate.html', {
                'user':user,
                'domain':domain,
                'uidb64':uidb64,
                'token':token_gen.make_token(user)
            })
            """
            
            mail_body = f"hi {user.username} click the link below to verify your account\n {activate_url}"
            mail = send_mail (mail_subject, mail_body,'noreply@retech.com',[email], fail_silently=False)
            messages.success(request, "Verification email has been sent to your email")
            return redirect('user:login')
            
    return render(request, 'auth/register.html', {})


def VerificationView(request,uidb64, token):

    uidb = force_text(urlsafe_base64_decode(uidb64)) or None
    user = User.objects.get(pk=uidb) or None

        
    if user is not  None and token_gen.check_token(user, token):
        user.is_active=True
        user.save()
        messages.info(request, "account verified")  
        return redirect("user:login")
    messages.error(request, "Oops, Something is wrong with the link, Please request anaother")
    return render(request,'auth/login')


def RequestResetEmail(request):
    if request.method == 'POST':
        form = ResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
        
    
            user = User.objects.filter(email=email)
        
            if user.exists():
                uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
                domain = get_current_site(request).domain #gives us the domain
                link = reverse('user:reset-password', 
                                kwargs={
                                    'uidb64':uidb64, 
                                    'token':PasswordResetTokenGenerator().make_token(user[0])
                                        })
                reset_password_url = f"http://{domain+link}"
                
                mail_subject = "Reset Password"
                
                """
                message = render_to_string('auth/activate.html', {
                    'user':user.username,
                    'url':activate_url,
                })
                """
                
                mail_body = f"hi {user[0].username} click the link below to reset your password\n {reset_password_url}"
                mail = send_mail (mail_subject, mail_body,'noreply@retech.com',[email], fail_silently=False)
                messages.success(request, "Check your Email for the reset link")
                return redirect('user:login')
            else:
                messages.error(request, "Sorry, there is no user with that email")
                return redirect('user:request-reset-email')

    return render(request, 'auth/reset-password-form.html')
  
def ResetPasswordView(request, uidb64, token):
    context = {
        'uidb64':uidb64, 
        'token':token
        }
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            messages.error(request, "Opps, The link has expired")
            return render(request, 'auth/reset_email_form.html', {})
            
        
        messages.success(request, "password changed successfully")
        return redirect('user:login')
    except DjangoUnicodeDecodeError as identifier:
        messages.error(request, "oops! something went wrong")
        return render(request, 'auth/reset_password.html', context)
    
    
    if request.method == 'POST':
        context = {
            'uidb64':uidb64,
            'token':token,
        }
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == "":
            messages.error(request, "Password is required")
        if password2 == "":
            messages.error(request, "Repeat Password is required")
            return render(request, 'auth/reset_password.html', context)
        if password1 != password2:
            messages.error(request, "Passwords do not match")
        if len(password1)<6:
            messages.error(request,"Password is too short")
            return render(request, 'auth/reset_password.html', context)
        if password1 != password2:
            messages.error(request, "Passwords do not match")
        if len(password1)<6:
            messages.error(request,"Password is too short")
            return render(request, 'auth/reset_password.html', context)  
        
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password1)
            user.save()
            messages.success(request, "password changed successfully")
            return redirect('user:login')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, "oops! something went wrong")
            return render(request, 'auth/reset_password.html', context)
    return render(request, 'auth/reset_password.html', context)