import urllib.request
import requests
from urllib.parse import urlparse

with open("./websitesToCheck.txt", "r") as f:
    websites = f.readlines()

changed = []

print(websites)
for w in websites:
    page = requests.get(w)
    # page = urllib.request.urlopen(w).text
    name = urlparse(w).netloc
    # print(page.read())
    with open("./latest-content/"+ name + ".html", "w", encoding="utf-8") as f:
        f.write(page.text)
