import time
import threading
import logging
from django.http import HttpResponse, JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    REQUEST_LIMIT    = getattr(settings, 'RATE_LIMIT_REQUESTS', 5)
    TIME_WINDOW      = getattr(settings, 'RATE_LIMIT_WINDOW', 60)
    CLEANUP_INTERVAL = 300

    def __init__(self, get_response):
        self.get_response  = get_response
        self._clients      = {}
        self._lock         = threading.Lock()
        self._last_cleanup = time.time()

    def __call__(self, request):
        protected = ('/login', '/register')
        if any(request.path.startswith(p) for p in protected):
            ip  = self._get_client_ip(request)
            now = time.time()
            with self._lock:
                self._maybe_cleanup(now)
                timestamps = [t for t in self._clients.get(ip, []) if now - t < self.TIME_WINDOW]
                if len(timestamps) >= self.REQUEST_LIMIT:
                    retry_after = int(self.TIME_WINDOW - (now - timestamps[0]))
                    logger.warning("Rate limit atteint pour IP %s", ip)
                    return self._rate_limit_response(request, retry_after)
                timestamps.append(now)
                self._clients[ip] = timestamps
        return self.get_response(request)

    def _get_client_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')

    def _maybe_cleanup(self, now):
        if now - self._last_cleanup < self.CLEANUP_INTERVAL:
            return
        cutoff = now - self.TIME_WINDOW
        self._clients = {
            ip: [t for t in ts if t > cutoff]
            for ip, ts in self._clients.items()
            if any(t > cutoff for t in ts)
        }
        self._last_cleanup = now

    def _rate_limit_response(self, request, retry_after):
        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            return JsonResponse(
                {'error': f'Trop de tentatives. Réessayez dans {retry_after} secondes.'},
                status=429,
                headers={'Retry-After': str(retry_after)},
            )
        return HttpResponse(
            f'Trop de tentatives. Réessayez dans {retry_after} secondes.',
            status=429,
            headers={'Retry-After': str(retry_after)},
        )


class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start    = time.perf_counter()
        response = self.get_response(request)
        duration = time.perf_counter() - start
        response['X-Process-Time'] = f'{duration:.4f}s'
        if duration > 1.0:
            logger.warning("Requête lente (%.2fs) : %s %s", duration, request.method, request.path)
        return response


class AuthAccessMiddleware:
    PROTECTED_PREFIXES = (
        '/dashboard', '/users/dashboard',
        '/produits/', '/commandes/', '/stock/', '/statistiques/',
    )

    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url    = getattr(settings, 'LOGIN_URL', '/login')

    def __call__(self, request):
        if not request.user.is_authenticated:
            if any(request.path.startswith(p) for p in self.PROTECTED_PREFIXES):
                from django.shortcuts import redirect
                from django.urls import reverse
                login_url = reverse('users:login')
                return redirect(f'{login_url}?next={request.path}')
        return self.get_response(request)