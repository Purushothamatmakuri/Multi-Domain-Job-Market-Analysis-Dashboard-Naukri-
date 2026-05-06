import pandas as pd
import re
df = pd.read_csv("jobs_with_posted_date.csv")
print(df.isnull().sum())
#Handle Missing Values
df.fillna({
    'Company': "Unknown",
    'Experience': "Not Specified",
    'Location': "Not Specified",
    'Skills': "Not Mentioned",
    'Posted': "Unknown"
}, inplace=True)
#Remove Duplicates
df.drop_duplicates(inplace=True)
#Clean Experience Column
def clean_experience(exp):
    try:
        nums = re.findall(r'\d+', exp)
        if len(nums) == 2:
            return (int(nums[0]) + int(nums[1])) / 2
        elif len(nums) == 1:
            return int(nums[0])
    except:
        return None
df['Experience_Num'] = df['Experience'].apply(clean_experience)

#Clean Posted Date
def convert_posted(x):
    x = str(x).lower()
    
    if "today" in x or "just" in x:
        return 0
    elif "hour" in x:
        return 0
    elif "day" in x:
        return int(re.findall(r'\d+', x)[0])
    elif "week" in x:
        nums = re.findall(r'\d+', x)
        return int(nums[0]) * 7 if nums else None
    elif "30+" in x:
        return 30
    else:
        return None

df['Posted_Days'] = df['Posted'].apply(convert_posted)

#Extract City from Location
import re

def clean_city(loc):
    loc = str(loc).lower()

    # Remove unwanted words
    loc = loc.replace("hybrid -", "").replace("remote", "").strip()

    # Take first part before comma or slash
    loc = re.split(',|/', loc)[0]

    # Standardize major cities
    if "bangalore" in loc or "bengaluru" in loc:
        return "Bangalore"
    elif "hyderabad" in loc:
        return "Hyderabad"
    elif "mumbai" in loc:
        return "Mumbai"
    elif "chennai" in loc:
        return "Chennai"
    elif "delhi" in loc or "ncr" in loc:
        return "Delhi NCR"
    elif "pune" in loc:
        return "Pune"
    elif "kolkata" in loc:
        return "Kolkata"
    elif "ahmedabad" in loc:
        return "Ahmedabad"
    else:
        return "Other"

df['City'] = df['Location'].apply(clean_city)

#Clean Skills Column 
df['Skills_List'] = df['Skills'].apply(lambda x: [i.strip() for i in str(x).split(',')])

#Standardize Role Names
def clean_role(title):
    title = str(title).lower()

    if "data scientist" in title:
        return "Data Scientist"
    elif "data analyst" in title:
        return "Data Analyst"
    elif "data engineer" in title:
        return "Data Engineer"
    elif "software" in title:
        return "Software Engineer"
    elif "devops" in title:
        return "DevOps Engineer"
    else:
        return "Other"

df['Role_Cleaned'] = df['Title'].apply(clean_role)

print(df.head())
print(df.shape)


df.to_csv("cleaned_jobs_data.csv", index=False)
print("Cleaned dataset saved!")