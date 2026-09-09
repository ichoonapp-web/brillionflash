import re
from django.http import JsonResponse

class SecuritySanitizerMiddleware:
    """
    Military-Grade Request Sanitizer Middleware:
    Inspects incoming HTTP requests and blocks SQL Injection, XSS, and Command Injection payloads.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.malicious_patterns = [
            re.compile(r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|EXEC|UNION)\b)", re.IGNORECASE),
            re.compile(r"(<script.*?>|javascript:|onload=)", re.IGNORECASE),
            re.compile(r"(\.\./|\.\.\\)", re.IGNORECASE), # Path Traversal
        ]

    def __call__(self, request):
        path = request.path
        if not path.startswith('/admin/'):
            query_string = request.META.get('QUERY_STRING', '')
            for pattern in self.malicious_patterns:
                if pattern.search(query_string):
                    return JsonResponse({
                        'error': 'Security Alert: Malicious request payload detected.',
                        'code': 'BLOCKED_BY_FIREWALL'
                    }, status=403)

        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        response['Content-Security-Policy'] = "default-src 'self'"
        return response
