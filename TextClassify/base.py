
from flask import Flask,request,jsonify

import nltk
import secrets
import NLTKProcessor
import os
app = Flask(__name__)

@app.route("/HealthCheck")
def hello():
    return "I am here to Classify"

@app.route("/extract_keyphrases_from_text",methods=["POST"])
def extract_keyphrases_from_text():
    try:
        authKey = request.json["authKey"]
        if authKey == os.environ['secrets']:
            final = NLTKProcessor.extractKeyPhrasesFromText(request.json["textIn"])
            return jsonify({"rank_list":final})
        else:
            return 'Processing Error Occured',500
    except:
        return 'Processing Error Occured',500

@app.route("/extract_summary_from_text",methods=["POST"])
def extract_summary_from_text():
    try:
        authKey = request.json["authKey"]
        if authKey == os.environ['secrets']:
            final = NLTKProcessor.generate_summary(request.json["textIn"])
            return jsonify({"SummaryText":final})
        else:
            return 'Processing Error Occured',500
    except:
        return 'Processing Error Occured',500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port= 8080)
