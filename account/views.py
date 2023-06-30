from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def edit(request):
    return render(request, 'account/edit_details.html', {})


def login(request):
    return render(request, 'account/login.html', {})

def register(request):
    return render(request, 'account/register.html', {})
