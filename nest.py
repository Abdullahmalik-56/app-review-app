from google_play_scraper import reviews, app, search, Sort
import torch
from transformers import pipelines

keyword = ['cricket', 'top cricket games', 'best cricket games']
# Get apps from Google Play
def search_apps_by_keywords():
    all_apps = []
    for key in keyword:
        app_names = search(key, country='us', lang='en',n_hits=30)
        all_apps.extend(app_names)
    return all_apps

# Write app titles and IDs to file
def save_app_list(apps):
    with open("new.txt", "w") as f:
        for app_info in apps:
            f.write(f"{app_info['title']} : {app_info['appId']}\n")
# Get reviews of apps
def fetch_reviews (app_ids):
    all_reviews = []
    for app_id in app_ids:
        result, _ = reviews(app_id, country='us', lang='en', sort=Sort.NEWEST, count=100)
        all_reviews.extend(result)
    return all_reviews

# Write reviews to file
def save_reviews (app_titles, all_reviews):
    with open("reviews.txt", "w") as f:
        for name in app_titles:
            f.write(f"--------------------------------------- {name} ---------------------------------------\n")
        for review in all_reviews:
            for k, v in review.items():
                if k not in ['reviewId', 'userImage']:
                    f.write(f"{k}: {v}\n")

# Get details of apps
def fetch_app_details (app_ids):
    app_details = []
    for app_id in app_ids:
        result = app(app_id, country='us', lang='en')
        app_details.append(result)
    return app_details

# Write app details to file
def save_app_details (app_titles, app_details):
    with open("details.txt", "w") as f:
        for name, details in zip(app_titles, app_details):
            f.write(f"--------------------------------------- {name}----------------------------------\n")
            for k, v in details.items():
                f.write(f"{k} : {v}\n")
# Summarize reply content
def summarize_reply_content(app_titles):
    reply_data = fetch_reviews(app_ids) 

    names=[]
    rep=[]

    for app_name in app_titles:
        names.append(app_name)
    for reply_info in reply_data:
        for k,v in reply_info.items():
            if k in ['content']:
                rep.append(v)
    return dict(zip(names,rep))


    #pipe=pipelines.pipeline("summarization", model="Falconsai/text_summarization")
    #reply_summary = pipe(rep_content, max_length=100, min_length=30, do_sample=False)
    
                
#Get reply percentile
def rextract_reply_data(app_ids):
    reply= []
    reply_data=fetch_reviews(app_ids)
    for reply_info in reply_data:
        for k,v in reply_info.items():
            if k in ['content']:reply.append(v)
    
                
                
    



# Main driver
if __name__ == "__main__":
    all_apps = search_apps_by_keywords()
    save_app_list(all_apps)

    app_ids, app_titles = zip(*[(app['appId'], app['title']) for app in all_apps])
    
    all_reviews = fetch_reviews (app_ids)
    save_reviews (app_titles, all_reviews)

    app_details = fetch_app_details(app_ids)
    save_app_details (app_titles, app_details)
    print (rextract_reply_data(app_ids))

    for k,v in summarize_reply_content(app_titles).items():
        print(f"{k} : {v}")

    print("Data extraction completed successfully.")     