from django.contrib import messages
from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Data, User

# Create your views here.


def index(request):
    datas = Data.objects.all()
    return render(
        request,
        "data/index.html",
        {
            "datas": datas,
        },
    )


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "data/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "data/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "data/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "data/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "data/register.html")


def addData(request):
    return render(request, "data/add.html")


def dashboard(request):
    currentUser = request.user
    datas = Data.objects.filter(owner=currentUser)
    return render(
        request,
        "data/dashboard.html",
        {
            "datas": datas,
        },
    )


@login_required(
    login_url="/login/"
)  # Add the login_required decorator to ensure the user is authenticated
def saveData(request):
    currentUser = request.user
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        city = request.POST["city"]
        country = request.POST["country"]
        newData = Data(
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
            city=city,
            country=country,
            owner=currentUser,
        )
        newData.save()
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login/")  # Add
def editData(request, id):
    data = Data.objects.get(pk=id)
    return render(
        request,
        "data/edit.html",
        {
            "data": data,
        },
    )


@login_required(login_url="/login/")  # Add
def saveEdit(request, id):
    data = Data.objects.get(pk=id)
    if request.method == "POST":
        data.firstname = request.POST.get("firstname", data.firstname)
        data.lastname = request.POST.get("lastname", data.lastname)
        data.email = request.POST.get("email", data.email)
        data.phone = request.POST.get("phone", data.phone)
        data.city = request.POST.get("city", data.city)
        data.country = request.POST.get("country", data.country)
        data.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


def deleteData(request, id):
    data = Data.objects.get(pk=id)
    data.delete()
    return HttpResponseRedirect(reverse("dashboard"))
