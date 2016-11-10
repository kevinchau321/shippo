from splinter import Browser
import time
import os
from selenium import webdriver
import tempfile
import urllib
import datetime

def pdf_to_csv(filename, separator, threshold):
    from cStringIO import StringIO
    from pdfminer.converter import LTChar, TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage

    class CsvConverter(TextConverter):
        def __init__(self, *args, **kwargs):
            TextConverter.__init__(self, *args, **kwargs)
            self.separator = separator
            self.threshold = threshold

        def end_page(self, i):
            from collections import defaultdict
            lines = defaultdict(lambda: {})
            for child in self.cur_item._objs:  # <-- changed
                if isinstance(child, LTChar):
                    (_, _, x, y) = child.bbox
                    line = lines[int(-y)]
                    line[x] = child._text.encode(self.codec)  # <-- changed
            for y in sorted(lines.keys()):
                line = lines[y]
                self.line_creator(line)
                self.outfp.write(self.line_creator(line))
                self.outfp.write("\n")

        def line_creator(self, line):
            keys = sorted(line.keys())
            # calculate the average distange between each character on this row
            average_distance = sum([keys[i] - keys[i - 1] for i in range(1, len(keys))]) / len(keys)
            # append the first character to the result
            result = [line[keys[0]]]
            for i in range(1, len(keys)):
                # if the distance between this character and the last character is greater than the average*threshold
                if (keys[i] - keys[i - 1]) > average_distance * self.threshold:
                    # append the separator into that position
                    result.append(self.separator)
                # append the character
                result.append(line[keys[i]])
            printable_line = ''.join(result)
            return printable_line

    # ... the following part of the code is a remix of the
    # convert() function in the pdfminer/tools/pdf2text module
    rsrc = PDFResourceManager()
    outfp = StringIO()
    device = CsvConverter(rsrc, outfp, codec="utf-8", laparams=LAParams())
    # becuase my test documents are utf-8 (note: utf-8 is the default codec)

    fp = open(filename, 'rb')

    interpreter = PDFPageInterpreter(rsrc, device)
    for i, page in enumerate(PDFPage.get_pages(fp)):
        outfp.write("START PAGE %d\n" % i)
        if page is not None:
            # print 'none'
            interpreter.process_page(page)
        outfp.write("END PAGE %d\n" % i)

    device.close()
    fp.close()

    return outfp.getvalue()

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
    # Parse Packing slips for addresses

    print pdf_to_csv(pdf_filename, "\n", 1.5)

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