curl https://api.goshippo.com/v1/orders/  \
    -H "Authorization: ShippoToken shippo_test_2cabafcf72d1758972066f51bdaabe288639f32a" \
    -H "Content-Type: application/json"  \
    -d '{
      "object_id": "71b8e324a89c4ec491c90c25a73bca8f",
      "order_number": "#1015",
      "order_status": "PAID",
      "created_at": "2016-11-18T07:35:35Z",
      "object_owner": "kevinchau321@berkeley.edu",
      "to_address": {
        "object_state": "VALID",
        "object_purpose": "PURCHASE",
        "object_source": "FULLY_ENTERED",
        "object_created": "2016-11-18T07:36:20.317Z",
        "object_updated": "2016-11-18T07:36:20.317Z",
        "object_id": "22ed2e348f004956998fda393e9e639f",
        "object_owner": "kevinchau321@berkeley.edu",
        "name": "Fooda Barda",
        "company": "",
        "street_no": "",
        "street1": "2716 Ellsworth St",
        "street2": "",
        "street3": "",
        "city": "Berkeley",
        "state": "CA",
        "zip": "94705",
        "country": "US",
        "phone": "",
        "email": "kevinchau321@berkeley.edu",
        "is_residential": null,
        "ip": null,
        "messages": [],
        "metadata": "",
        "test": null
      },
      "address_from": null,
      "shop_app": "Shopify",
      "weight": "3.50",
      "weight_unit": "lb",
      "transactions": [],
      "total_tax": "0.00",
      "total_price": "0.00",
      "subtotal_price": "0.00",
      "currency": "USD",
      "shipping_method": null,
      "shipping_cost": null,
      "shipping_cost_currency": null,
      "line_items": [
        {
          "object_id": "e394a037e6b9498ba75d3f6412c9f659",
          "product": "3e93846d712742e69680aab85a662843",
          "variant": null,
          "app_id": "9176617926",
          "title": "Pseudo Blue Deck 8.125",
          "sku": "pd8125",
          "parcel": 1,
          "quantity": 1,
          "is_fulfilled": false,
          "total_amount": "39.99",
          "currency": "USD",
          "total_weight": "3.50",
          "weight_unit": "lb",
          "variant_title": null
        }
      ],
      "items": [
        {
          "id": 44041562,
          "title": "Pseudo Blue Deck 8.125",
          "quantity": 1,
          "total_weight": "3.50",
          "weight_unit": "lb",
          "total_price": "39.99",
          "currency": "USD",
          "price": "39.99",
          "variant_title": null,
          "sku": "pd8125"
        }
      ],
      "hidden": true
    }'
