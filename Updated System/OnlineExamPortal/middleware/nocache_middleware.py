from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.utils.deprecation import MiddlewareMixin

class NoCacheMiddleware(MiddlewareMixin):
    @method_decorator(cache_control(no_cache=True, no_store=True, must_revalidate=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
