#Fetches all of the plugins from the Wordpress plugin API,
#saves to Maria DB.

#To query plugins, use get_plugins with the params:
#name, description, install count, slug

import requests
import mariadb
from multiprocessing import Pool

def fetch_plugins(link):
    json = requests.get(link).json()
    for plugin in json["plugins"]:
        print(plugin["slug"])
    return json["plugins"]

def scrape_plugins(keyword):
    plugins = []
    link = f"https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request[search]={keyword}&request[per_page]=99&request[page]=replaceme"
    result = requests.get(link.replace("replaceme", "1")).json()
    jobs = []
    for i in range(1, int(result["info"]["pages"])):
        jobs.append(link.replace("replaceme", str(i)))
    with Pool(15) as pool:
        plugin_arrays = pool.map(fetch_plugins, jobs)
    for array in plugin_arrays:
        plugins.extend(array)
    return plugins

def get_db():
    return mariadb.connect(
        host="localhost",
        port=2206,
        user="root",
        password="root"
    )

def get_plugins(name: str = "", description: str = "", slug: str = "", install_count: int = 0):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("USE wordpress_plugins")
    query = "SELECT "
    keywords = []
    if not name and not description and not slug and not install_count:
        raise Exception("ERROR: Must supply a query to get_plugins!")
    if name:
        keywords.append(name)
        query += "name, "
    if description:
        keywords.append(description)
        query += "description, "
    if slug:
        keywords.append(slug)
    if install_count > 0:
        keywords.append(install_count)
    query += "install_count, "
    query += "slug, "
    query = f"{query[0:-2]} FROM plugins"
    cursor.execute(query)
    plugins = []
    for tup in cursor:
        final_string = ""
        for x in tup[0:-1]:
            final_string += x
        for keyword in keywords:
            if isinstance(keyword, int):
                if keyword >= int(tup[len(tup)-2]):
                    plugins.append(tup[len(tup)-1])
            if keyword in final_string:
                plugins.append(tup[len(tup)-1])
    return plugins

def dump_to_db():
     all_plugins = scrape_plugins("")
     db = get_db()
     cursor = db.cursor()
     cursor.execute("USE wordpress_plugins")
     for plugin in all_plugins:
         if plugin["active_installs"] > 1000:
             cursor.execute(f"""INSERT INTO plugins(
             name, slug, description, author, install_count
             ) VALUES (
                '{db.escape_string(str(plugin["name"]))}', 
                '{db.escape_string(str(plugin["slug"]))}', 
                '{db.escape_string(str(plugin["short_description"]))}', 
                '{db.escape_string(str(plugin["author_profile"]))}', 
                '{db.escape_string(str(plugin["active_installs"]))}'
            )""")
     db.commit()
     cursor.close()
     db.close()

# if __name__ == "__main__":
#     dump_to_db()