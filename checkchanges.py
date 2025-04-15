import urllib.request
from urllib.parse import urlparse
from pathlib import Path
import requests
from bs4 import BeautifulSoup as bs4
from bs4 import Comment
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
        print(name + " now")
        # compare

        # open saved version of the page
        with open("./latest-content/"+ name + ".html", "r", encoding='utf-8') as f:
            saved_page = f.read()
        soup = bs4(page.content, 'html.parser')
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        body = soup.find("body")#.text.strip()

        first = []
        for p in saved_page.splitlines():
            soup = bs4(p, 'html.parser')
            first.append(soup.text)

        second = []

        for p in str(body).splitlines():
            soup = bs4(p, 'html.parser')
            second.append(soup.text)
        # all_tags = soup.find_all()
        # for tag in all_tags:
        #     print(tag.get_text())
        #     print()
        # compare the two versions of the page

        diff = difflib.unified_diff(first, second, fromfile='saved_page', tofile='str(body)', lineterm='', n=0)
        lines = list(diff)[2:]
        added = [line[1:] for line in lines if line[0] == '+']
        removed = [line[1:] for line in lines if line[0] == '-']

        additions =[]
        print(len(lines))

        # print('additions:')
        # for line in added:
        #     print(line)
        # print("------------")
        # print('additions, ignoring position')
        for line in added:
            if line not in removed:
                # print(line)
                additions.append(line)
        # print(additions)
        changed[w] = additions

        # replace html with newest version
        with open("./latest-content/"+ name + ".html", "w", encoding='utf-8') as f:
            print("opening " + name)
            f.write(str(body))
    else:
        print("not found")
        # print(page.read())
        soup = bs4(page.content, 'html.parser')
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        body = soup.find("body")#.text.strip()
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
# print(changed)

with open("./emailcontent/email.html", "w", encoding='utf-8') as f:
    f.write("this is the email now\n")
    for key, value in changed.items():
        f.write(f"<h2>{key}</h2>")
        for items in value:
            f.write('<p>%s</p><br>' %items)
        f.write("   ")
# env_file = os.getenv('GITHUB_ENV')

# with open(env_file, "a") as myfile:
#     myfile.write("email=MY_VALUE")