import os
import names

# first_name = names.get_first_name()
# last_name = names.get_last_name()

## os.system call:
os.system("curl https://api.goshippo.com/v1/orders/  \
    -H \"Authorization: ShippoToken shippo_test_2cabafcf72d1758972066f51bdaabe288639f32a\" \
    -H \"Content-Type: application/json\"  \
    -d '{   \
        \"to_address\": {   \
          \"object_purpose\": \"PURCHASE\", \
          \"name\": \"Kevin Chau\", \
          \"company\": \"Pseuo Skate Co.\", \
          \"street1\": \"2716 Ellsworth St\", \
          \"city\": \"Berkeley\", \
          \"state\": \"CA\",    \
          \"zip\": \"94705\",   \
          \"country\": \"US\",  \
          \"phone\": \"+1 503 820 9175\",   \
          \"email\": \"kevinchau321@berkeley.edu\",  \
          \"metadata\": \"Customer ID 123456\"  \
        },  \
        \"items\": [    \
          { \
            \"title\": \"Blue Pseudo Deck 8.125\",  \
            \"quantity\": 1,   \
            \"net_weight\": 3,  \
            \"weight_unit\": \"lb\",    \
            \"price\": 39.99,   \
            \"currency\": \"USD\",  \
            \"variant_title\": \"blue\",    \
            \"sku\": \"12222\"  \
          } \
        ] \
      }'")
