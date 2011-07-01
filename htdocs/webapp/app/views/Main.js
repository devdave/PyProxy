Ext.define("Px.views.Main", {
    extend: "Ext.container.Viewport"
    , layout: 'border'
    , initComponent: function() {
        this.items = [
            {
                xtype: 'tabpanel'
                ,activeTab: 0
                ,region: 'center'
                ,width: 100
                ,html: 'PyProxy web interface version .0000000001 double secret Alpha'
                ,id: 'dataTabs'
                ,items: [                    
                        Ext.create("Px.views.HostCountGrid")                        
                    ]
                , tbar:  [
                    {
                        xtype: 'button'
                        ,text: 'Host Count'
                    }
                    ,{
                        xtype: 'button'
                        ,text: 'Host digest'
                    }
                    ,{
                        xtype: 'button'
                        ,text: 'URL Digest'
                    }
                ]
            }
        ];
        Px.views.Main.superclass.initComponent.call(this);
    }
});
