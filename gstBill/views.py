from turtle import left
from django.http import Http404
from rest_framework.decorators import api_view
from django.http import JsonResponse,FileResponse
import json

from fpdf import FPDF



@api_view(["POST"])
def invoice(argument):
    try:
        data = json.loads(argument.body)
        # data = {"clientDetails":{"invoiceNo":"001","invoiceDate":"26/9/2022","companyName":"company","companyAddress":"Chethana\nCentre for neuropsychiatry\nMalaparamba,Calicut\n0495-2378825","oldBalance":"200", "gstNo":"32AALFC7052K1ZD"},"itemDetails":[{"itemName":"BANA FEAST (flavoured banana chips)","HSN":"20081940","qty":"24","unitPrice":"36.44","total":"874.56"}],"subTotal":"600.00","subTotalPieces":"20","subTotalWeight":"200","netPayable":"1340.00"}

        # data = {"clientDetails":{"invoiceNo":"001","invoiceDate":"10/11/2022","companyName":"alkjf \naf a'f\nafkaf","clientGST":"65649843"},"items":[{"itemName":"BANA FEAST (flavoured banana chips)","HSN":"20081940","quantity":"24","unitPrice":"36.44","Total":"874.56"}],"subTotal":"874.56","grandTotal":"1031.98","tax":"157.42","total":"1032","roundOff":"0.02"}


        tableHeadings = ["DESCRIPTION","HSN CODE","QTY (Pcs)","UNIT PRICE","TOTAL"]
        column_widths = [75, 25, 25, 25, 30]


        #Header and Footer
        class PDF(FPDF):
            def header(self):
                # Header Image
                self.image('gstBill/static/images/header.png', 0, 0, pdf.w)
                # Line break
                self.ln(40)

            def footer(self):
                # Footer
                self.image('gstBill/static/images/footer.png', 0, pdf.h-48, pdf.w)
        

        pdf = PDF('P', 'mm', 'A4')

        #Add font
        # pdf.add_font('Montserrat', '', 'pdf_generator/static/fonts/Montserrat/Montserrat-Regular.ttf', uni=True)
        # pdf.add_font('Montserrat', 'B', 'pdf_generator/static/fonts/Montserrat/Montserrat-Medium.ttf', uni=True)

        pdf.add_page()
        pdf.set_margin(15)
        pdf.set_font('Helvetica', '', 12)

        #Invoice number and date
        invoice_details_x = pdf.l_margin + 120
        pdf.set_font(style='B')
        pdf.set_x(invoice_details_x)
        pdf.cell(40, 5, 'INVOICE NO : ', align='R')
        pdf.set_font(style='')
        pdf.cell(0, 5, data['clientDetails']['invoiceNo'], align='L')
        pdf.set_font(style='B')
        pdf.ln()
        pdf.set_x(invoice_details_x)
        pdf.cell(40, 5, 'INVOICE DATE : ', align='R')
        pdf.set_font(style='')
        pdf.cell(0, 5, data['clientDetails']['invoiceDate'], new_x="LMARGIN", new_y="NEXT", align='L')

        #Client Details
        pdf.set_font(style='B', size=14)
        pdf.cell(0, 7, "Bill To", new_x="LMARGIN", new_y="NEXT", align='l')
        pdf.line(pdf.l_margin, pdf.y, pdf.l_margin + 50, pdf.y)
        pdf.set_font(style='', size=12)
        pdf.ln(1)
        pdf.multi_cell(50, 6, data["clientDetails"]["companyName"], new_x="LMARGIN", new_y="NEXT", align='l')
        pdf.set_font(style='B')
        pdf.cell(0, 8, "GST NO : " + data["clientDetails"]["clientGST"], new_x="LMARGIN", new_y="NEXT", align='l')
        
        pdf.ln(10)

        #Table
        line_height = 8
        #Table Headings
        pdf.set_font(style='B', size=10)
        pdf.set_draw_color(214,216,220)
        pdf.set_fill_color(217, 48, 48)
        pdf.set_text_color(255, 255, 255)

        heading_column_no = 0
        for datum in tableHeadings:
            pdf.cell(column_widths[heading_column_no], line_height, datum, border=1, align='C', new_x="RIGHT", new_y="TOP", fill=True)
            heading_column_no += 1
        pdf.ln(line_height)



        #Table Data
        pdf.set_font(style='', size=9.5)
        pdf.set_text_color(0, 0, 0)
        line_number = 0
        for row in data["items"]:
            column_number = 0
            for key in row:
                pdf.cell(column_widths[column_number], line_height*3,  row[key], border=1, new_x="RIGHT", new_y="TOP", align="C")
                column_number += 1
            pdf.ln(line_height*3)
            line_number += 1
        
        #Table Totals
        total_x = 100
        
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font(style='B')
        pdf.cell( total_x, line_height, "", new_x="RIGHT", new_y="TOP")
        pdf.cell( 50, line_height, "SUBTOTAL", border=1, new_x="RIGHT", new_y="TOP", align='L', fill=True)
        pdf.cell( 30, line_height, data["subTotal"], border=1, new_x="RIGHT", new_y="TOP", align='R', fill=True)
        pdf.ln(line_height)
        pdf.cell( total_x, line_height, "", new_x="RIGHT", new_y="TOP")
        pdf.cell( 50, line_height, "TAX RATE", border=1, align='L', new_x="RIGHT", new_y="TOP")
        pdf.cell( 30, line_height, "18%", border=1, align='R', new_x="RIGHT", new_y="TOP")
        pdf.ln(line_height)
        pdf.cell( total_x, line_height, "", new_x="RIGHT", new_y="TOP")
        pdf.cell( 50, line_height, "TOTAL TAX", border=1, align='L', new_x="RIGHT", new_y="TOP", fill=True)
        pdf.cell( 30, line_height, data["tax"], border=1, align='R', new_x="RIGHT", new_y="TOP", fill=True)
        pdf.ln(line_height)
        pdf.cell( total_x, line_height, "", new_x="RIGHT", new_y="TOP")
        pdf.cell( 50, line_height, "ROUND OFF", border=1, align='L', new_x="RIGHT", new_y="TOP")
        pdf.cell( 30, line_height, data["roundOff"], border=1, align='R', new_x="RIGHT", new_y="TOP")
        pdf.ln(line_height)
        pdf.cell( total_x, line_height*1.5, "", new_x="RIGHT", new_y="TOP")
        pdf.set_font_size(15)
        pdf.cell( 50, line_height*1.5, "TOTAL AMOUNT :", align='L', new_x="RIGHT", new_y="TOP")
        pdf.cell( 30, line_height*1.5,"Rs. " + data["total"], align='R', new_x="RIGHT", new_y="TOP",)
        pdf.ln(line_height)

        pdf.set_y(pdf.h-25)
        pdf.set_font(style='', size=12)
        pdf.cell(0,0, "Authorised Signature      ", align='R')
        pdf.ln(line_height)
        pdf.set_font(size=10)
        pdf.cell(0,0, "Thank You for cooperating with Tastier Agro Foods", align='C')


        


        #Print pdf
        pdf.output('invoice.pdf')
        return FileResponse(open('invoice.pdf', 'rb'), as_attachment=True, content_type='application/pdf')

    except ValueError:
        return JsonResponse({"error": "wrong data"})