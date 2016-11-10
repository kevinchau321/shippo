import pyPdf
import shippo
from re import sub
from decimal import Decimal

shippo.api_key = "shippo_test_2cabafcf72d1758972066f51bdaabe288639f32a"

def parse_pdf_and_create_shipments(pdf_filename):
    orders = []
    pdf = pyPdf.PdfFileReader(open(pdf_filename, "rb"))
    for page in pdf.pages:
        # new blank order, consisting of address_from, address_to, parcel
        order = []

        # these indices will need to be changed depending on given info
        lines = page.extractText().split('\n')

        order_num = lines[0].split('#')[1]
        sender_name = lines[2]
        sender_street = lines[5]
        sender_city = lines[6].split(', ')[0]
        sender_state = lines[6].split(', ')[1]
        sender_zip = lines[6].split(', ')[2]
        sender_country = lines[7]
        sender_email = lines[4]

        address_from = {
            "object_state": "VALID",
            "object_purpose": "PURCHASE",
            "object_id": order_num,
            "name": sender_name,
            "street1": sender_street,
            "city": sender_city,
            "state": sender_state,
            "zip": sender_zip,
            "country": sender_country,
            "email": sender_email,
            "phone": "+1 503 820 9175"
        }

        order.append(address_from)

        recipient_name = lines[9]
        recipient_street = lines[11]
        recipient_city = lines[12].split(', ')[0]
        recipient_state = lines[12].split(', ')[1]
        recipient_zip = lines[12].split(', ')[2]
        recipient_country = lines[13]
        recipient_email = lines[10]

        address_to = {
            "object_state": "VALID",
            "object_purpose": "PURCHASE",
            "object_id": order_num,
            "name": recipient_name,
            "street1": recipient_street,
            "city": recipient_city,
            "state": recipient_state,
            "zip": recipient_zip,
            "country": recipient_country,
            "email": recipient_email,
            "phone": "+1 503 820 9175"
        }

        order.append(address_to)

        # All parcels are a skateboard for now
        parcel = {
            "length": "32.25",
            "width": "8.5",
            "height": "2",
            "distance_unit": "in",
            "weight": lines[24].split(' ')[0],
            "mass_unit": "lb"
        }

        order.append(parcel)

        orders.append(order)

    for order in orders:
        shipment = shippo.Shipment.create(
            object_purpose = 'PURCHASE',
            address_from = order[0],
            address_to = order[1],
            parcel = order[2],
            async = False
        )

        #Create a Transaction Object

        # Get the minimum rate
        min_rate_object = None
        min_rate_amount = None
        for rate in shipment.rates_list:
            if min_rate_object == None:
                min_rate_object = rate
                min_rate_amount = Decimal(sub(r'[^\d.]', '', rate.amount))
            else:
                if Decimal(sub(r'[^\d.]', '', rate.amount)) < min_rate_amount:
                    min_rate_object = rate
                    min_rate_amount = Decimal(sub(r'[^\d.]', '', rate.amount))

        rate = min_rate_object

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
