

App_initialize = function(config){
    if(typeof App != "undefined"){
        //Prevent more then one instance of Application to be defined
        return App;
    }
    if(this == window){
        return new App_initialize(config);
    }
    
    //Claim namespaces
    window.App = this;
    window.Lib = {};
    
    App.nothing = function(){};
    
    //Default config
    App.config = {}
    jQuery.extend(App.config, config);
    
    App.LoadedScripts = [];
    
    
    $.each(document.getElementsByTagName("script"), function(element){
        if(this.src.length > 0){
            
            App.LoadedScripts.push(this.src.replace(document.location.origin, ""));
        }
    });
    
    
    return App;
    
}

App_initialize.prototype.loadScript = function(name, options){
        var config = { 
            path: "/js/"            
        }
    
        $.extend(config, options);
        var defer = jQuery.Deferred();
        var pathname = config['path'] + name
        
        var callback = function(response){
                console.log("Loaded ", pathname)
                if(defer.isResolved() == false){
                    App.LoadedScripts.push(pathname);
                
                    try{
                        defer.resolve(response, arguments);
                    }
                    catch(e){
                        console.error("loadScript() ", name , " ) Failed defer.resolve with ", arguments, e)
                    }
                
                }
                
            
        }
        
        
        var microsoftsucks = function(){
            if( this.readyState == "complete"){
                alert("You are using a shitty browser, this message will repeat for every required workaround");
                callback();
            }
        }
        
        
        
        if(App.LoadedScripts.indexOf(pathname) < 0 ){
            console.log("Loading ", pathname);
            var scriptElement = document.createElement("script")
            scriptElement.src = pathname;
            if(typeof scriptElement.onload != "undefined"){
                scriptElement.onload = callback;
            }
            else if(typeof scriptElement.onreadystatechange != "undefined") {
                alert("You are using a shitty browser, this message will repeat for every required workaround");
                scriptElement.onreadystatechange = microsoftsucks;
            }
            else{
                alert("I have no idea what web browser you're using; use chrome, firefox, or worst case MSIE ");
            }
            
            document.getElementsByTagName("head")[0].appendChild(scriptElement);
            
        }else{
            //We're already done, call defer on context shift
            setTimeout(function(){
                defer.resolve(true);
            }, 1)
        }
        
        return defer;
    }






