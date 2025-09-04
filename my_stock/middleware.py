# my_stock/middleware.py
from django.http import HttpResponseForbidden

class BlockBotsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        blocked_bots = [
            'twitterbot',
            'applebot',
            'trendictionbot',
            'googlebot',
            'bingbot',
            'yandexbot',
            'facebookexternalhit',
        ]
        if any(bot in user_agent for bot in blocked_bots):
            return HttpResponseForbidden("Bot access denied.")
        return self.get_response(request)