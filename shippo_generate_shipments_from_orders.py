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

    # Select all orders
    browser.find_by_id('select_all').click()

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

    # Call shippo API to create shipment labels and transactions

    parse_pdf.parse_pdf_and_create_shipments(pdf_filename)

    # hide orders so we won't create duplicate shipments
    # find and click drop down button
    for elem in browser.find_by_css('button'):
        if elem.has_class('btn btn-sm btn-primary dropdown-toggle custom-dropdown ember-view rl-dropdown-toggle'):
            elem.click()
            break

    # find all links with a cursor-pointer
    # Select Download packing slips
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

    # print "Waiting for input to exit..."
    # raw_input()
