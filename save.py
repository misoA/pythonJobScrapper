import csv


def save_to_file(jobs):
    file = open("jobs.csv", mode="w", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "loaction", "link"])
    for job in jobs:
        writer.writerow(job.values())
    print(file)