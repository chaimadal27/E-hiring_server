from .threadlocal import thread_local
from .mixins import GetTokenFromRequestHeaderMixin
"""
Swtich the middleware to change from
'Single Schema' to 'Multi Db' multitenancy
"""


class MultiDBMiddleware(GetTokenFromRequestHeaderMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        get_response = self.get_response

        db_name = self.get_db_name(request)
        if db_name is None:
            return get_response(request)
        
        @thread_local(using_db=db_name)
        def execute_request(request):
            return get_response(request)
        
        response = execute_request(request)
        
        return response
