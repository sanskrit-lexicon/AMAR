# AMAR
Convert Amarakosha to CDSD format

# amar1.txt

File copied from https://github.com/drdhaval2785/sanskrit-lexica-ocr/blob/master/namalinganushasana_amarasinha/orig/namalinganushasana.txt and renamed as amar1.txt as on 30 Jan 2024.

# scripts

addinfo.py, convert.py, gender_list.py, transcoder.py, transcoder folder and redo.sh copied from https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/amar/prep folder as on 30 Jan 2024. 
redo.sh is modified to give filenames of the present project.

# Notes on further steps:

```
mkdir csl-orig/amar
cp AMAR/amar.txt csl-orig/amar/amar.txt
touch csl-orig/amar/amar-meta2.txt
touch csl-orig/amar/amar_hwextra.txt
touch csl-orig/amar/amarheader.xml  # note this to be modified later
```

edit csl-pywork/dictparms.py

// add info for amar

edit csl-pywork/inventory.txt

// add info for amar

edit csl-pywork/redo_xampp_all.sh

edit csl-pywork/redo_cologne_all.sh

edit csl-websanlexicon/dictparms.py

//add info for amar

```
mkdir csl-websanlexicon/distinctfiles/amar
mkdir csl-websanlexicon/distinctfiles/amar/web
mkdir csl-websanlexicon/distinctfiles/amar/web/webtc
echo "0001:pg_0001.pdf" >  csl-websanlexicon/distinctfiles/amar/web/webtc/pdffiles.txt
```

edit csl-pywork/makotemplates/pywork/hw.py

 add init_keys for amar

edit csl-pywork/makotemplates/pywork/redo_xml.sh

  SKIP amar1.xml

edit csl-pywork/makotemplates/pywork/make_xml.py

 construct_xmlstring_1 (for anhk)

 construct_xmlstring_2 (for amar)

gender-frequency list
```
python gender_list.py amar.txt gender_list.txt
```


