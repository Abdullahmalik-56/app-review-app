from google_play_scraper import reviews, app, search, Sort

keyword = ['cricket', 'top cricket games', 'best cricket games']
# Get apps from Google Play
def get_app_title():
    all_apps = []
    for key in keyword:
        app_names = search(key, country='us', lang='en')
        all_apps.extend(app_names)
    return all_apps

# Write app titles and IDs to file
def app_name_title(apps):
    with open("new.txt", "w") as f:
        for app_info in apps:
            f.write(f"{app_info['title']} : {app_info['appId']}\n")

# Read the file and extract app IDs and titles
def extract_name_title():
    app_ids = []
    app_titles = []
    with open("new.txt", "r") as f:
        for line in f:
            if ":" in line:
                idx = line.rfind(":")
                title = line[:idx].strip()
                app_id = line[idx + 1:].strip()
                app_titles.append(title)
                app_ids.append(app_id)
    return app_ids, app_titles

# Get reviews of apps
def get_reviews(app_ids):
    all_reviews = []
    for app_id in app_ids:
        result, _ = reviews(app_id, country='us', lang='en', sort=Sort.NEWEST, count=100)
        all_reviews.extend(result)
    return all_reviews

# Write reviews to file
def review_file(app_titles, all_reviews):
    with open("reviews.txt", "w") as f:
        for name in app_titles:
            f.write(f"--------------------------------------- {name} ---------------------------------------\n")
        for review in all_reviews:
            for k, v in review.items():
                if k not in ['reviewId', 'userImage']:
                    f.write(f"{k}: {v}\n")

# Get details of apps
def get_app_details(app_ids):
    app_details = []
    for app_id in app_ids:
        result = app(app_id, country='us', lang='en')
        app_details.append(result)
    return app_details

# Write app details to file
def get_details_file(app_titles, app_details):
    with open("details.txt", "w") as f:
        for name, details in zip(app_titles, app_details):
            f.write(f"--------------------------------------- {name} ---------------------------------------\n")
            for k, v in details.items():
                f.write(f"{k} : {v}\n")
#Get reply percentile
def reply_rate(app_ids):
    reply= []
    reply_data=get_reviews(app_ids)
    for reply_info in reply_data:
        for k,v in reply_info.items():
            if k in ['replyContent' ,'repliedAt']:reply.append(v)
    return reply
                
                
    



# Main driver
if __name__ == "__main__":
    all_apps = get_app_title()
    app_name_title(all_apps)

    app_ids, app_titles = extract_name_title()
    all_reviews = get_reviews(app_ids)
    review_file(app_titles, all_reviews)

    app_details = get_app_details(app_ids)
    get_details_file(app_titles, app_details)

    print(reply_rate(app_ids))