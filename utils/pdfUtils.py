#!/usr/bin/python3
import PyPDF2
import os
import utils.constant as ct

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
    
