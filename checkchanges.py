import urllib.request
from urllib.parse import urlparse
from pathlib import Path
import requests
from bs4 import BeautifulSoup as bs4
import difflib

# import os


with open("./websitesToCheck.txt", "r") as f:
    websites = f.readlines()

changed = {}
# print(websites)
for w in websites:
    page = urllib.request.urlopen(w)
    page = requests.get(w)
    name = urlparse(w).netloc

    my_file = Path("./latest-content/"+ name + ".html")
    if my_file.is_file():
        # compare

        # open saved version of the page
        with open("./latest-content/"+ name + ".html", "r", encoding='utf-8') as f:
            saved_page = f.read()
        soup = bs4(page.content, 'html.parser')
        body = soup.find("body").text.strip()

        # compare the two versions of the page
        diff = difflib.unified_diff(saved_page.splitlines(), str(body).splitlines(), fromfile='saved_page', tofile='str(body)', lineterm='', n=0)
        lines = list(diff)[2:]
        added = [line[1:] for line in lines if line[0] == '+']
        removed = [line[1:] for line in lines if line[0] == '-']

        additions = ""

        # print('additions:')
        # for line in added:
        #     print(line)
        # print("------------")
        # print('additions, ignoring position')
        for line in added:
            if line not in removed:
                # print(line)
                additions += line + "\n"

        changed[w] = additions


        # replace html with newest version
        with open("./latest-content/"+ name + ".html", "w", encoding='utf-8') as f:
            f.write(body)
    else:
        print("not found")
        # print(page.read())
        soup = bs4(page.content, 'html.parser')
        body = soup.find("body").text.strip()
        with open("./latest-content/"+ name + ".html", "w", encoding='utf-8') as f:
            f.write(str(body))


# print("sending this to you in an email")
# print("example: this website " + websites[0] + " has changed. wow!")
# print("another line here!")
# print("")
# print(" that was a gap")
# for key, value in changed.items():
#     print(f"{key}: {value}")
#     print("   ")

with open("./emailcontent/email.txt", "w", encoding='utf-8') as f:
    f.write("this is the email now\n")
    for key, value in changed.items():
        f.write(f"{key}: {value}")
        f.write("   ")
# env_file = os.getenv('GITHUB_ENV')

# with open(env_file, "a") as myfile:
#     myfile.write("email=MY_VALUE")