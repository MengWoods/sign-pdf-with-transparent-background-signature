#!/usr/bin/python3
import os
# Image operation
from PIL import Image
import cv2
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
# PDF operation
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from pdf2image import convert_from_path
# Math
from math import floor
import numpy as np
# Internal lib
import utils.constant as ct

class pdfUtils:
    def __init__(self, base_path, pdf_file_list):
        self.file_name_list = pdf_file_list
        self.file_name = os.path.basename(pdf_file_list[0])
        self.file_name_without_extenstion = os.path.splitext(self.file_name)[0]
        self.relative_path = base_path
        self.absolute_path = os.path.abspath(self.relative_path)
    
    def ocrAndSaveTxt(self):
        for i in range(len(self.file_name_list)):
            with open(self.absolute_path + '/' + self.file_name_list[i], 'rb') as pdf:
                pdf_reader = PdfReader(pdf)
                saved_txt_path = \
                    self.absolute_path + '/' + os.path.splitext(self.file_name_list[i])[0] + '.txt'
                ct.logger.info('Loading file: %s' % self.file_name_list[i])
                with open(saved_txt_path, 'w') as f:
                    for j in range (len(pdf_reader.pages)):
                        page = pdf_reader.pages[j]
                        f.write(page.extract_text())
                pdf.close()
                ct.logger.info("TXT file is saved to: %s" % (saved_txt_path))

    def mergePdfs(self):
        pdf_merger = PdfMerger()
        for i in range(len(self.file_name_list)):
            ct.logger.info('Loading file: %s' % self.file_name_list[i])
            with open(self.absolute_path + '/' + self.file_name_list[i], 'rb') as pdf:
                pdf_merger.append(pdf)
        output_path = self.absolute_path + '/' + self.file_name_without_extenstion + '_merged.pdf'
        with open(output_path,'wb') as f:
            pdf_merger.write(f)
        ct.logger.info('Merged file is saved to: %s' % output_path)

    def splitPdf(self):
        with open(self.absolute_path + '/' + self.file_name_list[0], 'rb') as f:
            pdf_reader = PdfReader(f)
            # Iterate over each page and create a new PDF for each page
            for page_num in range(len(pdf_reader.pages)):
                writer = PdfWriter()
                writer.add_page(pdf_reader.pages[page_num])
                # Write the new PDF file
                output_path = self.absolute_path + '/' + \
                    self.file_name_without_extenstion + '_page_' + str(page_num) + '.pdf'
                with open(output_path, 'wb') as out:
                    writer.write(out)
        ct.logger.info('Split files are saved to: %s' % self.absolute_path)

    def watermark(self, input_watermark, add_to_page):
        pdf_out = PdfWriter()
        ct.logger.info('Loading pdf file: %s' % self.file_name_list[0])
        with open(self.absolute_path + '/' + self.file_name_list[0], 'rb') as f:
            pdf_reader = PdfReader(f)
            ct.logger.info('Loading watermark file: %s' % os.path.basename(input_watermark))
            watermark = PdfReader(open(self.absolute_path + '/' + input_watermark, 'rb'), strict=False)

            for i in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[i]
                if add_to_page == 'all':
                    page.merge_page(watermark.pages[0])
                elif add_to_page == 'first':
                    if i == 0:
                        page.merge_page(watermark.pages[0])
                elif add_to_page == 'last':
                    if i == len(pdf_reader.pages) - 1:
                        page.merge_page(watermark.pages[0])
                page.compress_content_streams()
                pdf_out.add_page(page)
            output_path = self.absolute_path + '/' + \
                    self.file_name_without_extenstion + '_watermark.pdf'
            with open(output_path, 'wb') as out:
                pdf_out.write(out)
            ct.logger.info('Watermarked file is saved to: %s' % output_path)

    def signature(self, input_signature, page, offset_xy, scale, gray_threshold):
        temp_path = self.absolute_path + "/temp"
        isExist = os.path.exists(temp_path)
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        pdf_width = 0
        pdf_height = 0
        # Split PDF to multiple ones
        with open(self.absolute_path + '/' + self.file_name_list[0], 'rb') as f:
            pdf_reader = PdfReader(f)
            page_width = pdf_reader.pages[0].mediabox.width
            page_height = pdf_reader.pages[0].mediabox.height
            # Iterate over each page and create a new PDF for each page
            for page_num in range(len(pdf_reader.pages)):
                writer = PdfWriter()
                writer.add_page(pdf_reader.pages[page_num])
                # Write the new PDF file
                output_filename = temp_path + '/' + self.file_name_without_extenstion + '_page_' + str(page_num) + '.pdf'
                with open(output_filename, 'wb') as out:
                    writer.write(out)
        # Image processing
        page_to_be_signed = temp_path + '/' + self.file_name_without_extenstion + '_page_' + str(page-1)
        images = convert_from_path(page_to_be_signed + '.pdf')
        images[0].save(page_to_be_signed + '.jpg', 'JPEG')
        os.remove(page_to_be_signed + '.pdf')
        cv_page = cv2.imread(page_to_be_signed + '.jpg')
        cv_signature = cv2.imread(self.absolute_path + '/' + input_signature)
        # Size check
        if cv_signature.shape[0] > cv_page.shape[0] or cv_signature.shape[1] > cv_page.shape[1]:
            scale_min = floor(min(cv_page.shape[0]/cv_signature.shape[0], cv_page.shape[1]/cv_signature.shape[1]))
            if scale > scale_min: scale = scale_min
        # denoise
        cv_signature = cv2.bilateralFilter(cv_signature, 10, 75, 75)
        cv_signature = cv2.cvtColor(cv_signature, cv2.COLOR_BGR2GRAY)
        ret, cv_signature = cv2.threshold(cv_signature, gray_threshold, 255, cv2.THRESH_BINARY)
        cv_signature = cv2.bilateralFilter(cv_signature, 10, 75, 75)
        indices = np.where(cv_signature == 0)
        # Convert the indices to pixel coordinates
        signature_coords = np.transpose(indices)
        signature_coords = signature_coords * scale
        signature_coords = signature_coords + offset_xy
        # Plot signature to cv page
        for coord in signature_coords:
            cv_page[int(coord[0]), int(coord[1])] = 0
        cv2.imwrite(page_to_be_signed + '.jpg', cv_page)
        # Convert cv page to PDF page
        c = canvas.Canvas(page_to_be_signed + '.pdf' , pagesize=(page_width, page_height))
        c.drawImage(page_to_be_signed + '.jpg', 0, 0, float(page_width), float(page_height))
        os.remove(page_to_be_signed + '.jpg')
        c.save()
        # Merge PDFs to PDF and save
        output_pdf = PyPDF2.PdfWriter()
        for i in range(len(pdf_reader.pages)):
            pdf_file = open(temp_path + '/' + self.file_name_without_extenstion + '_page_' + str(i) + '.pdf', 'rb')
            input_pdf_reader = PdfReader(pdf_file)
            for page in range(len(input_pdf_reader.pages)):
                output_pdf.add_page(input_pdf_reader.pages[page])
        output_path = self.absolute_path + '/' + \
                    self.file_name_without_extenstion + '_signed.pdf'
        with open(output_path, 'wb') as output_file:
            output_pdf.write(output_file)
        for file_name in os.listdir(temp_path):
            file_path = os.path.join(temp_path, file_name)
            os.remove(file_path)
        os.rmdir(temp_path)
        ct.logger.info('Signed file is saved to: %s' % output_path)