from google_play_scraper import reviews, app, search

keyword = ['cricket', 'top cricket games', 'best cricket games'] #to get more then 30 n_hits
all_apps = []

# Get apps from Google Play
for keys in keyword:
    app_names = search(keys, country='us', lang='en')
    all_apps.extend(app_names)#using extend because append will do each character

# Write app title and appId to file
with open("new.txt", "w") as f:
    for app in all_apps:
        f.write(f"{app['title']} : {app['appId']}\n")

# Read the file and extract only the appId (part after ':')
app_ids= []

with open("new.txt", "r") as f:
    contents=f.read()
    new=contents.split('\n')
    for i in new:
        for j in range(len(i)):
            if i[j] == ":":
                app_ids.append(i[j+2:])


# Get reviews of apps from Google Play
all_reviews = []

with open("reviews.txt", "w", encoding="utf-8") as f:
    for app_id in app_ids:
        app_info = app(app_id, lang='en', country='us')  # get app info
        app_name = app_info['title']                     # extract app title
        f.write(f"\n=== Reviews for: {app_name} ===\n\n")  # write app name as header

        result, _ = reviews(app_id, country='us', lang='en', count=100)  # get reviews
        all_reviews.extend(result)

        for review in result:
            for k, v in review.items():
                if k == 'reviewId' or k == 'userImage':
                    pass
                else:
                    f.write(f"{k}:{v}\n")
            f.write("\n")