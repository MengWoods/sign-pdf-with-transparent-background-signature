#!/usr/bin/python3
import PyPDF2
import os
import utils.constant as ct

def ocrAndSaveTxt(path_to_file):
    pdfFile = open(path_to_file,'rb')
    ct.logger.info('Loading file: %s' % os.path.basename(path_to_file))
    pdfReader = PyPDF2.PdfReader(pdfFile)
    ct.logger.info("Total pages are: %i" % len(pdfReader.pages))
    with open(path_to_file + '.txt', 'w') as f:
        for i in range (len(pdfReader.pages)):
            page = pdfReader.pages[i]
            f.write(page.extract_text())
    pdfFile.close()
    ct.logger.info("TXT file is saved to: %s" % (path_to_file + '.txt'))

def mergeFiles(input_pdfs, output_file):
    pdfMerger = PyPDF2.PdfMerger()
    for pdf in input_pdfs:
        ct.logger.info('Loading file: %s' % os.path.basename(pdf))
        with open(pdf,'rb') as f:
            pdfMerger.append(f)
    with open(output_file,'wb') as f:
        pdfMerger.write(f)
    ct.logger.info('Merged file saved: %s' % os.path.basename(output_file))