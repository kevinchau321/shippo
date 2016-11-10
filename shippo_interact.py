from splinter import Browser
import time
import os
from selenium import webdriver
import tempfile
import urllib
import datetime
from pdf_to_csv import pdf_to_csv
import pyPdf
import csv
import shippo

with Browser('chrome') as browser:
    #browser = Browser('chrome')
    # Visit URL
    url = "https://goshippo.com"
    browser.visit(url)

    # Find and click the 'Login' button
    button = browser.click_link_by_text('Login')

    # Find Email Form
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


    # Select all orders
    browser.find_by_id('select_all').click()

    # Find drop down button

    # for i in range(1210,1220):
    #     ember_id = 'ember' + str(i)
    #     print ember_id
    #     for elem in browser.find_by_id(ember_id):
    #         if elem.has_class('dropdown-menu ember-view rl-dropdown'):
    #             print "found drop down menu ", ember_id
    #             browser.find_by_id(ember_id).click()

    # find and click drop down button
    for elem in browser.find_by_css('button'):
        if elem.has_class('btn btn-sm btn-primary dropdown-toggle custom-dropdown ember-view rl-dropdown-toggle'):
            elem.click()
            break

    # find all links with a cursor-pointer
    # Select Download packing slips
    for elem in browser.find_by_css('a'):
        if elem.has_class('cursor-pointer'):
            if "Download packing slips" in elem.text:
                elem.click()
                break

    #webdriver.Chrome().switch_to_alert()
    # Download packing slips
    browser.windows.current = browser.windows[1]
    pdf_link = browser.find_by_id('plugin').first['src']
    pdf_filename = "orders/shippo_orders" + datetime.datetime.now().strftime("%I%M%S%p%B%d%Y") + ".pdf"
    urllib.urlretrieve(pdf_link, pdf_filename)

    #return control to main window
    browser.windows.current = browser.windows[0]
    browser.windows[1].close()


    ###### Parse Packing slips for addresses #####
    # print pdf_to_csv(pdf_filename, "\n", 5)

    #create list of orders
    orders = []

    pdf = pyPdf.PdfFileReader(open(pdf_filename, "rb"))
    for page in pdf.pages:
        # new blank order, consisting of address_from, address_to, parcel
        order = []
        lines = page.extractText().split('\n')
        order_num = lines[0].split('#')[1]
        print order_num



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


    ###############################################
    # Call shippo API to create shipment labels and transactions


    # hide orders so we won't create duplicate shipments

    print "Waiting for input to exit..."
    raw_input()

    # Logout...
    #browser.click_link_by_text('kevinchau321@berkeley.edu')
    #browser.click_link_by_href('https://goshippo.com/user/logout/')
    for elem in browser.find_by_css('a'):
        if elem.has_class('cursor-pointer'):
            if "LOGOUT" in elem.text:
                elem.click()
                break

    # print "Waiting for input to exit..."
    # raw_input()