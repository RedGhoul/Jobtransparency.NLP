from flask import jsonify,Blueprint,render_template, redirect, url_for,Flask,request,jsonify
from flask_login import login_required
from JobtransparencyNLP import db
from JobtransparencyNLP.models import ApiStats, nlprecords
import nltk
from config import SECRET_KEY,SQLALCHEMY_DATABASE_URI,AUTH_TOKEN
import JobtransparencyNLP.NLTKProcessor as nlpstuff
import os

apistats_blueprint = Blueprint('apistats',__name__, template_folder='templates/apistats')


@apistats_blueprint.route("/HealthCheck")
def hello():
    return "I am here to Classify"

@apistats_blueprint.route("/extract_keyphrases_from_text",methods=["POST"])
def extract_keyphrases_from_text():
    stats = ApiStats.query.filter_by(name='extract_keyphrases_from_text').first()
    
    if stats is not None:
        stats.addHit()
    else:
        newstats = ApiStats('extract_keyphrases_from_text',1)
        db.session.add(newstats)
        db.session.commit()

    try:
        authKey = request.json["authKey"]
        print("authKey  " + authKey)
        print("AUTH_TOKEN  " + AUTH_TOKEN)
        if authKey == AUTH_TOKEN: #os.environ["AUTH_TOKEN"]:
            final = nlpstuff.extract_key_phrases_from_text(request.json["textIn"])
            print("final")
            print(final)
            nlprecords = nlprecords(request.json["textIn"],final)
            db.session.add(nlprecords)
            db.session.commit()
            return jsonify({"rank_list":final})
        else:
            return 'Processing Error Occured AUTH_TOKEN',500
    except:
        return 'Processing Error Occured',500

@apistats_blueprint.route("/extract_summary_from_text",methods=["POST"])
def extract_summary_from_text():
    stats = ApiStats.query.filter_by(name='extract_summary_from_text').first()
    
    if stats is not None:
        stats.addHit()
    else:
        newstats = ApiStats('extract_summary_from_text',1)
        db.session.add(newstats)
        db.session.commit()

    final = nlpstuff.generate_summary(request.json["textIn"])
    nlpr = nlprecords(request.json["textIn"],final)
    db.session.add(nlpr)
    db.session.commit()
    return jsonify({"SummaryText":final})
