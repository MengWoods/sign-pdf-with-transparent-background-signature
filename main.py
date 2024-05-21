#!/usr/bin/python3
# Internal libs
import utils.pdfUtils as ut
import utils.imgUtils as imgut
import utils.constant as con

def parse_two_numbers(value):
    numbers = value.split(',')
    if len(numbers) != 2:
        raise ValueError('List must contain exactly two numbers')
    try:
        return [float(numbers[0]), float(numbers[1])]
    except ValueError:
        raise ValueError('Invalid list format')

con.logger.info("The default folder of input/output files are ./files, put pdfs, signature there for processing.")
# Read configs
p = con.configargparse.ArgParser()
p.add('-b', '--base-path', default='./files', type=str, help='Base path to the PDF files for processing')
p.add('-t', '--type-of-manipulation', required=True, type=str, \
      choices=['ocr', 'merge', 'split', 'split2image', 'watermark', 'signature', 'make-signature'], \
      help="Type of PDF/Img manipulation")
p.add('-i', '--input-files', required=True, nargs='+', help="Input PDF or Img file name(s), add space between two files")
p.add('-w', '--watermark-file', type=str, help="Watermark PDF file name")
p.add('-p', '--watermark-page', type=str, choices=['first', 'last', 'all'], default='all', help="Add watermark to which page")
p.add('-s', '--signature-file', type=str, help="Sinature picture file name")
p.add('-n', '--signature-page-num', type=int, default=1, help="Signature page number [1, +Inf) of PDF file")
p.add('-o', '--signature-offset-xy', type=parse_two_numbers, default=[0,0], help="Offset proportion of x and y coordinates of the signature. Range is [0,1]")
p.add('-c', '--signature-scale', type=float, default=1, help="Scale (0,+inf) the input sgnature file, set it to negative value if need rotate signature")
p.add('-g', '--gray-threshold', type=float, default=100, help="Gray threshold [0,255] to process signature image")
# The color is only used for signature file generation use.
p.add('--color', type=str, default='black', help='Define the color of output signature')

options = p.parse_args()

def main():
    pdf_utils = ut.pdfUtils(options.base_path, options.input_files)

    if options.type_of_manipulation == 'ocr':
        pdf_utils.ocrAndSaveTxt()
    elif options.type_of_manipulation == 'merge':
        if len(options.input_files) == 1:
            con.logger.error("Merge operation needs at least 2 input files!")
        else:
            pdf_utils.mergePdfs()
    elif options.type_of_manipulation == 'split':
        if len(options.input_files) == 1:
            pdf_utils.splitPdf()
        else:
            con.logger.error("Split operation needs at max 1 input file!")
    elif options.type_of_manipulation == 'split2image':
        if len(options.input_files) == 1:
            pdf_utils.split2image()
        else:
            con.logger.error("Split operation needs at max 1 input file!")
    elif options.type_of_manipulation == 'watermark':
        if options.watermark_file == None:
            con.logger.error("Watermark file is needed as one input!")
        elif len(options.input_files) == 1:
            pdf_utils.watermark(options.watermark_file, options.watermark_page)
        else:
            con.logger.error("Watermark operation needs at max 1 input file!")
    elif options.type_of_manipulation == 'signature':
        if options.signature_file == None:
            con.logger.error("Signature file is needed as one input!")
        elif len(options.input_files) == 1:
            pdf_utils.signature(options.signature_file, \
                                options.signature_page_num,\
                                options.signature_offset_xy,\
                                options.signature_scale,\
                                options.gray_threshold)
        else:
            con.logger.error("Signature operation needs at max 1 input file!")
    elif options.type_of_manipulation == 'make-signature':
        image_utils = imgut.imgUtils(options.base_path, \
                                options.input_files, \
                                options.gray_threshold, \
                                options.color)
        image_utils.process()

if __name__ == "__main__":
    main()