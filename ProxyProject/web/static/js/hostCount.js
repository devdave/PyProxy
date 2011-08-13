

App.HostCount = function(){
    var self = this;
    jQuery(".hostCount").live("click", function(evt){
        self.processClick(jQuery(this), evt);
    });
    
    
    self.processClick = function(anchor, evt){
        console.log(anchor.data("host"), anchor, evt);
        
    }
    
}



App.hostCount = new HostCount();