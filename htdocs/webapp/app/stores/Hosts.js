Ext.define("Px.stores.Hosts"
,{
    extend: "Ext.data.Store"
    , storeId: "hostStore"
    , fields: [
        {name: "host", type:"string"}
        , {name: "count", type: "int"}        
    ]
    , autoLoad: true
    , model: "Px.models.Host"
    , proxy: {
        type: 'ajax'
        , url: "/simple/host_count"
        , reader: "json"
    }    
});