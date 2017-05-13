# LinkedBooksReferenceParsing: Annotations Dataset and CRF Parsing

# TODO
refactor all code
report results of current models (included) in the paper
prepare documentation and final release (describe data in detail)
put the dataset in zenodo (annotations)

TODO Zenodo
[![DOI](https://zenodo.org/badge/79789632.svg)](https://zenodo.org/badge/latestdoi/79789632)

A dataset of annotated references (in both reference lists and footnotes) from journal issues and monographs on the history of Venice, created in the context of the [LinkedBooks project](http://dhlab.epfl.ch/page-127959-en.html). 

Along the dataset of annotations, a framework to train your own parsers is provided, based on Conditional Random Fields. Feel free to use it to build your own parser, and if you improve on our results, please let us know!

## Contents

* `LICENCE` MIT.
* `README.md` this file.
* `dataset/`
    * [annotated_dataset](dataset/annotated_dataset.json.zip) Note that the dataset of annotations in json format can be downloaded from Zenodo at: . See there for a detailed description of the dataset.
    * [annotated_dataset](dataset/report.p) A set of statistics on the annotated dataset
* `M1.ipynb` a Python notebook to train a CRF parsing model using specific reference tags (e.g. author, title, publication year). You can use the annotated dataset in json format as input here.
* `M2.ipynb` a Python notebook to train a CRF parsing model using generic begin/end reference tags (e.g. begin-secondary, in-secondary, end-secondary for a reference to a secondary source).
* `models/`
    * [modelM1](models/modelM1_ALL_L.pkl) trained model 1, details in the paper.
    * [modelM2](models/modelM1_ALL_L.pkl) trained model 2, details in the paper.
* `code/`
    * [support_functions](code/support_functions.py) trained model 1, details in the paper.
    * [feature_extraction_words](models/modelM1_ALL_L.pkl) trained model 2, details in the paper.
    * [support_functions](code/support_functions.py) trained model 1, details in the paper.

## Running the notebook

Assuming that Python is already installed (tested with version 3.5.0), the following depencies need to be installed as well (it will take a moment):

    scipy, numpy, seaborn, pandas, jupyter, igraph
    Vincent Traag's Louvain implementation: https://github.com/vtraag/louvain-igraph

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

Giovanni Colavizza, Matteo Romanello, Martina Babetto, Silvia Ferronato. (2017). dhlab-epfl/LinkedBooksReferenceParsing: LinkedBooksReferenceParsing (version 1.0) [Data set]. Zenodo. TBD

    @misc{colavizza_parsing_2017,
      author       = {Giovanni Colavizza, Matteo Romanello, Martina Babetto and Silvia Ferronato},
      title        = {{dhlab-epfl/LinkedBooksReferenceParsing: 
                       LinkedBooksReferenceParsing (version 1.0)}},
      month        = jun,
      year         = 2017,
      doi          = {TODO},
      url          = {TODO}
    }
