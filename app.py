from JobtransparencyNLP import app
from flask import render_template
from JobtransparencyNLP import db
from JobtransparencyNLP.models import ApiStats, nlprecords
# flask db upgrade
@app.route('/')
def index():
    stats_keyphrases = ApiStats.query.filter_by(name='extract_keyphrases_from_text').first()
    stats_summary = ApiStats.query.filter_by(name='extract_summary_from_text').first()
    values = []
    for x in range(1,8):
        result = db.session.execute("SELECT count(*) as \"ProcessedCount\"" + 
                                    "FROM public.nlprecords where " +
                                    "created_at < now()::date and " +
                                    f"created_at > now()::date - INTERVAL '{x} DAYS'")
        for rr in result:
            temp = []
            temp.append(str(x))
            temp.append(str(rr[0]))
            values.append(temp)

    return render_template('home.html',homepage={
        "history":values,
        "stats_keyphrases":stats_keyphrases,
        "stats_summary":stats_summary
    })

if __name__ == '__main__':
    app.run()
