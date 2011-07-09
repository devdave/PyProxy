    
    lib._existsDetails = {};
    
    lib.RequestDetail = function(parent, menu, host, url, jQuery){
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
                            self.page.html("<p>Error loading details" + data.reason + "</p>");
                        }else{
                            self.renderData(data);
                        }
                        
                        self.page.show()
                    })
                    .error(function(){
                        console.error("Failed to detail " , arguments);
                    });
                
        }
        
        self.renderData = function(data){
            self.page.empty();
            self.page.append("<h1>").text(data.host + - + data.ts);
            for( var uri in data.uris){
                var responses = data.uris[uri]
                var body = jQuery("<div>");
                var list = jQuery("<ul>");
                list.append("<li>").text( data.host + "/ `" + uri + "` * " + responses.length)
                
                body.append(list)
                self.page.append(body);
                
            }
            self.page.append( jQuery("<input>", {type: "button", value: "Refresh"}).click(self.load));
            
        }
        
        self.uriTemplate = "";
        
    }
    

    
//    {
//   "host":"ominian.net",
//   "ts":1310014998.826,
//   "success":true,
//   "uris":{
//      "/":[
//         {
//            "headers":{
//               "accept-charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.7",
//               "host":"ominian.net",
//               "accept-language":"en-us,en;q=0.5",
//               "accept-encoding":"gzip, deflate",
//               "connection":"close",
//               "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,* /*;q=0.8",
//               "user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0"
//            },
//            "host":"ominian.net",
//            "uri":"/",
//            "ext":"",
//            "method":"GET"
//         }
//      ]
//   }
//}