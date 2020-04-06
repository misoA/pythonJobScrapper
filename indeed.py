import math
import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?limit={LIMIT}"
JOB_URL = "https://www.indeed.com/viewjob"


def get_last_page(word):
    result = requests.get(f"{URL}&q={word}")
    soup = BeautifulSoup(result.text, "html.parser")

    job_count = soup.find("div", {"id": "searchCountPages"}).get_text(strip=True)
    job_count = int(job_count.split()[3].replace(",", ""))

    max_page = math.ceil(job_count / LIMIT) if job_count > LIMIT else 1
    return max_page


def extract_job(html):
    # title
    title = html.find("div", {"class": "title"}).find("a")["title"]
    # company
    company_span = html.find("span", {"class": "company"})
    company = ""
    if company_span is not None:
        if company_span.string is None:
            company = company_span.find("a").string
        else:
            company = company_span.string
    company = company.strip()
    # location
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    # job id
    job_id = html["data-jk"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"{JOB_URL}?jk={job_id}",
    }


def extract_jobs(last_page):
    print(f"Start scarpping {last_page} pages")
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed page:{page}")
        result = requests.get(f"{URL}&start={page * LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    last_page = get_last_page(word)
    jobs = extract_jobs(last_page)
    return jobs
