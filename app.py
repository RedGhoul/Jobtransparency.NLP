from JobtransparencyNLP import app
from flask import render_template
from JobtransparencyNLP import db
from JobtransparencyNLP.models import ApiStats, nlprecords
# flask db upgrade
@app.route('/')
def index():
    stats_keyphrases = ApiStats.query.filter_by(name='extract_keyphrases_from_text').first()
    stats_summary = ApiStats.query.filter_by(name='extract_summary_from_text').first()

    return render_template('home.html',homepage={
        "stats_keyphrases":stats_keyphrases,
        "stats_summary":stats_summary
    })

if __name__ == '__main__':
    app.run()
