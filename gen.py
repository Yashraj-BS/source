from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm


class FinalBillGenerator:
    LOGO_POSITION = (1.5, 22)
    LOGO_SIZE = (18.8, 6.2)
    CUSTOMER_INFO_TABLE_POSITION = (2, 17)
    SELF_TABLE_POSITION = (2.6, 19.8)
    ITEMS_TABLE_POSITION = (2, 11)
    PAYMENT_DETAILS_TABLE_POSITION = (2, 2)
    SIGNATURE_BOX_POSITION = (14.25, 2)  
    LINE_POSITION = (2, 19.2) 

    def __init__(self, buyer_name, items, filename='invoice'):
        self.buyer_name = buyer_name
        self.items = items
        self.filename = filename + ".pdf"

    def create_table(self, data, size, position, params=[]):
        # Define the style of the table

        default = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Light grey background for the first row
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Black text color for the first row
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Left alignment for all cells
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Middle alignment for all cells
            #('GRID', (0, 0), (-1, -1), 1, colors.black),  # Black border with width 1 for all cells
            ('FONT', (0, 0), (-1, -1), 'Muli', 12)  # Muli font for all cells
        ]

        if params:
            default.extend(params)

        style = TableStyle(default)
        table = Table(data)
        table.setStyle(style)

        x , y = position
        width, height = size 
        table.wrapOn(self.canvas, width * cm, height * cm) 
        table.drawOn(self.canvas, x * cm, y * cm)

    def generate_invoice(self, logo=None):
        self.canvas = canvas.Canvas(self.filename, pagesize=letter)
        pdfmetrics.registerFont(TTFont('Muli', 'assets/muli.ttf'))

        self.add_logo(self.canvas, logo)
        self.contact_details()
        self.customer_info()
        self.items_table()
        self.payment_details()
        self.signature()
        self.draw_lines()

        self.canvas.save()

    def add_logo(self, canvas, logo):
        x, y = self.LOGO_POSITION
        w, h = self.LOGO_SIZE
        canvas.drawImage(logo, x*cm, y*cm, width=w*cm, height=h*cm, mask='auto')

    def items_table(self):
        # Define the data for the table
        Total = 0
        data = [["Sr. No.", "Date", "Vehicle Number", "Trip", "Amount"]]
        for item in self.items:
            Total += item['Amount']
            data.append([str(item['Sr. No.']), str(item['Date']), str(item['Vehicle Number']), str(item['Trip']), str(item['Amount'])])
        data.append(["", "Pan Number: ", "BDHPS3373P", "Total: ", str(Total)])

        # Draw the table on the canvas at the specified position
        w, h = letter
        i, j = self.CUSTOMER_INFO_TABLE_POSITION
        x, y = self.ITEMS_TABLE_POSITION
        f = j - (0.636 * len(data)) - 1.3
        self.create_table(data, (w, h), (x, f), params=[('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey), ('GRID', (0, 0), (-1, -1), 1, colors.white)])


    def customer_info(self):
        # Define the data for the table
        data = [["Customer Name:", "Invoice Number:", "Invoice Date:"],
                [self.buyer_name, "INV-123", "25-Feb-2024"]]

        self.create_table(data, (14.54, 1.5), self.CUSTOMER_INFO_TABLE_POSITION, params=[('GRID', (0, 0), (-1, -1), 1, colors.white)])

    def contact_details(self):
        # Define the data for the table
        data = [["SHOP NO.04, NEAR BALAJI KATTA, TALEGAON-CHAKAN ROAD, MAHALUNGE\nTAL-KHED, PUNE 410501, Email - tts@gmail.com\nMobile Number -  9327383095, 7046689999"]]
        
        self.create_table(data, (17.75, 5.41), self.SELF_TABLE_POSITION, params=[('BACKGROUND', (0, 0), (-1, 0), colors.white), ('ALIGN', (0, 0), (-1, -1), 'CENTER')])

    # Add new method to write payment details table
    def payment_details(self):
        # Define the data for the table
        data = [[f"{' '*13}Payment Details"],
                ["Bank Name: ICICI Bank\nBranch: Silvassa Branch\nIFSC Code: ICIC0000422\nAccount Number: 042205000590\nAccount Name: TTS"]]
            
        self.create_table(data, (14.54, 1.5), self.PAYMENT_DETAILS_TABLE_POSITION, params=[('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Add new method to write signature box
    def signature(self):
        # Define the data for the table
        data = [[f"{' '*14}Signature"], [f"{' '*40}\n{' '*40}\n{' '*40}\n{' '*40}\n{' '*40}"]]

        self.create_table(data, (14.54, 5), self.SIGNATURE_BOX_POSITION, params=[('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Add new method to draw line below self info table
    def draw_lines(self):
        self.canvas.setLineWidth(1)  
        self.canvas.setStrokeColor(colors.darkgrey)  
        self.canvas.line(2 * cm, 19.2 * cm, 2 * cm + 17.75 * cm, 19.2 * cm)
        self.canvas.line(1.9 * cm, 6.2 * cm, 1.9 * cm + 17.75 * cm, 6.2 * cm)  # Draw the line




invoice_data = {
        'buyer_name': 'Sugar Cosmetics',
        'items': [
            {'Sr. No.': '1', 'Date': "05/06/2024", 'Vehicle Number': "MH26BJ2089", "Trip": "Mumbai to Pune", "Amount": 8000},
            {'Sr. No.': '2', 'Date': "05/06/2024", 'Vehicle Number': "MH26AI2669", "Trip": "Daman to Pune", "Amount": 8000},
            {'Sr. No.': '3', 'Date': "05/06/2024", 'Vehicle Number': "MH26BJ2089", "Trip": "Mumbai to Pune", "Amount": 8000},
        ]  
    }

#generator = InvoiceGenerator(invoice_data['buyer_name'], invoice_data['items'])
#generator.generate_invoice(logo='assets/title.png')


class LRGenerator:
    LOGO_POSITION = (2, 24)
    LOGO_SIZE = (3, 2.2)
    FROM_TO = (15, 21)
    SELF_TABLE_POSITION = (2, 21) #(3.6, 2)
    ITEM_DETAILS = (2, 8.5)
    CONSIGNEE = (2, 15)
    CONSIGNER = (2, 19)  
    SIGNATURE = (17, 6)

    def __init__(self, items, filename='invoice'):
        self.items = items
        self.filename = filename + ".pdf"


    def text(self, text, x, y, line_height=0.015, font_name="Muli", font_size=16, color=colors.black):
        # Set font, size, and color
        self.canvas.setFont(font_name, font_size)
        self.canvas.setFillColor(color)
        y = y
        for line in text.split("\n"):
            self.canvas.drawString(x * cm, y * cm, line)
            y -= line_height * cm

    def box(self, x, y, width, height, color=colors.darkgrey):
        x = x * cm
        y = y * cm
        width = width * cm
        height = height * cm

        # Draw a rectangle
        self.canvas.setStrokeColor(color)
        self.canvas.rect(x, y, width, height)

    def create_table(self, data, size, position, params=[]):
        # Define the style of the table

        default = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Light grey background for the first row
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Black text color for the first row
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Left alignment for all cells
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Middle alignment for all cells
            #('GRID', (0, 0), (-1, -1), 1, colors.darkgrey),  # Black border with width 1 for all cells
            ('FONT', (0, 0), (-1, -1), 'Muli', 12)  # Muli font for all cells
        ]

        if params:
            default.extend(params)

        style = TableStyle(default)
        table = Table(data)
        table.setStyle(style)

        x , y = position
        width, height = size 
        table.wrapOn(self.canvas, width * cm, height * cm) 
        table.drawOn(self.canvas, x * cm, y * cm)

    def generate_invoice(self):
        self.canvas = canvas.Canvas(self.filename, pagesize=letter)
        pdfmetrics.registerFont(TTFont('Muli', 'assets/muli.ttf'))
        pdfmetrics.registerFont(TTFont('Arial', 'assets/arial.ttf'))
        pdfmetrics.registerFont(TTFont('Hindi', 'assets/devanagari.ttf'))

        self.add_logo(self.canvas, 'assets/logo.png')
        self.consignee()
        self.weight_charge()
        self.header_boxes()
        self.draw_lines()
        self.item_details()
        self.footer()

        self.canvas.save()

    def add_logo(self, canvas, logo):
        x, y = self.LOGO_POSITION
        w, h = self.LOGO_SIZE
        canvas.drawImage(logo, x*cm, y*cm, width=w*cm, height=h*cm, mask='auto')
        #----------------------------------------------------------------
        self.text("ॐ नमो नमः", 10, 27, font_name="Hindi", font_size=12)
        self.text("TRIMURTI TEMPO SERVICES", 5.5, 25.5, font_name="Helvetica-Bold", font_size=28)
        self.text("SHOP NO.04, NEAR BALAJI KATTA, TALEGAON-CHAKAN ROAD, MAHALUNGE,\nTAL-KHED, PUNE, 410501,   Email - tts@gmail.com\nMobile Number - 9327383095, 7046689999", 5.5, 25, font_name="Muli", font_size=8)
        
    def header_boxes(self):
        self.box(2, 21, 5.3, 2)
        self.text("Shivanand V. Sakhare\nPAN NO. BDHPS3373P", 2.3, 22.3, line_height=0.027, font_size=12)
        self.box(8, 21, 5.5, 2)
        self.text("This consignment will not be detained\ndiverted re-routed without consignee.\nBank permission will be delivered at\nthe destination", 8.2, 22.5, line_height=0.015, font_size=8)
        self.box(14.4, 21, 5.3, 2)
        self.text(f"LR NO. {self.items['LR']}\nDate: {self.items['date']}", 14.6, 22.3, line_height=0.027, font_size=12)
        #----------------------------------------------------------------
        self.box(2, 19, 5.3, 2)
        self.text("Address of Delivery:\nDoor-To-Door Delivery", 2.2, 20.3, line_height=0.027, font_size=12)
        self.box(8, 19, 5.5, 2)
        self.text(f"Vehicle Number:\n{self.items['vehicle_number']}", 8.2, 20.3, line_height=0.027, font_size=12)
        self.box(14.4, 19, 5.3, 2)
        self.text(f"From: {self.items['from'].title()}\nTo: {self.items['to'].title()}", 14.6, 20.3, line_height=0.027, font_size=12)
        #----------------------------------------------------------------
        self.text("Subject to Pune Jurisdiction", 8.6, 1.7, font_size=12)
        self.text("Driver Copy", 16.7, 26.9, font_name="Muli", font_size=12)

    def weight_charge(self):
        data = [["Actual\nWeight Kg", "Weight\nCharged Kg"],
                ["Fix", "Fix"]]
        
        self.create_table(data, (14.54, 1.5), (15, 16), params=[('FONT', (0, 0), (-1, -1), 'Muli', 10)])

    def item_details(self):
        # Define the data for the table
        data = [["No. of Packages", "Description", "Rate", "Paid", "To-Pay"],
                [self.items['no_of_packages'], self.items['description'], "Rate per Qty", self.items['suboptions']['rate_per_qty_paid'], self.items['suboptions']['rate_per_qty_to_pay']],
                ["", "", "Sur. Charge", self.items['suboptions']['sur_charge_paid'], self.items['suboptions']['sur_charge_to_pay']],
                ["", "", "Cover Charge", self.items['suboptions']['cover_charge_paid'], self.items['suboptions']['cover_charge_to_pay']],
                ["", "", "St. Charge", self.items['suboptions']['st_charge_paid'], self.items['suboptions']['st_charge_to_pay']],
                ["", "", "Hamali", self.items['suboptions']['hamali_paid'], self.items['suboptions']['hamali_to_pay']],
                ["", "", "Other Charge", self.items['suboptions']['other_charge_paid'], self.items['suboptions']['other_charge_to_pay']],
                ["Value Rs: ", f"{self.items['value_rs']}/-", "Total", "-", f"{self.items['total']}/-"],
                ]

        self.create_table(data, (14.54, 1.5), self.ITEM_DETAILS) #params=[('GRID', (0, 0), (-1, -1), 1, colors.dimgrey)])

    # Add new method to write payment details table
    def consignee(self):
        # Define the data for the table
        data = [["Consignee", f"{self.items['consignee']},"],
                ["", self.items['consignee_address']],
                ["Consigner", f"{self.items['consigner']},"],
                ["", self.items['consigner_address']]]
                
        self.create_table(data, (14.54, 1.5), self.CONSIGNEE, params=[('BACKGROUND', (0, 0), (0, 0), colors.lightgrey), ('BACKGROUND', (0, 2), (0, 2), colors.lightgrey), ('BACKGROUND', (-1, 0), (-1, 0), colors.white)])

    def footer(self):
        # Define the data for the table
        x, y = self.SIGNATURE
        #self.text("", 2, 6, font_size=12)
        self.text("Signature", x, y, font_size=12)
        self.text("Not responsible for Leakage, Breakage or Damage", 6, 1, font_size=12)

    # Add new method to draw line below self info table
    def draw_lines(self):
        self.canvas.setLineWidth(1)  
        self.canvas.setStrokeColor(colors.darkgrey)  
        self.canvas.line(1.9 * cm, 18.2 * cm, 1.9 * cm + 17.75 * cm, 18.2 * cm)
        self.canvas.line(1.9 * cm, 14.6 * cm, 1.9 * cm + 17.75 * cm, 14.6 * cm)  # Draw the line 
        self.canvas.line(1.9 * cm, 8 * cm, 1.9 * cm + 17.75 * cm, 8 * cm)  # Draw the line 


#generator = LRGenerator()
#generator.generate_invoice()
        