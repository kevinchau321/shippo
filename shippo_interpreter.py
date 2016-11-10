from splinter import Browser
import time


browser = Browser('chrome')
# Visit URL
url = "https://goshippo.com"
browser.visit(url)

# Find and click the 'Login' button
button = browser.click_link_by_text('Login')


#Find Email Form
browser.fill('email', 'kevinchau321@berkeley.edu')
browser.fill('password', '196464Ktc')
browser.find_by_value('Log In').click()

time.sleep(1)

# Go to orders page
browser.click_link_by_href('/orders')

# Find Sync Orders Button, first instance of button is the sync button...
# Click on Sync Orders Button
browser.find_by_css('button').click()
time.sleep(3)
# Refresh Page
browser.reload()


# Select all orders
browser.find_by_id('select_all').click()

# Find drop down button
# This does not work because the ember ID changes everytime there is a new order
#browser.find_by_xpath('//*[@id="ember1199"]').click()
#browser.find_by_name('Download packing slips for selected orders').first.click()
#browser.find_by_xpath('//*[@id="ember1214"]/li[2]').click()

# print browser.find_by_id('buy_all_button')[0]
# browser.click_link_by_text('Download packing slips for selected orders')

#ember id number
for i in range(0,2000):
    ember_id = 'ember' + str(i)
    #print ember_id
    for elem in browser.find_by_id(ember_id):
        if elem.has_class('dropdown-menu ember-view rl-dropdown'):
            elem.click()




# Download packing slips

# Parse Packing slips for addresses

# Call shippo API to create shipment labels and transactions

print "Waiting for input to exit..."
raw_input()

# Logout...
#browser.click_link_by_text('kevinchau321@berkeley.edu')
#browser.click_link_by_href('https://goshippo.com/user/logout/')
