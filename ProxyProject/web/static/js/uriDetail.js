
lib._loadedURIS = {}

lib.RequestURIDetail = function(parent, menu, host, uri, jQuery){
                        if( typeof lib._existsDetails[host] == "undefined"){
                            lib._existsDetails[host+uri] = new lib.UriDetail(parent, menu, host, url, jQuery);
                        }
                        return lib._existsDetails[host+uri].load();                        
                        };
                        
lib.UriDetail = function(parent, menu, host, uri, jQuery){
                    var self = this;
                    self.loaded = false;
                    self.parent = parent;
                    self.menu = menu;
                    self.host = host;
                    self.uri = uri;
                    self.element_id = self.host.replace(/\./g,"_") + self.uri.replace(/\//g, "_")
                    
                    if( jQuery("#" + self.element_id)
                }