from splinter import Browser
import time
import os
from selenium import webdriver
import tempfile
import urllib
import datetime
import pyPdf
import shippo
import parse_pdf
import subprocess
import json
from decimal import Decimal
from re import sub

with Browser('chrome') as browser:
    # Visit URL
    url = "https://goshippo.com"
    browser.visit(url)

    # Find and click the 'Login' button
    button = browser.click_link_by_text('Login')

    # Find Email form and fill
    # example: export SHIPPO_EMAIL="email@email.com"
    browser.fill('email', os.environ['SHIPPO_EMAIL'])
    browser.fill('password', os.environ['SHIPPO_PASSWORD'])
    browser.find_by_value('Log In').click()

    time.sleep(1)

    # Go to orders page
    browser.click_link_by_href('/orders')

    # Find Sync Orders Button, first instance of button is the sync button...
    # Click on Sync Orders Button
    browser.find_by_css('button').click()
    time.sleep(3)
    # Refresh Page, wait 3 seconds so the synchronization has time
    browser.reload()


    # capture orders using order endpoint
    orders = os.popen("curl https://api.goshippo.com/v1/orders/  \
        -H \"Authorization: ShippoToken shippo_test_2cabafcf72d1758972066f51bdaabe288639f32a\" \
        -H \"Content-Type: application/json\"").read()

    print "Read orders from shippo account."

    print orders

    print "Parsing JSON..."
    # parse json orders
    orders_json = json.loads(orders)
    print orders_json
    orders_count = orders_json["count"]
    print "Number of orders is " + str(orders_count)
    orders_list = orders_json["results"]

    # print out the orders
    i = 1
    orders = []
    for order_json in orders_list:
        print "order number " + str(i)
        print order_json
        i += 1

        # call shipment making API

        # # Hide orders
        # order["hidden"] = True
        #
        # print "Hiding order..."
        #
        # # update outgoing to json to hide orders
        # new_order_json = json.dumps(order)
        # print new_order_json
        #
        # print "sending hidden json..."
        # # send json to api
        # os.system("curl https://api.goshippo.com/v1/orders/  \
        #     -H \"Authorization: ShippoToken shippo_test_2cabafcf72d1758972066f51bdaabe288639f32a\" \
        #     -H \"Content-Type: application/json\"  \
        #     -d '" + new_order_json + "'")

        # new blank order, consisting of address_from, address_to, parcel
        order = []
        order_num = order_json["order_number"]
        # The sender is always me (business owner)
        sender_name = "Kevin Chau"
        sender_street = "521 Mccollam Dr"
        sender_city = "San Jose"
        sender_state = "CA"
        sender_zip = "95127"
        sender_country = "US"
        sender_email = "kevinchau321@gmail.com"

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

        # recipient_name = order_json[""]
        # recipient_street = lines[11]
        # recipient_city = lines[12].split(', ')[0]
        # recipient_state = lines[12].split(', ')[1]
        # recipient_zip = lines[12].split(', ')[2]
        # recipient_country = lines[13]
        # recipient_email = lines[10]

        address_to = order_json["to_address"]

        order.append(address_to)

        # print "WEIGHT OF PACKAGE: "
        weight = order_json["weight"]
        parcel = {
            "length": "32.25",
            "width": "8.5",
            "height": "2",
            "distance_unit": "in",
            "weight": weight,
            "mass_unit": "lb",
        }
        # print weight
        # All parcels are a skateboard for now

        order.append(parcel)

        orders.append(order)

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

    # Select all orders
    browser.find_by_id('select_all').click()

    # hide orders so we won't create duplicate shipments
    # find and click drop down button
    for elem in browser.find_by_css('button'):
        if elem.has_class('btn btn-sm btn-primary dropdown-toggle custom-dropdown ember-view rl-dropdown-toggle'):
            elem.click()
            break

    # find all links with a cursor-pointer
    # Hide orders
    for elem in browser.find_by_css('a'):
        if elem.has_class('cursor-pointer'):
            if "Hide" in elem.text:
                elem.click()
                break

    # Logout...
    for elem in browser.find_by_css('a'):
        if elem.has_class('cursor-pointer'):
            if "LOGOUT" in elem.text:
                elem.click()
                break
