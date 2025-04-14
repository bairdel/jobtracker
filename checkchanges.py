import urllib.request
from urllib.parse import urlparse
# import os


with open("./websitesToCheck.txt", "r") as f:
    websites = f.readlines()

changed = []

# print(websites)
for w in websites:
    page = urllib.request.urlopen(w)
    name = urlparse(w).netloc
    with open("./latest-content/"+ name + ".html", "wb") as f:
        f.write(page.read())
print("sending this to you in an email")


# env_file = os.getenv('GITHUB_ENV')

# with open(env_file, "a") as myfile:
#     myfile.write("email=MY_VALUE")