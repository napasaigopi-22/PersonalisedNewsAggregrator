from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
# from django.conf import settings
from userauths.models import User
from django.contrib.auth import logout

# User=settings.AUTH_USER_MODEL

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            current_level = messages.get_messages(request)
            print("\n\n\n\n\n\n\n\n",current_level)  # not recorded
            for i in current_level:
                print(current_level)
            messages.success(request, f"Hey {username}, your account was created successfully")

            new_user = authenticate(username=form.cleaned_data['email'], 
                                    password=form.cleaned_data['password1'])
            
            login(request, new_user)
            return redirect("core:index")
    else:
        form=UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'userauths/sign-up.html', context)

def login_view(request):
    #email-numamahesh2000@gmail.com, password- 6_PK8Mg-6A25pZ6
    if request.user.is_authenticated:
        current_level = messages.get_messages(request)
        print("\n\n\n\n\n\n\n\n",current_level)  # not recorded
        for i in current_level:
            print(current_level)
        messages.warning(request,f"Hey, You are already Logged in")
        return redirect('core:index')
    else:
        if request.method=="POST":
            email=request.POST.get("email")
            password=request.POST.get("password")
            current_level = messages.get_messages(request)
            print("\n\n\n\n\n\n\n\n",current_level)  # not recorded
            for i in current_level:
                print(current_level)
            # try:
            #     print("user object")
            #     user=authenticate(request,email=email,password=password)
            #     print('authenticate',user)
            #     user=User.objects.get(email=email)
            #     print("user is --------~~~~~~~~~~~~~~~~~~~~~~~~",user)
            # except:
            #     current_level = messages.get_messages(request)
            #     print("\n\n\n\n\n\n\n\n",current_level)  # not recorded
            #     for i in current_level:
            #         print(current_level)
            #     messages.warning(request,f"User with {email} does not exist")
            #     return render(request,"userauths/sign-in.html")
                

            user=authenticate(request,email=email,password=password)
            print("use ris ",user)
            if user is not None:
                login(request,user)             
                return redirect("core:index")
            
            else:
                current_level = messages.get_messages(request)
                print("\n\n\n\n\n\n\n\n",current_level)  # not recorded
                for i in current_level:
                    print(current_level)
                # messages.warning(request,"User Does not exist, create an account")
                messages.warning(request,f"User with {email} does not exist")

                
    return render(request,"userauths/sign-in.html")


def logout_view(request):
   
    logout(request)
    # messages.warning(request, None)  # recorded
    # messages.set_level(request, 0)
    
    current_level = messages.get_messages(request)
    print("\n\n\n\n\n\n\n\n",current_level)  # not recorded
    for i in current_level:
        print(current_level)
    # print("\n\n\n\n\n\n\n\n",current_level.message)  # not recorded
    messages.success(request, "You Logged-Out, successfully")
    return redirect("userauths:sign-in")

def home(request):
    return render(request,'base_auth.html')