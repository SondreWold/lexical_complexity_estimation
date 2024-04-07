<h2 align="center"><b>Estimating Lexical Complexity from Document-Level Distributions</h2><br></b>


<p align="center">
  <b>Sondre Wold<sup>*</sup>, Petter Mæhlum<sup>*</sup>, Oddbjørn Hove</b>
</p>

<p align="center">
  <i>
    <sup>*</sup>University of Oslo<br>
    Language Technology Group<br>
  </i>
  <br>
  <i> Helse Fonna </i>
</p>
<br>

Existing methods for complexity estimation are typically developed for entire documents. This limitation in scope makes them inapplicable for shorter pieces of text, such as health assessment tools. These typically consist of lists of independent sentences, all of which are too short for existing methods to apply. The choice of wording in these assessment tools is crucial, as both the cognitive capacity and the linguistic competency of the intended patient groups could vary substantially. As a first step towards creating better tools for supporting health practitioners, we develop a two-step approach for estimating lexical complexity that does not rely on any pre-annotated data. We implement our approach for the Norwegian language and verify its effectiveness using statistical testing and a qualitative evaluation of samples from real assessment tools. We also investigate the relationship between our complexity measure and certain features typically associated with complexity in the literature, such as word length, frequency, and the number of syllables.

<p align="center">
  <a href="https://arxiv.org/abs/2404.01196"><b>Paper</b></a><br>
</p>

_______

This repository contains the code for reproducing the results for our
upcoming paper at LREC-COLING 2024. 

# Online tool
TBA

# Collecting the raw data

Not all of the data used in the paper is publically available. Links to the
original sources can be found in the paper. Upon request, we can provide
the collections. Please see the paper for contact details.

# Processing

The `*_parser.py` scripts can be used to collect/process individual
documents from original sources. The output of these parsers are
`.json` files that includes cleaned text for each document identifier.
These files should then be given as inputs to `serializer.py` which
transforms the documents into lemmatized  sequences on the same format.

# Calculating the LIX score

Given a lemmatized document list, the `metrics.py` script calculates the
document-level LIZ score for each entry. The script can also calculate the
coleman-liau.

# Indexing

The `inverted_indexer.py` script takes as input the lemmatized documents
and creates an inverted index for each lemma. The `index_merger.py` scipt
takes as input these indexes and merges them into one combined lemma list
for all the sources. This is used to calculate all the lemma-level
statistics in the analysis.

# Analysis

`corpora_statistics.py` reproduces the results related to each individual
collection and their correlations. It also produces all of the plots used
in the paper.

`lexical_analysis.py` takes as input the combined inverted index, a
complete lemma list from all the sources, and reproduces the results and
figures related to calculating complexity scores for individual lemmas.

