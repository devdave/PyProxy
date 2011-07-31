    
    lib._existsDetails = {};
    
    lib.RequestHostDetail = function(parent, menu, host, url, jQuery){
        if( typeof lib._existsDetails[host] == "undefined"){
            lib._existsDetails[host] = new lib.HostDetail(parent, menu, host, url, jQuery);
        }
        lib._existsDetails[host].load();
    }
    lib.HostDetail = function(parent, menu, host, remote_url, jQuery){
        var self = this;
        self.parent = parent;
        self.menu  = menu;
        self.host = host;
        self.clean_host = host.replace(/\./g, "_");
        self.remote_url = remote_url;
        self.element_id = "tabpanel-" + self.clean_host;
        self.loaded = false;
        
        if(jQuery("#" + self.element_id).length == 0){
            self.page = jQuery("<div></div>").attr("id", self.element_id).hide();
            self.menu.append(self.page);
        }else{
            self.page = jQuery("#" + self.element_id).hide();
        }
        var priv = {};
        
        
        self.load = function(){
                jQuery.ajax(self.remote_url, {dataType: "json"})
                    
                    .success(function(data){
                        if(self.loaded == false){
                            self.menu.tabs("add", "#" + self.page.attr("id"), self.host );
                            self.loaded = true;
                        }
                        if(data.success == false){
                            self.page.html("<p>Error loading details " + data.reason + " </p>");
                        }else{
                            self.renderData(data);
                        }
                        
                        self.page.show()
                    })
                    .error(function(){
                        console.error("Failed to fetcg detail " , arguments);
                    });
                
        }
        
        self.renderData = function(data){
            self.page.empty();
            self.page.append("<h1>").text(data.host + - + data.ts);
            for( var i = 0; i < data.uris.length; i++){
            
                
                var body = jQuery("<div>");
                var list = jQuery("<ul>");
                var element = jQuery("<a>", {href:"#"}).text( data.host + data.uris[i] ).addClass("uriDetail").data('host', data.host).data("uri", data.uris[i] );
                list.append(jQuery("<li>").append(element)); 
                
                body.append(list)
                self.page.append(body);
                
            }
            self.page.append( jQuery("<input>", {type: "button", value: "Refresh"}).click(self.load));
            
        }
        
        self.uriTemplate = "";
        jQuery("a.uriDetail").live("click",function(evt){
           var element = jQuery(this);
           var host = element.data("host");
           var uri = element.data("uri");
           
        });
        
    }
    

