#!/usr/bin/python3
# Internal libs
import utils.pdfUtils as ut
import utils.constant as con

con.logger.info("The default folder of input/output files are ./files, put pdfs there for futher processing.")
# Read configs
p = con.configargparse.ArgParser()
p.add('-t', '--type-of-manipulation', required=True, type=str, choices=['ocr', 'merge', 'watermark'], help="Type of PDF manipulation")
p.add('-i', '--input-files', required=True, nargs='+', help="Input PDF files name(s), add space between two files")
p.add('-w', '--watermark-file', type=str, help="Watermark PDF file")
p.add('-p', '--watermark-page', type=str, choices=['first', 'last', 'all'], default='all', help="Add watermark to which page")
options = p.parse_args()

def main():
    BASE_PATH = './files/'

    if options.type_of_manipulation == 'ocr':
        if len(options.input_files) == 1:
            ut.ocrAndSaveTxt(BASE_PATH + options.input_files[0])
        else:
            con.logger.error("OCR manipulation accepts 1 input file per time!")

    elif options.type_of_manipulation == 'merge':
        if len(options.input_files) == 1:
            con.logger.error("Merge manipulation need at least 2 input files!")
        else:
            inputs = []
            for i in range(len(options.input_files)):
                inputs.append(BASE_PATH + options.input_files[i])
            ut.mergeFiles(inputs, inputs[0] + '_merged.pdf')
    
    elif options.type_of_manipulation == 'watermark':
        if len(options.input_files) == 1:
            ut.watermark(BASE_PATH + options.input_files[0], \
                         BASE_PATH + options.watermark_file, \
                         options.watermark_page)
        else:
            con.logger.error("Watermark manipulation accepts 1 input file per time!")

if __name__ == "__main__":
    main()