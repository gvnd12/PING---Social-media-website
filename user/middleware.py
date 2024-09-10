from django.utils.deprecation import MiddlewareMixin
import re

class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        dm_pattern = re.compile(r'^/dm/\d+/$')
        
        if request.path == '/notifications/' or dm_pattern.match(request.path):
            response['X-Frame-Options'] = 'ALLOWALL'
        else:
            response['X-Frame-Options'] = 'DENY'
        
        return response