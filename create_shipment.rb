require 'shippo'

Shippo::api_token = 'shippo_test_2cabafcf72d1758972066f51bdaabe288639f32a'

address_from = {
    :object_purpose => 'PURCHASE',
    :name => 'Kevin Chau',
    :street1 => '521 MCCOLLAM DR',
    :city => 'San Jose',
    :state => 'CA',
    :zip => '95127',
    :country => 'US',
    :phone => '+1 503 820 9175',
    :email => 'kevinchau321@gmail.com' 
}

address_to = {
    :object_purpose => 'PURCHASE',
    :name => 'Kevin Chau',
    :street1 => '2716 Ellsworth St',
    :city => 'Berkeley',
    :state => 'CA',
    :zip => '95127',
    :country => 'US',
    :phone => '+1 503 820 9175',
    :email => 'kevinchau321@gmail.com'
}

parcel = {
    :length => 5,
    :width => 1,
    :height => 5.555,
    :distance_unit => :in,
    :weight => 2,
    :mass_unit => :lb
}

shipment = Shippo::Shipment.create(
    :object_purpose => 'PURCHASE',
    :address_from => address_from,
    :address_to => address_to,
    :parcel => parcel,
    :async => false
)

puts shipment

# Create transaction object

# Get the first rate in the rates results.
# Customize this based on your business logic.
rate = shipment.rates_list.first

# Purchase the desired rate.
transaction = Shippo::Transaction.create( 
  :rate => rate["object_id"], 
  :label_file_type => "PDF", 
  :async => false )

# label_url and tracking_number
if transaction["object_status"] == "SUCCESS"
  puts "Label sucessfully generated:"
  puts "label_url: #{transaction.label_url}" 
  puts "tracking_number: #{transaction.tracking_number}" 
else
  puts "Error generating label:"
  puts transaction.messages
end

puts transaction