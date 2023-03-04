# PDFmanipulation

Manipulate PDF (Portable Document Format) files with functions such as adding signature, merging PDFs, cutting PDFs, OCR, etc.

## Requirements
- Python 3.7
- PyPDF2 3.0.1
- configargparse 1.5.3
- coloredlogs 15.0.1

## Usage

Put the input files to `./files` folder, and `python main.py -h` to check arguments meaning.

Here are some usage examples assuming you have `a.pdf`, `b.pdf`, `watermark.pdf` in `./files` folder:
- OCR pdf and save to txt file: `python main.py -t ocr -i a.pdf`
- Merge mulitple PDFs into one PDF: `python main.py -t merge -i a.pdf b.pdf`
- Add watermark to every pages of PDF file: `python main.py -t watermark -i a.pdf -w watermark.pdf`

## TODO
- [x] Add watermark
- [ ] Add signature assigning postion
- [ ] Rotate a page
- [ ] Print basic info of PDF
- [ ] Separate a PDF to multiple ones