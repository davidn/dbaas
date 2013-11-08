angular.module('geniedb').controller('MainCtrl', function ($scope, User, dbaasConfig) {
    // Inject User to force initialization of Token
    $scope.showInfo = function () {
        console.log(dbaasConfig);
    };


//    $data.initService('http://jaydata.org/examples/Northwind.svc/');

//    $data.Entity.extend("Provider", {
//        url: { type: "string", key: true, computed: true },
//        name: { type: "string", required: true },
//        code: { type: "string", required: true },
//        flavors: { type: "Array", elementType: "Flavor", navigationProperty: "provider" },
//        regions: { type: "Array", elementType: "Region", navigationProperty: "provider" }
//    });
//    $data.Entity.extend("Flavor", {
//        url: { type: "string", key: true, computed: true },
//        code: { type: "string", computed: true },
//        name: { type: "string", computed: true },
//        cpus: { type: "string", computed: true },
//        ram: { type: "string", computed: true },
//        provider: { type: "Provider", navigationProperty:"flavors"}
//    });
//    $data.Entity.extend("Region", {
//        url: { type: "string", key: true, computed: true },
//        code: { type: "string", computed: true },
//        name: { type: "string", computed: true },
//        latitude: { type: "number", computed: true },
//        longitude: { type: "number", computed: true },
//        provider: { type: "Provider", navigationProperty:"regions"}
//    });
//
//    $data.Entity.extend("Cluster", {
//        id: { type: "string", key: true, computed: true },
//        backup_count: { type: "int" },
//        backup_schedule: { type: "string"},
//        ca_cert: { type: "string"},
//        client_cert: { type: "string"},
//        client_key: { type: "string"},
//        dbname: { type: "string"},
//        dbpassword: { type: "string"},
//        dbusername: { type: "string"},
//        dns_name: { type: "string"},
//        label: { type: "string" },
//        port: { type: "int" },
//        status: { type: "string" },
//        status_code: { type: "int" },
//        url: { type: "string", computed: true },
//        user: { type: "string", computed: true },
//        nodes: { type: "Array", elementType: "Node", navigationProperty: "cluster" },
//    });
//
//    $data.Entity.extend("Node", {
//        url: { type: "string", key: true, computed: true },
//        label: { type: "string" },
//        nid: { type: "int", computed: true},
//        ip: { type: "string", computed: true},
//        dns_name: { type: "string", computed: true},
//        status: { type: "string", computed: true },
//        status_code: { type: "int", computed: true },
//        iops: { type: "string"},
//        flavor: { type: "Flavor", navigationProperty:"nodes"},
//        region: { type: "Region", navigationProperty:"nodes"},
//        cluster: { type: "Cluster", navigationProperty:"nodes"}
//    });
//
//    $data.EntityContext.extend("DBaaSContext", {
//        Provider: { type: $data.EntitySet, elementType: Provider },
//        Flavor: { type: $data.EntitySet, elementType: Flavor },
//        Region: { type: $data.EntitySet, elementType: Region },
//        Cluster: { type: $data.EntitySet, elementType: Cluster },
//        Node: { type: $data.EntitySet, elementType: Node }
//    });


});