from flask import jsonify,Blueprint,render_template, redirect, url_for,Flask,request,jsonify
from flask_login import login_required
from JobtransparencyNLP import db
from JobtransparencyNLP.models import ApiStats, nlprecords
import nltk
import secrets
import JobtransparencyNLP.NLTKProcessor as nlpstuff
import os
from datetime import datetime, timedelta

def findAllBetweenDates(curDate, pastDate):
    return nlprecords.query.filter(
        nlprecords.created_at >= pastDate,
        nlprecords.created_at < curDate).all()

apistats_blueprint = Blueprint('apistats',__name__, template_folder='templates/apistats')

@apistats_blueprint.route("/GetStats")
def stats():
    statsQuery = ApiStats.query.all()
    stats = []
    for stat in statsQuery:
        stats.append(stat.as_dict())
    return jsonify(stats)

@apistats_blueprint.route("/GetCountsLast10Days")
def nlpstats():
    countsLast10Days = []
    for dayMinus in range(7):
        nlp = findAllBetweenDates(datetime.today(),(datetime.today()-timedelta(days=dayMinus+1)))
        title = "Last " + str(dayMinus + 1)
        countsLast10Days.append({"title":title,"count":len(nlp)})

    return jsonify(countsLast10Days)


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
        if authKey == os.environ['secrets']:
            final = nlpstuff.extractKeyPhrasesFromText(request.json["textIn"])
            nlprecords = nlprecords(request.json["textIn"],final)
            db.session.add(nlprecords)
            db.session.commit()
            return jsonify({"rank_list":final})
        else:
            return 'Processing Error Occured',500
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
    # try:
    #     authKey = request.json["authKey"]
    #     if True:
    #         final = nlpstuff.generate_summary(request.json["textIn"])
    #         nlprecords = nlprecords(request.json["textIn"],final)
    #         db.session.add(nlprecords)
    #         db.session.commit()
    #         return jsonify({"SummaryText":final})
    #     else:
    #         return 'Processing Error Occured',500
    # except:
    #     return 'Processing Error Occured',500
