pdf_filename = 

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