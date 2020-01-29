import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"
JOB_URL = "https://www.indeed.com/viewjob"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, 'html.parser')
  # print(soup.prettify())

  links = soup.find("div", {"class":"pagination"}).find_all("a")

  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))
  max_page = pages[-1]

  return max_page


def extract_job(html):
  # title
  title = html.find("div", {"class":"title"}).find("a")["title"]
  # company
  company_span = html.find("span", {"class":"company"})
  company = ""
  if company_span is not None:
    if company_span.string is None:
      company = company_span.find("a").string
    else:
      company = company_span.string
  company =  company.strip()
  # location
  location = html.find("div", {"class":"recJobLoc"})["data-rc-loc"]
  # job id
  job_id = html["data-jk"]

  return {
    'title': title,
    'company': company,
    "location": location,
    "link" : f"{JOB_URL}?jk={job_id}"
  }

def extract_jobs(last_pages):
  jobs = []
  for page in range(last_pages):
    print(f"Scrapping Indeed page:{page}")
    result = requests.get(f"{URL}&start={page * LIMIT}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page();
  jobs = extract_jobs(last_page)
  return jobs