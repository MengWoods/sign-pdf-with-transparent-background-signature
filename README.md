# sign-pdf-with-transparent-background-signature

Sign PDF file with signature photo input, the tool extracts signature trace and merge it into PDF with specific page, postions and scale values. 

Besides it, the repo supports other operations such as PDF's merging, splitting, OCR, watermarking, and make transparent signature picture based on the input photo.

## Introduction

The tool takes PDF and signature image inputs and output a signed PDF file. 

![example result](./resource/introduction.png)

In the picture above, you could see an example of the input photo and output result, the full signed PDF can be found from [files/example-pdf_signed.pdf](./files/example-pdf_signed.pdf):

## Requirements
- If you have virtual env installed [Virtualenv](https://virtualenv.pypa.io/en/latest/): 
  - In the repository root path, activate virtual python envrionment by `source .venv/bin/activate`. 

- Or if you prefer to install dependencies yourself:
  - In Python 3.X environment, install by `pip install -r requirements.txt` in repository root path.

## Usage

Put the input files to `./files` folder, and `python main.py -h` to check arguments meaning.
Here lists essential arguments for signing PDF:
```python
'-b', '--base-path', default='./files', type=str, help='Base path to the PDF files for processing'
'-t', '--type-of-manipulation', required=True, type=str, \
      choices=['ocr', 'merge', 'split', 'split2image', 'watermark', 'signature', 'make-signature']
'-i', '--input-files', required=True, nargs='+', help="Input PDF files name(s), add space between two files"
'-s', '--signature-file', type=str, help="Sinature picture file name"
'-n', '--signature-page-num', type=int, default=1, help="Signature page number [1, +Inf) of PDF file"
'-o', '--signature-offset-xy', type=parse_two_numbers, default=[0,0], help="Offset proportion of x and y coordinates of the signature. Range is [0,1]"
'-c', '--signature-scale', type=float, default=1, help="Scale (0,+inf) the input sgnature file, set it to negative value if need rotate signature"
'-g', '--gray-threshold', type=float, default=100, help="Gray threshold [0,255] to process signature image"
# The color is only used for signature file generation use.
'--color', type=str, default='black', help='Define the color of output signature'
```

### Sign name to PDF

- Take a signature photo such as the [example](./files/example-signature.jpg).
- Put the signature photo and PDF file to `./files` folder.
- Select the signature page (`-n`), gray threshold (`-g`), scale (`-c`), and offset proportions (`-o`), the later two arguments might need try a few times to get best results.
  - Page starts from 1.
  - Gray threshold's range is [0, 255], it is used to extract signature from photo, the default value should be enough for most cases. If not, adjust it and check result. 
  - Scale's range is [0, +inf), usually needs to decrease the signature size such as 0.3. Set it to negative value will rotate signature.
  - Offset proportion is in X,Y oder, the top-left corner of the PDF page is the origin, Y is horizontal and X is vertical. Range is [0,1]. See below picture for a reference.
<p align="center">
    <a href="https:/" target="_blank" rel="noopener noreferrer">
        <img width="300" src="resource/position_refer.png" alt="PDFium Library Logo">
    </a>
</p>

- With above, run the program to sign signature. The examples signed [PDF](./files/example-pdf_signed.pdf) uses this command:
  ```
  python main.py -t signature -i example-pdf.pdf -s example-signature.jpg -c 0.2 -n 2 -o 0.65,0.72
  ```
- One reference command:
  ```bash
  python main.py -t signature -i 1.pdf -s name_photo.jpg -c 0.26 -n 3 -o 0.26,0.6 -g 150
  ```
### Other supported operations

Here are some other usage examples assuming you have input files in the `./files` folder:
- OCR pdf and save to txt file
 `python main.py -t ocr -i a.pdf`
- Merge mulitple PDFs into one PDF
 `python main.py -t merge -i a.pdf b.pdf`
- Split one PDF to multiple PDFs
 `python main.py -t split -i a.pdf`
- Split one PDF to multiple PNG images
  `python main.py -t split2image -i a.pdf`
- Add watermark to all pages of PDF file
`python main.py -t watermark -i a.pdf -w watermark.pdf`;
  Add watermark to first (or last) page only
`python main.py -t watermakr -i a.pdf -w watermark.pdf -p first`

To create transparent-background signature in GIF format assuming the input photo is in the `./files` folder:
 - Typical operation
 `python main.py -t make-signature -i example-signature.jpg --color blue`

## TODO
- [ ] Publish Pypi package.
- [ ] Add frontend webpage.
- [x] Add .venv to the repo
- [ ] After converting, the file size is increased. Find reason and solve it.


