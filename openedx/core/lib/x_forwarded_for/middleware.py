"""
Middleware to use the X-Forwarded-For header as the request IP.
Updated the libray to use HTTP_HOST and X-Forwarded-Port as
SERVER_NAME and SERVER_PORT.
"""
from django.utils.deprecation import MiddlewareMixin


class XForwardedForMiddleware(MiddlewareMixin):
    """
    Gunicorn 19.0 has breaking changes for REMOTE_ADDR, SERVER_* headers
    that can not override with forwarded and host headers.
    This middleware can be used to update these headers set by proxy configuration.

    """

    def process_request(self, request):
        """
        Process the given request, update the value of REMOTE_ADDR, SERVER_NAME and SERVER_PORT based
        on X-Forwarded-For, HTTP_HOST and X-Forwarded-Port headers
        """

        for field, header in [("HTTP_X_FORWARDED_FOR", "REMOTE_ADDR"), ("HTTP_HOST", "SERVER_NAME"),
                              ("HTTP_X_FORWARDED_PORT", "SERVER_PORT")]:
            if field in request.META:
                if ',' in request.META[field]:
                    request.META[header] = request.META[field].split(",")[0].strip()
                else:
                    request.META[header] = request.META[field]

        return None


from cProfile import Profile
from pstats import Stats


class ProfilingMiddleware(MiddlewareMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prof = None

    def process_request(self, request):
        if request.GET.get('profile_name'):
            self.prof = Profile()
            self.prof.enable()
        print("MIKE: profile", request.GET.get('profile_name'))

    def process_response(self, request, response):
        if self.prof:
            self.prof.disable()
            s = Stats(self.prof)
            s.dump_stats(request.GET['profile_name'])

        self.prof = None
        return response
