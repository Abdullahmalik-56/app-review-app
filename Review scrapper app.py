from google_play_scraper import reviews, app, search, Sort
import os
import torch
import json
import requests
url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
token="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" 

keyword=['best cricket game','cricket game','cricket real game']
def user_menu():
    print("\nAvailable actions:")
    print(" - search   : Search and save apps")
    print(" - reviews  : Fetch and save reviews")
    print(" - details  : Fetch and save app details")
    print(" - summary  : Summarize reviews")
    print(" - all      : Perform all actions")
    print(" - quit     : Exit program")

    choice = input("\nEnter your action: ").strip().lower()
    return choice
def llm(prompt):
    parameters = {
      "max_new_tokens": 150,
      "temperature": 1.0,
      "top_k": 3,
      "top_p": 0.95,
         
      }
    
    headers = {
      'Authorization': f'Bearer {token}',
      'Content-Type': 'application/json'
  }
  
    payload = {
      "inputs": prompt,
      "parameters": parameters
  }
  
    response = requests.post(url, headers=headers, json=payload)
    response_text = response.json()

    return response_text
# Get apps from Google Play
def search_apps_by_keywords():
    all_apps = []
    for key in keyword:
        app_names = search(key, country='us', lang='en')
        all_apps.extend(app_names)
    return all_apps

# Write app titles and IDs to file
def save_app_list(apps):
    with open("new.txt", "w") as f:
        for app_info in apps:
            f.write(f"{app_info['title']} : {app_info['appId']}\n")
# Get reviews of apps
def fetch_reviews (app_ids,app_titles):
    all_reviews = {}

    for app_id, app_title in zip(app_ids, app_titles):
        print(f"Fetching reviews for {app_title}...")
        result, _ = reviews(app_id, country='us', lang='en', sort=Sort.NEWEST, count=100)
        contents = [review['content'] for review in result if 'content' in review]
        all_reviews[app_title] = contents
        with open("new.txt", "w") as f:
                f.write(f"{all_reviews}")

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
def summarize_reply_content(all_reviews):
    with open('summary.txt', 'w') as f:
            f.write("")
    for app_titles,reviews in all_reviews.items():
        review_text = "  ".join(reviews[:10])

        prompt = (
    "You are a helpful assistant. Your task is to summarize the following mobile app user reviews in a concise paragraph. "
    "Highlight the main strengths and weaknesses based on user feedback:"
    f"{review_text}"
)
        with open ('summary.txt','a')as f:
            summary_response = llm(prompt)
            f.write(f"--------------------------------------- {app_titles}----------------------------------\n")
            f.write(f"{summary_response}\n")

                
#Get reply percentile
#def rextract_reply_data(app_ids):
 ##
 #   reply_data=fetch_reviews(app_ids)
  #  for reply_info in reply_data:
   #     for k,v in reply_info.items():
    #        if k in ['content']:reply.append(v)
    
                
                
    



# Main driver
if __name__ == "__main__":
    all_apps = search_apps_by_keywords()
    app_ids, app_titles = zip(*[(app['appId'], app['title']) for app in all_apps])
    
    while True:
        action = user_menu()
        if action == 'search':
            save_app_list(all_apps)
        elif action == 'reviews':
            all_reviews = fetch_reviews(app_ids, app_titles)
            save_reviews(app_titles, all_reviews)
        elif action == 'details':
            app_details = fetch_app_details(app_ids)
            save_app_details(app_titles, app_details)
        elif action == 'summary':
            all_reviews = fetch_reviews(app_ids, app_titles)
            summarize_reply_content(all_reviews)
        elif action == 'all':
            save_app_list(all_apps)
            all_reviews = fetch_reviews(app_ids, app_titles)
            save_reviews(app_titles, all_reviews)
            app_details = fetch_app_details(app_ids)
            save_app_details(app_titles, app_details)
            summarize_reply_content(all_reviews)
        elif action == 'quit':
            print("Exiting program.")
            break
  
