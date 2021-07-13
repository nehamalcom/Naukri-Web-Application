import random
from flask import Flask, render_template

def create_app():
    app = Flask("jobs")
    app.config.from_mapping(
        DATABASE="naukri"
    )

    from . import jobs
    app.register_blueprint(jobs.bp)

    from . import db
    db.init_app(app)

    @app.route("/")
    def index():
        quotes = [["The best way to get started is to quit talking and begin doing.", "Walt Disney"],
                  ["The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.", "Winston Churchill"],
                  ["Don’t let yesterday take up too much of today.", "Will Rogers"]]
        quote, author = random.choice(quotes)
        conn = db.get_db()
        curs = conn.cursor()
        curs.execute("SELECT COUNT(*) FROM openings")
        count = curs.fetchone()[0]
        curs.execute("SELECT crawled_on FROM crawl_status ORDER BY  DESC LIMIT 1");
        crawl_date = curs.fetchone()[0]

        return render_template('index.html', quote=quote, author=author, count=count, date=crawl_date)
    from . import crawler
    crawler.init_app(app)

    return app
    
