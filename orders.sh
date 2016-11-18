curl https://api.goshippo.com/v1/orders/  \
    -H "Authorization: ShippoToken shippo_test_2cabafcf72d1758972066f51bdaabe288639f32a" \
    -H "Content-Type: application/json"  \
    -d '{
        "to_address": {
          "object_purpose": "PURCHASE",
          "name": "Mrs. Hippo",
          "company": "Shippo",
          "street1": "965 Mission St.",
          "city": "San Francisco",
          "state": "CA",
          "zip": "94105",
          "country": "US",
          "phone": "+1 555 341 1111",
          "email": "support@goshippo.com",
          "metadata": "Customer ID 123456"
        },
        "items": [
          {
            "title": "Item 1",
            "quantity": 12,
            "weight": 12.12,
            "weight_unit": "lb",
            "price": 45.00,
            "currency": "USD",
            "variant_title": "blue",
            "sku": "12222"
          }
        ],
        "total_tax": "12.00",
        "total_price": "133.00",
        "subtotal_price": "1.00",
        "currency": "USD",
        "shipping_method": "USPS-Box",
        "shipping_cost": "3.45",
        "shipping_cost_currency": "USD"
      }'
