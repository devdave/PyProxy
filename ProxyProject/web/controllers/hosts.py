

from ProxyProject import data

from urllib import unquote_plus

from base import *

#todo add 2 base
from mako import exceptions
    

class Hosts(Base):

    store = None
    @expose
    def index(self, request):
        return self.list(request)
    
    @expose    
    def list(self, request):
        #todo push the must and can helpers to txWeb
        ts = int(float(request.args.get('ts', [0])[0]))
        with self.getSessionData(request) as session:
            #be interesting to see how the context manager handles the inner method here
            
            
            def response(*args):
                view = {}
                view['hosts'] = request.site.store.getHostCount()                
                view['list_actions'] = {}
                view['page_actions'] = {}
                view['ts'] = request.site.store.lastChange
                data.bus.call("web.hosts.list", self, view)
                template = render.byMako("hosts/list")
                try:
                    request.write( template.render(**view) )
                    
                except Exception, e :
                    request.write( exceptions.html_error_template().render() )
                    
                try:
                    request.finish()
                except Exception, e:
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
        view = {}
        view['uris'] = records
        view['args'] = request.args
        view['post'] = postpath
        view['host'] = domain
        view['path'] = uri
        view['uri_actions'] = {}
        view['page_actions'] = {}
        data.bus.call("web.hosts.uri", self, view)
        return view
        
    @expose
    @render.asMako("hosts/sessions")
    def sessions(self, request):
        if len(request.postpath) <= 0:
            return "Missing host name in URL"
        
        
            
        host = request.postpath[-1]
        payload = request.site.store.getURISByHost(host)
        
        def getContentTypes(uri):
        #relocate into view
            mapper = lambda record : record.response['headers']['Content-Type']
            unique = set()
            allTypes = request.site.store.map2uri( host,uri, mapper )
            unique.update( allTypes )
            return [x for x in unique]
        
        view = {}
        view.update(payload)        
        view['getContentTypes'] = getContentTypes
        view['store'] = request.site.store
        
        #Additional bindings for plugins
        view['session_actions'] = {}
        view['page_actions'] = {}
        data.bus.call("web.hosts.sessions", self, view)
        return view

    @expose
    @render.asMako("hosts/response")
    def record(self, request):    
        view = {}
        if len(request.postpath) <= 0:            
            view['record'] = None
            view['error'] = "Missing record.id"
            record = None
        else:        
            view['record_id'] = request.postpath[0]
            view['record'] = request.site.store.getRecordById(view['record_id'])
        
        
        if view['record'] is None:                         
            view['body'] = view['host'] = "Bad or missing record.id"
            view['error'] = "Unable to find requested record.body"
        else:
            view['body'] = record.getBody()
            view['host'] = record.host
        
        
        return view