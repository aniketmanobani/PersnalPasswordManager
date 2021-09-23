import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from homeapp.models import PasswordStore


@login_required(login_url='login')
def index(request):
    ps = PasswordStore.objects.filter(user_id=request.user).order_by('-id')
    page = request.GET.get('page', 1)
    no_of_item = 10
    paginator = Paginator(ps, no_of_item)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'list': list})


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
                messages.warning(
                    request, "Authentication error, please try again")
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

    recent = PasswordStore.objects.filter(
        user_id=request.user).order_by('-id')[:10]
    return render(request, 'create_password.html', {'recent': recent, 'range': range(10)})


@login_required(login_url='login')
def viewDetails(request, id):
    p = PasswordStore.objects.filter(user_id=request.user, id=id)
    showPassword = False

    if request.method == "POST":
        if 'password' in request.POST.keys() and len(request.POST.get('password')) > 0:
            verifyPass = auth.authenticate(
                username=request.user.username, password=request.POST.get('password'))
            if verifyPass is not None:
                showPassword = True
            else:
                messages.warning(request, "Incorrect Password")
    if p.exists():
        print(p)
        return render(request, 'viewdetails.html', {'info': p[0], 'showPassword': showPassword})
    else:
        return render(request, 'not_found.html')
    return render(request, 'viewdetails.html')


@login_required(login_url='login')
def appsPassword(request):
    ps = PasswordStore.objects.filter(
        user_id=request.user, app_type='apps').order_by('-id')
    page = request.GET.get('page', 1)
    no_of_item = 10
    paginator = Paginator(ps, no_of_item)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request, 'apps_password.html', {'list': list})


@login_required(login_url='login')
def websitePassword(request):
    ps = PasswordStore.objects.filter(
        user_id=request.user, app_type='website').order_by('-id')
    page = request.GET.get('page', 1)
    no_of_item = 10
    paginator = Paginator(ps, no_of_item)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request, 'website_passwords.html', {'list': list})


@login_required(login_url='login')
def otherPassword(request):
    ps = PasswordStore.objects.filter(
        user_id=request.user, app_type='others').order_by('-id')
    page = request.GET.get('page', 1)
    no_of_item = 10
    paginator = Paginator(ps, no_of_item)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request, 'others_password.html', {'list': list})


@csrf_exempt
@login_required(login_url='login')
def deletePass(request, id):
    if request.method == "POST":
        if 'password' in request.POST.keys():
            print(request.POST.get('password'))
            au = auth.authenticate(
                username=request.user.username, password=request.POST.get('password'))
            if au is not None:
                p = PasswordStore.objects.filter(user_id=request.user, id=id)
                if p.exists():
                    p.delete()
                    print("del")
                    return HttpResponse("Deleted")
                else:
                    print('not del')
                    return HttpResponse("Password Does Not Match")
            else:
                return HttpResponse("Password Does Not Matched")

    return HttpResponse("Post method is required")


@login_required(login_url='login')
def editpass(request, id):
    p = PasswordStore.objects.filter(user_id=request.user, id=id)
    if p.exists():
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
                pt = PasswordStore.objects.filter(user_id=request.user, id=id)
                app_or_web = formData.get('app_web_name')
                apptype = formData.get('apptype')
                password = formData.get('createpassword')

                pt = pt[0]
                pt.apptype = apptype
                pt.app_or_web = app_or_web
                pt.email = email
                pt.username = username
                pt.app_pass = password
                pt.other_detail = otherDetails
                pt.updated_on = datetime.date.today()
                pt.save()
                messages.warning(request, "Changes Saved Succesfully")
        return render(request, 'editapps.html', {'info': p[0]})
    else:
        return render(request, 'not_found.html')


@login_required(login_url='login')
def search(request):
    if "search_text" in request.GET.keys() and len(request.GET.get('search_text')) > 0:
        search_text = request.GET.get('search_text')
        res = PasswordStore.objects.filter(app_or_web__contains=search_text).order_by('-id')[:50]
        return render(request, "search.html",{'search_text':search_text,'res':res})

    return render(request, "search.html")


@login_required(login_url='login')
def profile(request):
    return render(request,'profile.html')

@login_required(login_url='login')
def settings(request):
    return render(request,'settings.html')