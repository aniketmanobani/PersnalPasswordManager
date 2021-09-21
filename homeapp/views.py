import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages, auth

# Create your views here.
from homeapp.models import PasswordStore


@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        errors = {}
        if 'email' not in request.POST.keys() or request.POST.get('email') == "":
            errors['email'] = "Email is required"

        if 'password' not in request.POST.keys() or request.POST.get('password') == "":
            errors['password'] = "Password is required"

        if errors:
            for e in errors.values():
                messages.warning(request, e)
            return render(request, 'login.html')
        else:
            print(request.POST.get('email'), request.POST.get('password'))
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = auth.authenticate(username=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                messages.warning(request, "Email or password is wrong")
                return render(request, 'login.html')
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        errors = {}
        if 'firstname' not in request.POST.keys() or request.POST.get('firstname') == "":
            errors['firstname'] = "Firstname is required"
        if 'email' not in request.POST.keys() or request.POST.get('email') == "":
            errors['email'] = "Email is required"

        if 'password' not in request.POST.keys() or request.POST.get('password') == "":
            errors['password'] = "Password is required"

        if 'rpassword' not in request.POST.keys() or request.POST.get('rpassword') == "":
            errors['password'] = "Repeat Password is required"

        if request.POST.get('rpassword') != request.POST.get('password'):
            errors['rpassword'] = "Repeat Password is is diffrent"

        if len(request.POST.get('password')) < 6:
            errors['password'] = 'Password should be atleast 6 character'

        if 'username' not in request.POST.keys() or request.POST.get('username') == "":
            errors['username'] = "username is required"
        else:
            if not request.POST['username'].isalnum():
                errors['username'] = "AlphaNumeric is required only"

        if len(request.POST.get('username')) < 6:
            errors['username'] = 'Username should be atleast 6 character'

        if User.objects.filter(username=request.POST.get('username')):
            errors['username'] = 'User is Alerady Exist'

        if User.objects.filter(email=request.POST.get('email')):
            errors['email'] = 'Email is Alerady Exist'

        if errors:
            for m in errors.values():
                messages.warning(request, m)
            return render(request, 'register.html')
        else:
            firstname = request.POST.get('firstname')
            username = request.POST.get('username')
            lastname = ""
            if 'lastname' in request.POST.keys():
                lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname,
                                            last_name=lastname)
            user.save()
            a = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                messages.warning(request, "Authentication error, please try again")
                render(request, 'register.html')

    return render(request, 'register.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect(index)


@login_required(login_url='login')
def createPassword(request):
    if request.method == "POST":
        formData = request.POST
        errors = {}
        email = ""
        username = ""
        otherDetails = ''
        if 'apptype' not in formData.keys() or len(formData.get('apptype')) < 2:
            errors['apptype'] = "App Type is required"
        if 'createpassword' not in formData.keys() or formData.get('createpassword') == "":
            errors['password'] = 'Password field is required'
        if 'email' in formData.keys():
            email = formData.get('email')
        if 'username' in formData.keys():
            username = formData.get('username')
        if 'otherDetails' in formData.keys():
            otherDetails = formData.get('otherDetails')

        if 'app_web_name' not in formData.keys() or len(formData.get('app_web_name')) < 2:
            errors['app_web_name'] = "App/Website name is required"

        if errors:
            for e in errors.values():
                messages.warning(request, e)
        else:
            app_or_web = formData.get('app_web_name')
            apptype = formData.get('apptype')
            password = formData.get('createpassword')
            pm = PasswordStore(user_id=request.user, username=username, app_or_web=app_or_web, email=email,
                               other_detail=otherDetails,
                               app_type=apptype, app_pass=password, updated_on=datetime.date.today())
            is_saved = pm.save()
            print(is_saved)
            messages.warning(request, "Password Saved Succesfully")
            # return render(request, 'create_password.html')

    recent = PasswordStore.objects.filter(user_id=request.user).order_by('-id')[:10]
    return render(request, 'create_password.html', {'recent': recent, 'range': range(10)})


@login_required(login_url='login')
def viewDetails(request, id):
    p = PasswordStore.objects.filter(user_id=request.user, id=id)
    showPassword = False

    if request.method == "POST":
        if 'password' in request.POST.keys() and len(request.POST.get('password')) > 0:
            verifyPass = auth.authenticate(username=request.user.username, password=request.POST.get('password'))
            if verifyPass is not None:
                showPassword = True
    if p.exists():
        print(p)
        return render(request, 'viewdetails.html', {'info': p[0], 'showPassword': showPassword})
    else:
        return render(request, 'not_found.html')
    return render(request, 'viewdetails.html')
