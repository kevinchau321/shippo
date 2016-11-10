import shippo

shippo.api_key = "shippo_test_2cabafcf72d1758972066f51bdaabe288639f32a"

address_from = {
    "object_purpose": "PURCHASE",
    "name": "Kevin Chau",
    "street1": "521 Mccollam Dr",
    "city": "San Jose",
    "state": "CA",
    "zip": "95127",
    "country": "US",
    "phone": "+1 503 820 9175",
    "email": "kevinchau321@gmail.com"
}

address_to = {
    "object_purpose": "PURCHASE",
    "name": "Kevin Chau",
    "street1": "2716 Ellsworth St",
    "city": "Berkeley",
    "state": "CA",
    "zip": "94705",
    "country": "US",
    "phone": "+1 503 820 9175",
    "email": "kevinchau321@gmail.com"
}

parcel = {
    "length": "5",
    "width": "5",
    "height": "5",
    "distance_unit": "in",
    "weight": "2",
    "mass_unit": "lb"
}

shipment = shippo.Shipment.create(
    object_purpose = 'PURCHASE',
    address_from = address_from,
    address_to = address_to,
    parcel = parcel,
    async = False
)

# print shipment

#Create a Transaction Object

# Get the first rate in the rates results.
# Customize this based on your business logic.
rate = shipment.rates_list[0]

# Purchase the desired rate. 
transaction = shippo.Transaction.create( 
    rate=rate.object_id, 
    label_file_type="PDF", 
    async=False )

# Retrieve label url and tracking number or error message
if transaction.object_status == "SUCCESS":
    print transaction.label_url
    print transaction.tracking_number
else:
    print transaction.messages

# print transaction