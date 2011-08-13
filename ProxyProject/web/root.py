



from txweb import expose
from static import relPath, ROOT, JS, CSS
from twisted.web.static import File
from twisted.python.rebuild import Sensitive
from twisted.web.server import NOT_DONE_YET
import render
from cgi import escape
from urllib import unquote_plus

def SessionDict(request):
    #Candidate for a txweb.Request class getSessionData perhaps?
    session = request.getSession()
    if not hasattr(session, "data"):
        session.data = dict()
        
    return session.data
        

class Hosts(object, Sensitive):

    store = None
    
    @expose
    def index(self, request):
        return self.list(request)
                
    
    @expose    
    def list(self, request):
        session_data = SessionDict(request)
        
        def response(*args):
            #Check if the client timed out
            if not request.finished:
                session_data['ts'] = request.store.lastChange
                hosts = request.site.store.getHostCount()
                
                view = render.byMako("root/list_hosts")
                request.write( view.render( hosts = hosts ) )
                try:
                    request.finish()
                except:
                    pass
                    #todo find a better way of cancelling expired responses
            
        
        if session_data.get('ts',0) < request.store.lastChange:
            response()
        else:
            request.site.store.onChange(response)
        
        return NOT_DONE_YET
        
        
    @expose
    @render.asMako("hosts/uri_details")
    def uri(self, request):
        postpath = request.postpath
        
        domain = request.postpath[0]
        path   = unquote_plus(request.postpath[1])
        
        uris = request.site.store.getTRXByHostURI(domain, path)
        data = dict(uris = uris)
        data['args'] = request.args
        data['post'] = postpath
        return data
        
    @expose
    @render.asMako("hosts/sessions")
    def sessions(self, request):
        if len(request.postpath) <= 0:
            return "Missing host name in URL"
        
        host = request.postpath[-1]
        data = request.site.store.getURISByHost(host)
        return data
        
        


class Root(object, Sensitive):
    
    store = None
    
    def __init__(self, store):
        self.store = store
        self.hosts.store = store
    
    index = File(ROOT)
    css = File(CSS)
    js  = File(JS)
    
    
    hosts = Hosts()
    
    
    
    
    