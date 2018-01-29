from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.shortcuts import redirect


def callback(request: HttpRequest):
    if 'code' not in request.GET:
        return redirect('index')

    capsuleer = authenticate(request, code=request.GET['code'])

    if capsuleer is not None:
        login(request, capsuleer)

    return redirect('index')


def sso_logout(request):
    logout(request)
    return redirect('index')


def sso_login(request):
    return redirect(
        'https://login.eveonline.com/oauth/authorize?response_type=code&redirect_uri=http://localhost:8000/auth/callback&client_id=27487b15c8c540a2b446484b3dcd877f&scope=esi-location.read_location.v1')
