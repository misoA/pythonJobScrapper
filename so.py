import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?sort=i&r=true"
JOB_URL = "https://stackoverflow.com/jobs"


def get_last_page(word):
    result = requests.get(f"{URL}&q={word}")
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find_all("a", {"class": "s-pagination--item"})
    if len(pages) == 0:
        return 0
    else:
        return int(pages[-2].find("span").get_text(strip=True))


def extract_job(html):
    title = html.find("a", {"class": "s-link"})["title"]
    company_row = html.find("h3").find_all("span", recursive=False)
    company = company_row[0].get_text(strip=True)
    location = company_row[1].get_text(strip=True)
    job_id = html["data-jobid"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"{JOB_URL}/{job_id}",
    }


def extract_jobs(last_page):
    print(f"Start scarpping {last_page} pages")
    jobs = []
    for page in range(1, last_page + 1):
        print(f"Scrapping SO page:{page}")
        result = requests.get(f"{URL}&=pg={page}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    last_page = get_last_page(word)
    jobs = []
    if last_page == 0:
        print("there is no job!, plz search another word!!")
    else:
        jobs = extract_jobs(last_page)
    return jobs
