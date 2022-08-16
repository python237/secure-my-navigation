import requests
import os
import tarfile

from db.migrations import DBOperation
from db import danger_choices
from db.models import Malicious

from datetime import datetime


db = DBOperation()
repo_source = [
    "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/ALL-phishing-domains.tar.gz",
    "https://malware-filter.gitlab.io/malware-filter/phishing-filter-domains.txt",
    "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-ACTIVE.txt",
]


def search_phishing_site():
    global repo_source
    
    for url in repo_source:
        filename = os.path.join(os.path.dirname(__file__), "download", os.path.basename(url))        
        print(filename)
        text_content = filename.endswith(".txt")
        
        with open(filename, "w" if text_content else "wb") as file:
            file.write(
                (lambda p: p.decode("utf-8") if not isinstance(p, str) and text_content else p)(requests.get(url).content)
            )
            file.close()
        
        if filename.endswith(".tar.gz"):
            tar = tarfile.open(filename)
            
            for member in tar.getmembers():
                f = tar.extractfile(member)
                if f is not None:
                    content = f.read().decode("utf-8")
                    save_phishing_site(content.split("\n"))
            
            tar.close()
        elif filename.endswith(".txt"):
            f = open(filename, "r")
            content = f.read()
            f.close()
            save_phishing_site(content.split("\n"))
            
        print(f"[{datetime.now()}] >> [{filename}] Removed")
        os.remove(filename)


def save_phishing_site(domain: list):
    global db
    
    for x in domain:
        if x.strip() and not x.strip().startswith("#") and not x.strip().startswith("//"):
            rs: Malicious = db.add_domain(x, danger_choices[0], True)
            print(f"[{datetime.now()}] >> [{rs.domain_name}] New phishing domain detected")
