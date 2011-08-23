"""
    Similar to most MVC frameworks, Base Controller builds up a common
    list of imports, decorators, and class methods (mixins too)
"""


from twisted.python.rebuild import Sensitive
from twisted.web.server import NOT_DONE_YET
from txweb.util import expose

from ProxyProject.web import render

from contextlib import contextmanager

class Base(object, Sensitive):
    pass
    
    @contextmanager
    def getSessionData(self, request):
        session = request.getSession()
        if not hasattr(session, "data"):
            session.data = {}
        data = session.data
        yield data
        session.data = data