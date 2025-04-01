from django.shortcuts import render
from django.contrib.auth import login
from .forms import RegisterForm


def register(request):
    if request.method == "post":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return "shop/index"
    else:
        form = RegisterForm()
    return render(request, "account/register.html", {"form": form})
