# LinkedBooksReferenceParsing: Annotations Dataset and CRF Parsing

TODO Zenodo
[![DOI](https://zenodo.org/badge/79789632.svg)](https://zenodo.org/badge/latestdoi/79789632)

A dataset of annotated references (in both reference lists and footnotes) from journal issues and monographs on the history of Venice, created in the context of the [LinkedBooks project](http://dhlab.epfl.ch/page-127959-en.html). 

The dataset contains annotated reference lists of monographs and annotated references from the footnotes of journal issues from the following journals (mostly, but not exclusively in Italian): Ateneo Veneto, Archvio Veneto, Studi Veneziani. This dataset was digitized, OCRed (using ABBYY FineReader) and annotated (using Brat ADD) from 2014 to 2016.

Along the dataset of annotations, a framework to train your own parsers is provided, based on Conditional Random Fields. Feel free to use it to build your own parser, and if you improve on our results, please let us know!

## Contents

* `LICENSE` CC BY 4.0.
* `README.md` this file.
* `dataset/`
    * [annotated_dataset](dataset/annotated_dataset.json.zip) The annotated dataset in json format (zip compressed).
    * [report.p](dataset/report.p) A set of statistics on the annotated dataset, pickled.
    * [report.txt](dataset/report.txt) A set of statistics on the annotated dataset, txt.
    * [sources](dataset/sources.csv) List of monographs and journal issues which have been annotated, with number of annotations for each. TODO Matteo (put id, issue, year, name of journal or monograph, number of annotations specific and generic).
* `M1.ipynb` a Python notebook to train a CRF parsing model using specific reference tags (e.g. author, title, publication year). You can use the annotated dataset in json format as input here.
* `M2.ipynb` a Python notebook to train a CRF parsing model using generic begin/end reference tags (e.g. begin-secondary, in-secondary, end-secondary for a reference to a secondary source).
* `models/`
    * [modelM1](models/modelM1_ALL_L.pkl) trained model 1, details in the paper.
    * [modelM2](models/modelM1_ALL_L.pkl) trained model 2, details in the paper.
* `code/`
    * [support_functions](code/support_functions.py) supporting functions for training/testing, plotting and parsing references.
    * [feature_extraction](code/feature_extraction_words.py) feature extraction functions, document level.
    * [feature_extraction_supporting_functions](code/feature_extraction_supporting_functions_words.py) feature extraction functions, token level.

## Example of entry in annotated dataset

The annotated dataset consists of a list of documents, either monographs or journal issues, which contain pages and lists of tokens with annotations. Note that only tokens from text lines with annotations are kept within the dataset, not all the contents, which would not comply with copyright. An entry could look as follows:

    ```json
    {
        "bid": "BVE0058909", # identifier of monograph or jounal. Find details here: http://id.sbn.it/bid/BVE0058909
        "doc_number": "", #issue number if an issue
        "doc_type": "monograph", #type of document: monpgraph or journal_issue
        "pages": { # dicionary with page number and list of contents for every page
            "2": { # page number
                "is_annotated": true, #is the page has been annotated (always at true in this dataset)
                "offsets": [ # list of offsets (tokens)
                    [ # every token is a list of lists with three main contents
                        [
                            "piGNATTi", # surface of the token
                            1964, # begin offset
                            1971, # end offset
                            297, # token number in the page
                            59, # line number where token is located
                            "BVE0058909" # identifier (same as above, use as feature for referencing style)
                        ],
                        [
                            false, # is Italics
                            false, # is Bold
                            "" # size of font (if available)
                        ],
                        [
                            "secondary-full", # generic tag
                            "author", # specific tag
                            "b", # begin/in/end/out tag
                            "b-secondary-full" # begin-end plus generic tag
                        ]
                    ],
                    [
                        [
                            "T.,",
                            1973,
                            1975,
                            298,
                            59,
                            "BVE0058909"
                        ],
                        [
                            false,
                            false,
                            ""
                        ],
                        [
                            "secondary-full",
                            "author",
                            "i",
                            "i-secondary-full"
                        ]
                    ],
                    ... # more offsets
                ],
                "page_id": "BVE0058909--page-0002", # identifier of the page
                "single_page_file_number": 2 # page number
            }
            ... # more pages
        }
    },
    ... # next entry (document).
    ```

## Annotation taxonomy
     
Taxonomy for generic tags. The main distinction is among primary sources (documents at an archive or rare books), secondary sources (monographs) and meta-annotations (for journal articles, contributions and other publications contained within another publication):

     'meta-annotation'
     'primary-full'
     'primary-partial'
     'secondary-full'
     'secondary-partial'
     
Taxonomy for begin'end tags:

    'b' # begin
    'e' # end
    'i' # in
    'o' # out
    
The taxonomy for generic begin-end annotations. Read as: `Tag (as in the dataset): ConsolidatedTag (as used in the paper's results: some tags are merged)`. The main change from the annotated dataset to the generic dataset has to do with the suppression of full and partial annotations:

     'b-primary-full': 'b-primary', # Primary source, full reference, begin
     'i-primary-full': 'i-primary', # Primary source, full reference, in
     'e-primary-full': 'e-primary', # Primary source, full reference, end
     'b-primary-partial': 'b-primary', # Primary source, partial reference, begin
     'i-primary-partial': 'i-primary', # Primary source, partial reference, in
     'e-primary-partial': 'e-primary', # Primary source, partial reference, end
     'b-meta-annotation': 'b-meta-annotation', # Meta source (journal article, contribution), begin
     'i-meta-annotation': 'i-meta-annotation', # Meta source (journal article, contribution), in
     'e-meta-annotation': 'e-meta-annotation', # Meta source (journal article, contribution), end
     'b-secondary-full': 'b-secondary', # Secondary source, full reference, begin
     'i-secondary-full': 'i-secondary', # Secondary source, full reference, in 
     'e-secondary-full': 'e-secondary',  # Secondary source, full reference, end
     'b-secondary-partial': 'b-secondary', # Secondary source, partial reference, begin
     'i-secondary-partial': 'i-secondary', # Secondary source, partial reference, in
     'e-secondary-partial': 'e-secondary', # Secondary source, partial reference, end
     'o': 'o', # out of a reference

The taxonomy for specific annotations. This is a working taxonomy, which is provided with a consolidated version as well. The main challenge is to track the necessary components of references to both primary and secondary sources. Read as: `Tag (as in the dataset): ConsolidatedTag (as used in the paper's results: some tags are merged)`. It is helpful to read this taxonomy with the report on the number of annotations per tag, so as to distinguish between often used and barely used tags. Note that several tags indeed need consolidation as they are under represented in the dataset. Their presence relates to the great variety of materials cited by historians: 
    
    'abbreviatedtitle': 'title', # Title
    'abbreviation': 'abbreviation', # Abbreviation such as Ivi, Ibid, Cit, Cf, etc.
    'appendix': 'ref', # Appendix
    'archivalfond': 'archivalreference', # Archival record group
    'archivalreference': 'archivalreference', # Archival reference
    'archivalseries': 'archivalreference', # Archival series or sub series (document collections)
    'archivalunit': 'archivalreference', # Archival unit (box, register)
    'archive': 'archive_lib', # Archive
    'attachment': 'attachment', # Attachment
    'author': 'author', # Author
    'box': 'box', # Box
    'cartulation': 'cartulation', # Cartulation such as c. 12.
    'cedola': 'ref', # Cedola (another form of reference)
    'century': 'date', # Century for a date, such as XIX century.
    'chapter': 'ref', # Chapter of a book
    'citation': 'ref', # Citation
    'codex': 'archivalreference', # Codex
    'column': 'column', # Column
    'conjunction': 'conjunction', # Conjunction such as in. 
    'curator': 'author', # Curator
    'date': 'date', # Date
    'editor': 'author', #Editor
    'fascicolo': 'folder', # Dossier
    'filza': 'filza', # Gathering
    'folder': 'folder', # Folder
    'foliation': 'foliation', # Foliation such as f. 12.
    'fond': 'archivalreference', # # Archival record group.
    'library': 'archive_lib', # Library
    'mazzo': 'ref', # Group of documents
    'notary': 'archivalreference', # Notary (name of a person)
    'note': 'numbered_ref', # Note
    'numbering': 'numbered_ref', # Numbering such as n. 12.
    'other': '', # Generic placeholder
    'pagination': 'pagination', # Pagination such as p. 12.
    'parchment': 'ref', # Parchment 
    'period': 'date', # Period such as 1950-1995.
    'protocollo': 'ref', # Registration of a document
    'parte': 'ref', # Law
    'publicationnumber': 'publicationnumber-year', # Issue and volume number such as 12(3).
    'publicationnumber-year': 'publicationnumber-year', # Issue and volume number, with year such as 12(3), 1990.
    'publicationplace': 'publicationplace', # Place of publication
    'publicationspecifications': 'publicationspecifications', # Other specifications linked with a publication
    'publicationyear': 'year', # Publication year
    'publisher': 'publisher', # Publisher
    'registry': 'registry', # Register
    'responsible': 'author', # Responsible (similar to Curator)
    'series': 'series', # Archival document series
    'table': 'ref', # Table
    'title': 'title', # Title
    'tomo': 'tomo', # Volume
    'topicdate': 'publicationplace', # Place of publication
    'voce': 'ref', # Entry e.g. in a dictionary.
    'volume': 'volume', # Volume
    'website': 'ref', # Website
    'year': 'year', # Year
    '': '' # no tag!
    
## Running the notebook

Assuming that Python is already installed (tested with version 3.5.2), the following depencies need to be installed as well (it will take a moment):

    scipy, sklearn, sklearn_crfsuite, numpy, seaborn, jupyter, multiprocessing

Then launch the notebook server with

    jupyter notebook

A new browser/tab will open pointing at Jupyter's starting page. You can find there the code used to develop the models in the repository, whose results are discussed in the paper.

## Linked Books Team at EPFL, DHLAB
Giovanni Colavizza, Matteo Romanello, Martina Babetto, Silvia Ferronato.

## Acknowledgements
This work would not have been possible without the help of several Italian institutions of culture. 
In alphabetical order we thank: the Ca’Foscari University Library System and the Ca’Foscari University Humanities Library (BAUM), the Central Institute for the Union Catalogue of Italian Libraries and Bibliographic Information (ICCU), the European Library of Information and Culture (BEIC), the Istituto Veneto di Scienze Lettere ed Arti, the Marciana Library, the State Archive of Venice.

The project is supported by the Swiss National Fund, with grants 205121_159961 and P1ELP2_168489.

## Please cite as

Giovanni Colavizza and Matteo Romanello. (2017). "Annotated References in the Historiography on Venice: XIX-XXI centuries". Submitted to the Journal of Open Humanities Data.

    @misc{colavizza_parsing_2017,
      author       = {Giovanni Colavizza and Matteo Romanello},
      title        = {{Annotated References in the Historiography on Venice: XIX-XXI centuries}},
      journal      = {{Journal of Open Humanities Data}},
      volume       = {TODO},
      number       = {TODO},
      pages        = {TODO},
      year         = 2017,
      doi          = {TODO},
      url          = {TODO}
    }