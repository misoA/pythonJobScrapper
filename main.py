from flask import Flask, render_template, request, redirect, send_file
from so import get_jobs as get_so_jobs
from rmo import get_jobs as get_rmo_jobs
from wwr import get_jobs as get_wwr_jobs
from save import save_to_file

app = Flask("SuperScrapper")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_so_jobs(word)
            jobs.extend(get_wwr_jobs(word))
            jobs.extend(get_rmo_jobs(word))
            db[word] = jobs
        return render_template(
            "report.html", searchingBy=word, resultsNumber=len(jobs), jobs=jobs
        )
    else:
        return redirect("/")


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")
    except Exception:
        return redirect("/")


app.run()
