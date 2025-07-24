from google_play_scraper import reviews, app, search
keyword = ['cricket', 'top cricket games', 'best cricket games'] #to get more then 30 n_hits
all_apps = []

# Get apps from Google Play
for keys in keyword:
    app_names = search(keys, country='us', lang='en')
    all_apps.extend(app_names)#using extend because append will do each character

# Write app title and appId to file
with open("new.txt", "w") as f:
    for app_info in all_apps:
        f.write(f"{app_info['title']} : {app_info['appId']}\n")

# Read the file and extract only the appId (part after ':')
app_ids= []
app_title=[]

with open("new.txt", "r") as f:
    contents = f.read()
    lines = contents.strip().split('\n')

    for line in lines:
        if ":" in line:
            idx = line.rfind(":")  # find the LAST colon
            title = line[:idx].strip() # deletes all the spaces
            app_id = line[idx + 1:].strip()

            app_title.append(title)
            app_ids.append(app_id)


# Get reviews of apps from Google Play
all_reviews = []


for app_id in app_ids:
    result,_= reviews(app_id, country='us', lang='en', count=100)  # get reviews
    all_reviews.extend(result) 
#print(app_title) Just to check wether the app names are being fetched name in the 38 is individual name 
with open("reviews.txt", "w") as f:
    for name in app_title:
        f.write(f"--------------------------------------- {name} ---------------------------------------\n")
        for review in all_reviews:
            for k, v in review.items():  
                if k == 'reviewId' or k == 'userImage':
                    pass
                else:
                    f.write(f"{k}:{v}\n") 


# Get details of apps from Google Play
app_details = []

for app_id in app_ids:
    result = app(app_id, country='us', lang='en')  # get details
    app_details.append(result)   # append dict, not extend

with open("details.txt", "w") as f:
    for name, details in zip(app_title, app_details):
        f.write(f"--------------------------------------- {name} ---------------------------------------\n")
        for k, v in details.items():  # details is a dict
            f.write(f"{k} : {v}\n")  
