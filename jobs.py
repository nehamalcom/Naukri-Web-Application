from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask import g
from . import db # module containing all the code and functions for db operations

# using the Blueprint as a regular Flask app
# first argument`
bp = Blueprint("jobs", "jobs", url_prefix="/jobs")

@bp.route("/")
def alljobs():
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT o.id, o.title, o.company_name, o.company_name, s.name FROM openings o, job_status s WHERE s.id=o.status ORDER BY s.name")
    jobs = cursor.fetchall()
    cursor.execute("SELECT crawled_on FROM crawl_status ORDER BY crawled_on DESC LIMIT 1")
    crawl_date = cursor.fetchone()[0]

    return render_template("jobs/jobslist.html", jobs=jobs, count=len(jobs), date=crawl_date)

@bp.route("/<jid>")
def jobDetail(jid):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT o.title, o.company_name, s.name, o.jd_text, o.crawled_on FROM openings o, job_status s WHERE o.id= %s AND s.id=o.status", (jid,))
    job = cursor.fetchone()
    if not job:
        return render_template("jobs/jobdetails.html"), 404
    title, company, status, info, crawled_on=job
    jid = int(jid)
    if jid == 1:
        prev=None
    else:
        prev = jid - 1
    nxt = jid + 1

    classes = {"crawled": "primary",
        "applied":"secondary",
        "ignored":"dark",
        "selected":"success",
        "rejected":"danger"}

    return render_template("jobs/jobsdetails.html",
        jid=jid,
        info=info,
        nxt=nxt,
        prev=prev,
        title=title,
        company=company,
        status=status,
        cls=classes[status],
        crawled_on=crawled_on)

@bp.route("/<jid>/edit", methods=["GET","POST",])
def edit_job(jid):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT o.title, o.company_name, s.name, o.jd_text, o.crawled_on FROM openings o, job_status s WHERE o.id=%s AND s.id=o,status", (jid,))
    job = cursor.fetchone()
    if not job:
        return render_template("jobs/jobdetails.html"), 404
    if request.method == "GET":
        title, company_name, status, jd, crawled_on = job
        cursor.execute("SELECT id, name FROM job_status")
        statuses = cursor.fetchall()
        return render_template("jobs/jobedit.html",
            jid=jid,
            info=jd,
            statuses=statuses,
            status=status,
            title=title,
            crawled_on=crawled_on)
    elif request.method == "POST":
        status = request.form.get("status")
        jd = request.form.get("jid")
        cursor.execute("UPDATE openings SET jd_text=%s, status=%s WHERE id=%s", (jd, status, jid))
        conn.commit()
        return redirect(url_for("jobs.jobdetail", jid=jid), 302)
