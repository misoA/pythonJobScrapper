import requests
from bs4 import BeautifulSoup

URL = "https://remoteok.io/"


def extract_job(html):
    link = html["data-url"]
    company = html.find("h3", {"itemprop": "name"}).get_text(strip=True)
    title = html.find("h2", {"itemprop": "title"}).get_text(strip=True)
    return {
        "title": title,
        "company": company,
        "location": "",
        "link": f"{URL}/{link}",
    }


def get_jobs(word):
    result = requests.get(f"{URL}remote-{word}-jobs")
    soup = BeautifulSoup(result.text, "html.parser")
    trs = soup.find_all("tr", {"class": "job"})
    jobs = []
    print(f"Start remoteok scarpping {len(trs)} jobs")
    if len(trs) > 0:
        for tr in trs:
            jobs.append(extract_job(tr))
    print(jobs)
    return jobs
