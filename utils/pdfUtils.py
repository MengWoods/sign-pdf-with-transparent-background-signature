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
# from fpdf import FPDF

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

def signature(input_pdf, input_signature, page, offset_xy, scale):
    # os.path.splitext("/path/to/some/file.txt")[0]
    fileName = os.path.basename(input_pdf)
    fileNameWithoutExtenstion = os.path.splitext(fileName)[0]
    # fileName = 
    print(fileNameWithoutExtenstion)
    ######1 Conver PDF file to temp images
    images = convert_from_path(input_pdf)
    pathRela = os.path.dirname(input_pdf)
    pathAbs = os.path.abspath(pathRela)

    # dir = os.path.dirname(input_pdf)

    pathTemp = pathAbs + "/temp"
    # print(pathTemp)
    # print(pathAbs)
# Check whether the specified path exists or not
    isExist = os.path.exists(pathTemp)
    if not isExist:
        os.makedirs(pathTemp)

    # print(os.path.abspath(input_pdf))
    # print(input_pdf)
    # # print(dir)

    for i in range(len(images)):
        images[i].save(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(i) + '.jpg', 'JPEG')

    pdfPage = cv2.imread(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(page) + '.jpg')
    ######2 Open page and signature with open cv
    # pdfPage = cv2.cvtColor(np.array(images[page]), cv2.COLOR_RGB2BGR)
    # # pdfPage = cv2.imread(pathAbs + '/temp/' + fileNameWithoutExtenstion + 'page' + str(page-1) + '.jpg') 
    signature = cv2.imread(input_signature)
    # # add shape checking
    # print(pdfPage.shape)  
    # print(signature.shape)
    signatureGray = cv2.cvtColor(signature, cv2.COLOR_BGR2GRAY)
    signatureCoords = np.column_stack(np.where(signatureGray <= 150))
    signatureCoords = signatureCoords * scale
    signatureCoords = signatureCoords + offset_xy

    for coord in signatureCoords:
        pdfPage[int(coord[0]), int(coord[1])] = 0
    cv2.imwrite(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(page) + '.jpg', pdfPage)

    for image in range(len(images)):
        image_width, image_height = images[image].size
        c = canvas.Canvas(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(image) + '.pdf' , pagesize=(image_width, image_height))
        c.drawImage(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(image) + '.jpg', 0, 0, image_width, image_height)
        os.remove(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(image) + '.jpg')
        c.save()
    
    # Define the directory containing the input PDF files
    # dir_path = '/path/to/pdf/files'
    output_pdf = PyPDF2.PdfWriter()
    for i in range(len(images)):
        pdf_file = open(pathAbs + '/temp/' + fileNameWithoutExtenstion + '_page' + str(i) + '.pdf', 'rb')
        # with open(pdf_file, 'rb') as input:
        input_pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in range(len(input_pdf_reader.pages)):
            output_pdf.add_page(input_pdf_reader.pages[page])

    with open(input_pdf + '_signed.pdf', 'wb') as output_file:
        output_pdf.write(output_file)

