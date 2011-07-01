
Ext.require([
    'Ext.container.Viewport'
    ,'Ext.grid.*'
    ,'Ext.data.*'
    ,'Ext.util.*'
    ,'Ext.toolbar.Paging'    
    ,'Ext.ModelManager'
    ,'Ext.tip.QuickTipManager'
]);
Ext.application({
    name: 'Px'
    , appFolder: "app"
    , launch: function() {
        Ext.create('Px.views.Main');
    }
});