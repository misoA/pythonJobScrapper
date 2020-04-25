import requests
from bs4 import BeautifulSoup

URL = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93"
JOB_URL = "https://weworkremotely.com/"


def extract_job(html):
    company = html.find("span", {"class": "company"}).get_text(strip=True)
    title = html.find("span", {"class": "title"}).get_text(strip=True)
    region = html.find("span", {"class": "region"})
    if region:
        region = region.get_text(strip=True)
    else:
        ""
    link = html.find("a", recursive=False)["href"]
    return {
        "title": title,
        "company": company,
        "location": region,
        "link": f"{JOB_URL}/{link}",
    }


def get_jobs(word):
    result = requests.get(f"{URL}&term={word}")
    soup = BeautifulSoup(result.text, "html.parser")
    lis = soup.find_all("li", {"class": "feature"})
    print(f"Start weworkremotely scarpping {len(lis)} jobs")
    jobs = []
    if len(lis) > 0:
        for li in lis:
            jobs.append(extract_job(li))
    return jobs
