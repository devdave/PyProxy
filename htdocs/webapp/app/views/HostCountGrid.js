Ext.define("Px.views.HostCountGrid", {
    extend: "Ext.grid.Panel"
    , store: Ext.create("Px.stores.Hosts")
    , stateful: true
    , stateId: "hostCountStateGrid"
    , columns: [
        {
            text: "Host"
            , flex: 1
            , sortable: true
            , dataIndex: "host"
        }
        ,{
            text: "Count"
            , flex: 1
            , sortable: true
            , dataIndex: "count"
        }
    ]
    , viewConfig: {
        stripeRows: true
    }
});