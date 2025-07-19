from google_play_scraper import reviews, app, search
keyword = ['cricket','top cricket games','best cricket games']
all_apps=[]
for keys in keyword:
    app_names = search (keys, country= 'us' , lang= 'en')
    all_apps.extend(app_names )


with open("new.txt", "w") as f:
    for app in  all_apps:
        f.write(f"{app['title']} : {app['appId']}\n")