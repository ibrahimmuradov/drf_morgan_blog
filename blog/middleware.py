from threading import local

_thread_locals = local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

class ThreadLocalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.user = request.user
        response = self.get_response(request)
        return response
