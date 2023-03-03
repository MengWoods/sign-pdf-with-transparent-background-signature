# PDFmanipulation

Manipulate PDF (Portable Document Format) files with functions such as adding signature, merging PDFs, cutting PDFs, OCR, etc.

## Requirements
- Python 3.7
- PyPDF2 3.0.1
- configargparse 1.5.3
- coloredlogs 15.0.1

## Usage

Put the input files to `./files` folder, and `python main.py -h` check how to use it.

Here are some usage examples assuming you have `a.pdf` and `b.pdf` in `./files` folder:
```bash
# OCR to txt file
python main.py -t ocr -i a.pdf
# Merge PDFs to one
python main.py -t merge -i a.pdf b.pdf
```

## TODO
- [ ] Add watermark
- [ ] Add signature
