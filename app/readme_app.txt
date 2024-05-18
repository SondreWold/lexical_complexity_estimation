#----------------------#
# GENERAL INFORMATION  #
#----------------------#

This folder contains what is needed to run a simple, interactive Flask app.

In addition to what is in this folder, you need to download model 76 from the european language model repository.

(Or another model of your choice)

The folder "templates" contains the single html file needed for the home page. The html for the other page is created in the function itself.

reduced.json is the same reduced file that is produced by lexical_analysis.py to produce the outputs reported there. It is significantly smaller in size,
but contains the necessary information to check complexities and compare. More specifically, the original but very large lemma_list_final.json file
which is produced in the pipeline, and which is used as input (along with an embedding model) to produce scores in lexical_analysis.py, contains
lemmas with POS, along with a list of complexity scores from all the books the word has appeared in. reduced.py on the other hand only contains
the lemmas and a complexity score. The score is not calculated for words that do not occur in enough (20) texts, and words that are very long (obvious errors) are removed.

Some apparent shortcomings to be aware of:

-The lemmatizer has a large impact on the results. The lemmatizer for Norwegian is relatively good, but still contains many obvious errors.
-Some of the texts used contain OCR errors. While we attempted to reduced this by avoiding later texts, there are still some errors.
-As the code is written now, it only attempts to find words with the same POS as the source word. This could easily be accounted for by using the POS information provided by the embedding model.


#----------#
# RUNNING  #
# ---------#

 To run the app, write:

flask --app flask_app.py run

This will provide an address (locally) where you can test the tool.

