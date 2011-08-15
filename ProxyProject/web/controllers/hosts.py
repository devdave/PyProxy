
from contextlib import contextmanager

from twisted.python.rebuild import Sensitive
from twisted.web.server import NOT_DONE_YET
from txweb.util import expose
from ProxyProject.web import render

from urllib import unquote_plus

@contextmanager
def getSessionData(request):
    session = request.getSession()
    if not hasattr(session, "data"):
        session.data = {}
    data = session.data
    yield data
    session.data = data
    

class Hosts(object, Sensitive):

    store = None
    @expose
    def index(self, request):
        return self.list(request)
    
    @expose    
    def list(self, request):
        #todo push the must and can helpers to txWeb
        ts = int(float(request.args.get('ts', [0])[0]))
        with getSessionData(request) as data:
            #be interesting to see how the context manager handles the inner method here
            
            
            def response(*args):                
                hosts = request.site.store.getHostCount()
                view = render.byMako("hosts/list")
                
                
                try:
                    request.write( view.render(hosts = hosts, ts = request.site.store.lastChange ) )
                    request.finish()    
                except Exception, e :
                    #NEed to find a better way of figuring out if the client timed out
                    #request.finished doesn't seem to be reliable
                    pass
            
            #round off the microseconds
            if ts >= int(request.site.store.lastChange):
                request.site.store.onChange(response)
            else:
                response()            
                
                
        
            return NOT_DONE_YET
        
            
            
    @expose
    @render.asMako("hosts/uri_details")
    def uri(self, request):
        postpath = request.postpath
        domain = request.postpath[0]
        uri    = unquote_plus(request.postpath[1])
        records = request.site.store.getTRXByHostURI(domain, uri)
        data = dict(uris = records)
        data['args'] = request.args
        data['post'] = postpath
        data['host'] = domain
        data['path'] = uri
        return data
        
    @expose
    @render.asMako("hosts/sessions")
    def sessions(self, request):
        if len(request.postpath) <= 0:
            return "Missing host name in URL"
        
        host = request.postpath[-1]
        data = request.site.store.getURISByHost(host)
        return data
