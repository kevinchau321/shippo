var shippo = require('shippo')('shippo_test_2cabafcf72d1758972066f51bdaabe288639f32a');

var addressFrom  = {
    "object_purpose":"PURCHASE",
    "name":"Kevin Chau",
    "street1":"521 Mccollam Dr",
    "city":"San Jose",
    "state":"CA",
    "zip":"95127",
    "country":"US", //iso2 country code
    "phone":"+1 503 820 9175",
    "email":"kevinchau321@gmail.com",
};

// example address_to object dict
var addressTo = {
    "object_purpose":"PURCHASE",
    "name":"Kevin Chau",
    "street1":"2716 Ellsworth St",
    "city":"Berkeley",
    "state":"CA",
    "zip":"94705",
    "country":"US", //iso2 country code
    "phone":"+1 503 820 9175",
    "email":"kevinchau321@gmail.com",
};

// parcel object dict
var parcelOne = {
    "length":"5",
    "width":"5",
    "height":"5",
    "distance_unit":"in",
    "weight":"2",
    "mass_unit":"lb"
};

var parcelTwo = {
    "length":"5",
    "width":"5",
    "height":"5",
    "distance_unit":"in",
    "weight":"2",
    "mass_unit":"lb"
};

var shipment = {
    "object_purpose": "PURCHASE",
    "address_from": addressFrom,
    "address_to": addressTo,
    "parcel": [parcelOne, parcelTwo],
    "submission_type": "DROPOFF"
};

shippo.transaction.create({
    "shipment": shipment,
    "servicelevel_token": "ups_ground",
    "carrier_account": "558c84bbc25a4f609f9ba02da9791fe4",
    "label_file_type": "png"
})
.then(function(transaction) {
    shippo.transaction.list({
      "rate": transaction.rate
    })
    .then(function(mpsTransactions) {
        mpsTransactions.results.forEach(function(mpsTransaction){
            if(mpsTransaction.object_status == "SUCCESS") {
                console.log("Label URL: %s", mpsTransaction.label_url);
                console.log("Tracking Number: %s", mpsTransaction.tracking_number);
            } else {
                // hanlde error transactions
                console.log("Message: %s", mpsTransactions.messages);
            }
        });
    })
}, function(err) {
    // Deal with an error
    console.log("There was an error creating transaction : %s", err.detail);
});