from flask import Flask,render_template, request
import json
import gensim
import pandas as pd
from os import path
from utils import load_embedding
from collections import defaultdict



with open("reduced.json","r",encoding="utf-8") as indata:
        lemma_list = json.load(indata)
        
    # Model can be downloaded from http://vectors.nlpl.eu/repository/
embeddings_file = path.join("./../models/76/", "model.bin")
model = load_embedding(embeddings_file)

def find_alternatives(word, model):
    og_word = word
    a = word.split("_")
    word, pos = a[0], a[-1]
    l = {word: {'Synonymity': 1, 'Complexity': get_complexity_score(og_word)}}
    # This will produce an error if the word is not in the model
    for i in model.most_similar(positive=[word], topn=10):
        comp_score = get_complexity_score(i[0] + f'_{pos}')
        if comp_score == -1:
            continue
        l[i[0]] = {'Synonymity': i[1], 'Complexity': comp_score}
    try:
        #a = pd.DataFrame.from_dict(l).T.sort_values(by=['Complexity'], ascending=True))
        print(pd.DataFrame.from_dict(l).T.sort_values(by=['Complexity'], ascending=True))
        #a = a.to_dict()
        return l
        #return a
    except:
        print('Not able to produce alternatives!')
        return {}


def get_complexity_score(word):
    return lemma_list.get(word,-1)

def colormap(complexity):
    if complexity < 20:
        return '<span style="color: #297508"> {} </span>'
    elif complexity < 30:
        return '<span style="color:#7fb911"> {} </span>'
    elif complexity < 40:
        return '<span style="color: #ce651f"> {} </span>'
    elif complexity < 50:
        return '<span style="color: #ff0000"> {} </span>'
    else:
        return '<span style="color: #000000"> {} </span>'

def getproportions(newtext):
    props = defaultdict(set)
    #55.8 highest possible
    #9.4 lowest possible
    wordet = newtext.strip()
    print("entered",wordet)
    if "_" not in wordet:
        print("missing",wordet)
        return "ERROR, format not correct. Examples: hus_NOUN, spise_VERB"
    if wordet.split("_")[-1] not in ["NOUN","VERB","ADJ","ADV"]:
        print("wrongpos",wordet,wordet.split("_")[-1])
        return "ERROR,POS not recognized. Only VERB; NOUN ADJ AND ADV are supported. Examples: hus_NOUN, spise_VERB"
    #print("modelhasit:",newtext in model.wv.key_to_index)
    # Creating HTML
    start = '<!DOCTYPE html>\n<html>\n<head>\n<title>Page Title</title>\n</head>\n<body>'
    tekst = start + '<p style="font-size:14px; color:#538b01; font-weight:bold;">'
    comp = get_complexity_score(wordet)
    
    similars = find_alternatives(wordet, model=model)
    tekst += "<p>You searched for the word {}</p>".format(wordet)
    
    if len(similars) == 1:
        tekst += "<p>Unfortunately no suggestions were found for this word.</p>"
    else:
        # Going through all results from the model and giving them colors
        # based on their complexities
        tekst += "<h3> Results for your word.</h3>"
        tablestring = "<table>"
        tablestring += """<tr><th style="border-bottom: 2px solid black;">{}</th>""".format("Word")
        tablestring += """<th style="border-bottom: 2px solid black;">{}</th>""".format("Synonymity")
        tablestring += """<th style="border-bottom: 2px solid black;">{}</th></tr>""".format("Complexity")
        for word in similars:
            sim = str(round(similars[word]["Synonymity"],2))
            com = round(similars[word]["Complexity"],2)
            comp = str(com)
            farge = colormap(com)
            tablestring += "<tr>"
            tablestring += "<td>{}</td>".format(farge.format(word))
            tablestring += "<td>{}</td>".format(farge.format(sim))
            tablestring += "<td>{}</td>".format(farge.format(comp))
            tablestring += "</tr>"
        tablestring += "</table>"
    tekst += tablestring
    tekst += "</p>\n</body>\n</html>"
    return tekst

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/samaneh1',methods=["POST","GET"])
def samaneh1():
    return render_template("complexity.html")

@app.route('/samaneh2',methods=["POST","GET"])
def samaneh2():
    strengen = ""
    if request.method == "POST":
        ordet = request.form["fname"]
        strengen += ordet
        print(strengen)
    elif request.method == "GET":
        strengen += "ERROR"
    else:
        strengen += "ERROR"
    return getproportions(strengen)