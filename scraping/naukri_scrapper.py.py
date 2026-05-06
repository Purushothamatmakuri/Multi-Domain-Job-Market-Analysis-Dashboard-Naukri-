from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import random
import os
# -----------------------------
# STEP 1: ROLE GROUPS
# -----------------------------
role_groups = {
    "Data Analytics": [
        "data analyst",
        "business analyst",
        "mis executive",
        "research analyst",
        "junior data analyst"
    ],
    
    "Data Science": [
        "data scientist",
        "machine learning engineer",
        "ai engineer",
        "data science intern",
        "data science engineer"
    ],
    
    "Data Engineering": [
        "data engineer",
        "sql developer",
        "database administrator",
        "data warehousing",
        "dba"
    ],
    
    "Software Development": [
        "software developer",
        "full stack developer",
        "java developer",
        "mern developer",
        "react developer",
        "python full stack developer",
        ".net developer",
        "associate software engineer"
    ],
    
    "Cloud & DevOps": [
        "devops engineer",
        "cloud engineer",
        "azure developer"
    ],
    
    "Digital Marketing": [
        "digital marketing executive",
        "seo analyst"
    ]
}

# -----------------------------
# STEP 2: SCRAPING
# -----------------------------
all_jobs = []


for domain, roles in role_groups.items():
    print(f"\n===== Domain: {domain} =====")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    for role in roles:
        print(f"\nRole: {role}")

        for page in range(1, 5):  # 🔥 4 pages

            try:
                encoded_role = role.replace(" ", "+")
                url = f"https://www.naukri.com/jobs?k={encoded_role}&pageNo={page}"

                print("Opening:", url)

                driver.get(url)
                time.sleep(5)

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                jobs = driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")

                print(f"{role} | Page {page} -> Jobs: {len(jobs)}")

                for job in jobs:

                    try:
                        title = job.find_element(By.CLASS_NAME, "title").text
                    except:
                        title = None

                    try:
                        company = job.find_element(By.CLASS_NAME, "comp-name").text
                    except:
                        company = None

                    try:
                        exp = job.find_element(By.CLASS_NAME, "exp-wrap").text
                    except:
                        exp = None

                    try:
                        loc = job.find_element(By.CLASS_NAME, "loc-wrap").text
                    except:
                        loc = None

                    try:
                        skills_elements = job.find_elements(By.CSS_SELECTOR, "ul.tags-gt li")
                        skills = [s.text for s in skills_elements if s.text]
                        skills = ", ".join(skills)
                    except:
                        skills = None

                    # ✅ POSTED DATE
                    try:
                        posted = job.find_element(By.CLASS_NAME, "job-post-day").text
                    except:
                        posted = None

                    all_jobs.append({
                        "Domain": domain,
                        "Role_Search": role,
                        "Title": title,
                        "Company": company,
                        "Experience": exp,
                        "Location": loc,
                        "Skills": skills,
                        "Posted": posted
                    })

                # ✅ Random delay (anti-block)
                time.sleep(random.randint(4, 7))

            except Exception as e:
                print("Error:", e)
                continue

    driver.quit()

# -----------------------------
# STEP 3: DATAFRAME
# -----------------------------
df = pd.DataFrame(all_jobs)
df.drop_duplicates(inplace=True)

# -----------------------------
# STEP 4: PREVIEW DATA
# -----------------------------
print("\n==============================")
print("FINAL DATA SHAPE:", df.shape)
print("==============================\n")

print(df.head(10))

# -----------------------------
# STEP 5: SAVE FILE
# -----------------------------
file_path = os.path.join(os.getcwd(), "jobs_with_posted_date.csv")

df.to_csv(file_path, index=False, encoding='utf-8-sig')

print("\n✅ Data saved successfully!")
print("📁 File location:", file_path)