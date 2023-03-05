# signPDF

Sign PDF file with signature photo, the tool extracts signature trace and merge it into PDF with specific page, postions and scale values. Besides it, the repo supports other PDF operation such as merge, OCR, watermark functions.

## Introduction

The tool takes PDF and signature image inputs and output a signed PDF file.
![example result](./resource/introduction.png)

In the picture above, you could see an example of the input photo and output result, the full signed PDF can be found from [files/example-pdf.pdf_signed.pdf](./files/example-pdf.pdf_signed.pdf):


## Requirements
In Python 3.7 environment, install dependencies with `pip install -r requirements.txt`.

## Usage

Put the input files to `./files` folder, and `python main.py -h` to check arguments meaning.

Here are some usage examples assuming you have input files in the `./files` folder:
- OCR pdf and save to txt file
 `python main.py -t ocr -i a.pdf`
- Merge mulitple PDFs into one PDF
 `python main.py -t merge -i a.pdf b.pdf`
- Add watermark to all pages of PDF file
`python main.py -t watermark -i a.pdf -w watermark.pdf`;
  Add watermark to first (or last) page only
`python main.py -t watermakr -i a.pdf -w watermark.pdf -p first`
- Sign PDF file with input signature photo, examples can be found from `./files` folder.
`python main.py -t signature -i example-pdf.pdf -s example-signature.jpg -n 1 -c 0.2 -g 100 -o 1280,1000`

## TODO
- [ ] Create class for util codes.
- [ ] Refine codes with logger information, better argument naming rule.
- [ ] Use splitting PDF to PDFs function in signature function.
- [ ] Add details guide to use the toolbox.