
function Menuman(menu, main){
    if(typeof App.menu != "undefined"){
        return App.menu;
    }
    var self = this;
    App.menu = this;
    
    this.tabEl = menu;
    this.main = main;
    this.tabEl.tabs();
    
    
    
    self.addOrUpdate = function(name, uri){
        
        var exists = self.tabEl.tabs("select", uri);
        console.log(exists, name, uri);
    }
    
    
    
    
}



