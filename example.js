/**
This example demonstrates how to purchase a label for an international shipment.
Creating domestic shipment would follow a similiar proccess but would not require
the creation of CustomsItems and CustomsDeclaration objects.
**/


// replace <YOUR_PRIVATE_KEY> with your ShippoToken key
var shippo = require('shippo')('shippo_test_2cabafcf72d1758972066f51bdaabe288639f32a');

var addressFrom  = {
	"object_purpose":"PURCHASE",
	"name":"Kevin Chau",
	"company":"Pseudo Skate Co.",
	"street1":"521 Mccollam Dr",
	"city":"San Jose",
	"state":"CA",
	"zip":"95127",
	"country":"US", //iso2 country code
	"phone":"+1 503 820 9175",
	"email":"kevinchau321@gmail.com",
}

// example address_to object dict
var addressTo = {
	"object_purpose":"PURCHASE",
	"name":"Kevin Thanh-Minh Chau",
	"company":"Pseudo Skate Co.",
	"street1":"2716 Ellsworth St",
	"city":"Berkeley",
	"state":"CA",
	"zip":"94705",
	"country":"US", //iso2 country code
	"phone":"+1 503 820 9175",
	"email":"kevinchau321@gmail.com",
	"metadata" : "Pseudo Skate Co. Order #1043"
}

// parcel object dict
var parcel = {
	"length":"5",
	"width":"5",
	"height":"5",
	"distance_unit":"in",
	"weight":"2",
	"mass_unit":"lb",
}

// example CustomsItems object. This is required for int'l shipment only.
var customsItem = {
	"description":"T-Shirt",
	"quantity":2,
	"net_weight":"0.3",
	"mass_unit":"lb",
	"value_amount":"20",
	"value_currency":"USD",
	"origin_country":"US",
}

// Creating the CustomsDeclaration
// (CustomsDeclaration are NOT required for domestic shipments)
shippo.customsdeclaration.create({
	"contents_type": "MERCHANDISE",
	"non_delivery_option": "RETURN",
	"certify": true,
	"certify_signer": "Mr. Hippo",
	"items": [customsItem],
})
.then(function(customsDeclaration) {
	console.log("customs Declaration : %s", JSON.stringify(customsDeclaration, null, 4));
	// Creating the shipment object. In this example, the objects are directly passed to the
	// shipment.create method, Alternatively, the Address and Parcel objects could be created
	// using address.create(..) and parcel.create(..) functions respectively.
	// adding the async:false makes this call synchronous
	return shippo.shipment.create({
		"object_purpose": "PURCHASE",
		"address_from": addressFrom,
		"address_to": addressTo,
		"parcel": parcel,
		"customs_declaration": customsDeclaration.object_id,
		"async": false
	})

}, function(err) {
	// Deal with an error
	console.log("There was an error creating customs declaration: %s", err);
})
.then(function(shipment) {
	console.log("shipment : %s", JSON.stringify(shipment, null, 4));
	shippo.shipment.rates(shipment.object_id)
	.then(function(rates) {
		console.log("rates : %s", JSON.stringify(rates, null, 4));
		// Get the first rate in the rates results for demo purposes.
		rate = rates.results[0];
		// Purchase the desired rate
		return shippo.transaction.create({"rate": rate.object_id, "async": false})
	}, function(err) {
		// Deal with an error
		console.log("There was an error retrieving rates : %s", err);
	})
	.then(function(transaction) {
			console.log("transaction : %s", JSON.stringify(transaction, null, 4));
			// print label_url and tracking_number
			if(transaction.object_status == "SUCCESS") {
				console.log("Label URL: %s", transaction.label_url);
				console.log("Tracking Number: %s", transaction.tracking_number);
			}else{
				//Deal with an error with the transaction
				console.log("Message: %s", transaction.messages);
			}

	}, function(err) {
		// Deal with an error
		console.log("There was an error creating transaction : %s", err);
	});
},function(err) {
	// Deal with an error
	console.log("There was an error creating shipment: %s", err);
});