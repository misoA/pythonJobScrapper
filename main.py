from flask import Flask, render_template, request, redirect, send_file
from so import get_jobs
from save import save_to_file

app = Flask("SuperScrapper")

db = {}


@app.route("/")
def home():
    return render_template("potato.html")


@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
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
