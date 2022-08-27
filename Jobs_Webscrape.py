import time

from bs4 import BeautifulSoup
import requests

print("enter your job preference based on your preferred skill..")
unfamiliar_skills = input(">>")
print(f"filtering {unfamiliar_skills} skills jobs...")


def find_jobs():
    html_text = requests.get("https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=java&txtLocation=").text
    soup = BeautifulSoup(html_text, "lxml")
    jobs = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")

    with open(f"posts_Jobs_Webscrape\\jobs.txt", "w") as f:
        for index, job in enumerate(jobs):
            posted_date = job.find("span", class_="sim-posted").text.strip()
            if "few" in posted_date:
                title = job.a.text.strip()      # job title
                experience = job.ul.li.contents[-1]     # job experience
                skills = job.find("span", class_="srp-skills").text.strip()     # job skill requirements
                link = job.header.h2.a["href"]
                if unfamiliar_skills not in skills:
                        f.write(f"title: {title}\n")
                        f.write(f"experience: {experience}\n")
                        f.write(f"skills: {skills}\n")
                        f.write(f"posted: {posted_date}\n")
                        f.write(f"link: {link}\n\n\n")
    print(f"job.txt created...")


if __name__ == "__main__":
    while True:
        find_jobs()
        wait = 10
        print(f"waiting {wait} minutes...")
        time.sleep(wait * 60)