import time
from django.http import HttpResponse


class RateLimitMiddleware:
    """Limiter les tentatives sur login et register"""

    REQUEST_LIMIT = 3
    TIME_WINDOW = 60  

    def __init__(self, get_response):
        self.get_response = get_response
        self.clients = {}

    def __call__(self, request):
        if request.path.startswith('/login') or request.path.startswith('/register'):
            ip = request.META.get('REMOTE_ADDR')
            now = time.time()
            if ip not in self.clients:
                self.clients[ip] = []
            self.clients[ip] = [t for t in self.clients[ip] if now - t < self.TIME_WINDOW]

            if len(self.clients[ip]) >= self.REQUEST_LIMIT:
                return HttpResponse("Trop de tentatives, réessayez plus tard.", status=429)

            self.clients[ip].append(now)

        return self.get_response(request)


import time

class TimingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start = time.time()

        response = self.get_response(request)

        duration = time.time() - start

        print(f"{request.path} → {duration:.3f}s")

        response['X-Process-Time'] = f"{duration:.3f}s"

        return response


from django.shortcuts import redirect


class AuthAccessMiddleware:
    """Middleware pour bloquer les accès non autorisés"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/dashboard') or request.path.startswith('/users/dashboard'):
            if not request.user.is_authenticated:
                return redirect('/login')
        return self.get_response(request)
