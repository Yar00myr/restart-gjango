from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, ProfileUpdateForm
from .models import Profile


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("shop:home")
    else:
        form = RegisterForm()
    return render(request, "account/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get("next")
            return redirect(next_url or "shop:home")
        else:
            return render(
                request, "account/login.html", {"error": "incorrect login or password"}
            )
    else:
        return render(request, "account/login.html")


def logout_view(request):
    logout(request)
    return redirect("shop:home")


@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, "account/profile.html", {"profile": profile})


@login_required
def edit_profile_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            new_email = form.cleaned_data.get("email")
            user.email = new_email
            user.save()

            avatar = form.cleaned_data.get("avatar")
            if avatar:
                profile.avatar = avatar
            profile.save()
            return redirect("account:profile")
    else:
        form = ProfileUpdateForm()

    return render(request, "account/edit_profile.html", {"form": form})
