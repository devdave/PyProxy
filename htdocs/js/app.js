
    /**
    * Base namespace for classes, utilities, and stuff
    */
    var lib = {};
    
    lib.Main = function(parent, box, jQuery){
        var self = this;
        this.pollSwitch = box.find("#pollOn");        
        this.tbody = box.find("tbody");
        
        //@todo find a better way
        this.tmpl = tmpl("main_hostCountRow");
        var priv = {
            pollIntervalHandle: null
            , succeedOnce: false
            , pollHosts: function(){
                $.ajax("/simple/host_count", {dataType: "json"})
                    .success(function(response){
                        if(response.success){
                            self.tbody.empty();                            
                            for(i = 0; i < response.hosts.length; i++){
                                self.tbody.append(self.tmpl(response.hosts[i]));
                            }
                        }
                    });
            }
        }
        
        /**
        *@argument {integer} delay Microsend interval to poll server for new hosts data
        */            
        this.poll = function(delay){
            if(priv.pollIntervalHandle != null){
                clearInterval(priv.pollIntervalHandle);
                priv.pollIntervalHandle = null;
            }
            
            priv.pollIntervalHandle = setInterval(priv.pollHosts, delay);
            return true;
        };
        
        this.haltPoll = function(){
            clearInterval(priv.pollIntervalHandle);
            priv.pollIntervalHandle = null;
        }
        
        this.onHostClick = function(){
            var hostName = $(this).data("host");
            parent.menu.tabs("add", "/simple/describe?host=" + hostName);
            
        }
        
        jQuery("a.hostClick").live("click", this.onHostClick);
        
        this.poll(1500);
        
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