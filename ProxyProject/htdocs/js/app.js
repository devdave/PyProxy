
    /**
    * Base namespace for classes, utilities, and stuff
    */
    var lib = {};
    
    lib.HostDetail = function(parent, menu, host, remote_url, jQuery){
        var self = this;
        self.parent = parent;
        self.menu  = menu;
        self.host = host;
        self.clean_host = host.replace(".", "_");
        self.remote_url = remote_url;
        self.element_id = "tabpanel-" + self.clean_host;
        
        if(jQuery(self.element_id).length == 0){
            self.page = jQuery("<div></div>").attr("id", self.element_id).data("handler", self).hide();        
        }else{
            self.page = jQuery(self.element_id); 
        }
        self.menu
        var priv = {
            fetchHostdetail : function(){
                jQuery.ajax(self.remote_url)
                    
                    .success(function(){
                        
                        self.menu.append(self.page);
                        self.menu.tabs("add", "#" + self.page.attr("id"), self.host );
                        self.page.show()
                    })
                    .failure(function(){
                        console.error("Failed to detail " , arguments);
                    })
                
            }
        }
        
        priv.fetchHostdetail();
        
    }
    
    lib.Main = function(parent, box, jQuery){
        var self = this;
        this.pollSwitch = box.find("#pollOn");        
        this.tbody = box.find("tbody");
        
        //@todo find a better way
        this.tmpl = tmpl("main_hostCountRow");
        var priv = {
            pollHandle: null
            , pollON: true
            , isPolling: false
            , storeTS: 0
            , pollHosts: function(){
                if(priv.isPolling){
                    return;
                }
                priv.isPolling = true;
                
                priv.pollHandle = $.ajax("/simple/host_count", {dataType: "json", data: {"ts": priv.storeTS } } )
                    .success(function(response){
                        if(response.success){
                            priv.ts = response.ts;
                            self.tbody.empty();                            
                            for(i = 0; i < response.hosts.length; i++){
                                self.tbody.append(self.tmpl(response.hosts[i]));
                            }
                        }
                    })
                    .complete(function(response){
                        priv.isPolling = false;                        
                        priv.pollHandle = null;
                        if(priv.pollON){
                            setTimeout(priv.pollHosts, 3000);                        
                        }
                        
                    });
            }
        }
        
        
        this.onHostClick = function(){
            var hostName = $(this).data("host");
            new lib.HostDetail(self, parent.menu, hostName, "/simple/describe?host=" + hostName, jQuery);
        }
        
        this.pollSwitch.change(function(){
            if(this.checked == false){
                priv.pollON = false;
                priv.isPolling = false;
                if(priv.pollHandle){                    
                    priv.pollHandle.abort();
                }
            }else{
                priv.pollON = true;
                priv.pollHosts();
            }
        });
        
        jQuery("a.hostClick").live("click", this.onHostClick);
        
        priv.pollHosts();
        
    }
    

    /**
    *@class lib.App The central god module for the console
    *@param object jQuery a Valid jQuery instance
    *@param a valid jQuery managed refernce to the Main html panel div/span/thing    
    */
    lib.App = function(jQuery, main, menu){
            var self = this;
            this.menu = menu;
            this.menu.tabs();
            try{
                this.main = new lib.Main(self, main, jQuery)
            }catch(e){
                console.error(e);
            }
            
            
            this.templates = {};
            
            
            this.setTemplate = function(name, id){
                self.templates[name] = tmpl(id);
            };
            
            
            
        };