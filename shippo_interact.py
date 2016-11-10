from splinter import Browser
import time
import os

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
    for elem in browser.find_by_css('a'):
        if elem.has_class('cursor-pointer'):
            if "Download packing slips" in elem.text:
                elem.click()
                break


    # This does not work because the ember ID changes everytime there is a new order
    #browser.find_by_xpath('//*[@id="ember1199"]').click()
    #browser.find_by_name('Download packing slips for selected orders').first.click()
    #browser.find_by_xpath('//*[@id="ember1214"]/li[2]').click()

    # print browser.find_by_id('buy_all_button')[0]
    #browser.click_link_by_text('Download packing slips for selected orders')






    # Download packing slips

    # Parse Packing slips for addresses

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