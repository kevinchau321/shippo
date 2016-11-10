var shippo = require('shippo')('shippo_test_2cabafcf72d1758972066f51bdaabe288639f32a');

var addressFrom  = {
    "object_purpose": "PURCHASE",
    "name": "Kevin Chau",
    "street1": "521 Mccollam Dr",
    "city": "San Jose",
    "state": "CA",
    "zip": "95127",
    "country": "US",
    "phone": "+1 503 820 9175",
    "email": "kevinchau321@gmail.com"
};

var addressTo = {
    "object_purpose": "PURCHASE",
    "name": "Kevin Chau",
    "street1": "2716 Ellsworth St",
    "city": "San Jose",
    "state": "CA",
    "zip": "95127",
    "country": "US",
    "phone": "+1 503 820 9175",
    "email": "mrhippo@goshippo.com"
};

var parcel = {
    "length": "5",
    "width": "5",
    "height": "5",
    "distance_unit": "in",
    "weight": "2",
    "mass_unit": "lb"
};

shippo.shipment.create({
    "object_purpose": "PURCHASE",
    "address_from": addressFrom,
    "address_to": addressTo,
    "parcel": parcel,
    "async": false
}, function(err, shipment){
    // asynchronously called
});

// Create Transaction Object

// Get the first rate in the rates results.
// Customize this based on your business logic.
var rate = shipment.rates_list[0];

// Purchase the desired rate.
shippo.transaction.create({
    "rate": rate.object_id,
    "label_file_type": "PDF",
    "async": false
}, function(err, transaction) {
   // asynchronous callback
});

