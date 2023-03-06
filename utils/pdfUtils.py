#!/usr/bin/python3
import PyPDF2
import os
import utils.constant as ct
# from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pdf2image import convert_from_path
from PIL import Image
import cv2
import numpy as np
import img2pdf
from math import floor

def ocrAndSaveTxt(input_pdf):
    pdfFile = open(input_pdf,'rb')
    ct.logger.info('Loading file: %s' % os.path.basename(input_pdf))
    pdfReader = PyPDF2.PdfReader(pdfFile)
    ct.logger.info("Total pages are: %i" % len(pdfReader.pages))
    with open(input_pdf + '.txt', 'w') as f:
        for i in range (len(pdfReader.pages)):
            page = pdfReader.pages[i]
            f.write(page.extract_text())
    pdfFile.close()
    ct.logger.info("TXT file is saved to: %s" % (input_pdf + '.txt'))

def mergeFiles(input_pdfs, output_file):
    pdfMerger = PyPDF2.PdfMerger()
    for pdf in input_pdfs:
        ct.logger.info('Loading file: %s' % os.path.basename(pdf))
        with open(pdf,'rb') as f:
            pdfMerger.append(f)
    with open(output_file,'wb') as f:
        pdfMerger.write(f)
    ct.logger.info('Merged file saved: %s' % os.path.basename(output_file))

def watermark(input_pdf, input_watermark, add_to_page):
    pdfOut = PyPDF2.PdfWriter()
    ct.logger.info('Loading pdf file: %s' % os.path.basename(input_pdf))
    pdfFile = open(input_pdf, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFile)
    ct.logger.info('Loading watermark file: %s' % os.path.basename(input_watermark))
    pdfWatermark = PyPDF2.PdfReader(open(input_watermark, 'rb'), strict=False)
    ct.logger.info('Adding watermark to %s page(s)' % add_to_page)
    for i in range(len(pdfReader.pages)):
        page = pdfReader.pages[i]
        if add_to_page == 'all':
            page.merge_page(pdfWatermark.pages[0])
        elif add_to_page == 'first':
            if i == 0:
                page.merge_page(pdfWatermark.pages[0])
        elif add_to_page == 'last':
            if i == len(pdfReader.pages) - 1:
                page.merge_page(pdfWatermark.pages[0])
        page.compress_content_streams()
        pdfOut.add_page(page)
    pdfOut.write(open(input_pdf + "_watermark.pdf", 'wb'))
    ct.logger.info('Watermarked file saved to: %s' % os.path.basename(input_pdf + "_watermark.pdf"))

def signature(input_pdf, input_signature, page, offset_xy, scale, gray_threshold):
    fileName = os.path.basename(input_pdf)
    fileNameWithoutExtenstion = os.path.splitext(fileName)[0]
    
    pathRela = os.path.dirname(input_pdf)
    pathAbs = os.path.abspath(pathRela)
    pathTemp = pathAbs + "/temp"
    isExist = os.path.exists(pathTemp)
    if not isExist:
        os.makedirs(pathTemp)

    pdf_reader = PyPDF2.PdfReader(input_pdf)
    # Get the dimensions (width and height) of the first page in the PDF file
    page_width = 0
    page_height = 0

    # Split PDF to multiple ones
    with open(input_pdf, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        page_1 = pdf_reader.pages[0]
        page_width = page_1.mediabox.width
        page_height = page_1.mediabox.height
        # Iterate over each page and create a new PDF for each page
        for page_num in range(len(pdf.pages)):
            writer = PyPDF2.PdfWriter()
            writer.add_page(pdf.pages[page_num])

            # Write the new PDF file
            output_filename = pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(page_num) + '.pdf'
            with open(output_filename, 'wb') as out:
                writer.write(out)

    image = convert_from_path(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(page-1) + '.pdf')
    image[0].save(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(page-1) + '.jpg', 'JPEG')
    os.remove(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(page-1) + '.pdf')

    pdfPage = cv2.imread(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(page-1) + '.jpg') 
    signature = cv2.imread(input_signature)
    if signature.shape[0] > pdfPage.shape[0] or signature.shape[1] > pdfPage.shape[1]:
         scale_ = floor(min(pdfPage.shape[0]/signature.shape[0], pdfPage.shape[1]/signature.shape[1]))
         if scale > scale_: scale = scale_
    signatureGray = cv2.cvtColor(signature, cv2.COLOR_BGR2GRAY)
    signatureCoords = np.column_stack(np.where(signatureGray < gray_threshold))
    signatureCoords = signatureCoords * scale
    signatureCoords = signatureCoords + offset_xy
    for coord in signatureCoords:
        pdfPage[int(coord[0]), int(coord[1])] = 0
    cv2.imwrite(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(page-1) + '.jpg', pdfPage)
    # convert the image to pdf
    c = canvas.Canvas(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(page-1) + '.pdf' , pagesize=(page_width, page_height))
    c.drawImage(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(page-1) + '.jpg', 0, 0, page_width, page_height)
    os.remove(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(page-1) + '.jpg')
    c.save()

    output_pdf = PyPDF2.PdfWriter()
    for i in range(len(pdf.pages)):
        pdf_file = open(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(i) + '.pdf', 'rb')
        input_pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in range(len(input_pdf_reader.pages)):
            output_pdf.add_page(input_pdf_reader.pages[page])
    with open(input_pdf + '_signed.pdf', 'wb') as output_file:
        output_pdf.write(output_file)
    for file_name in os.listdir(pathAbs + '/temp/'):
        file_path = os.path.join(pathAbs + '/temp/', file_name)
        os.remove(file_path)
    os.rmdir(pathAbs + '/temp/')