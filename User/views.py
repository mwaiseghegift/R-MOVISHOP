from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponseRedirect
# Create your views here.

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
            return redirect('products:index')
        else:
            messages.error(request,"Ivalid Login")
            return render(request,'auth/login.html')
    return render(request, 'auth/login.html', {})