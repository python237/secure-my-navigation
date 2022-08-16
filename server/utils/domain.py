import csv
import os
import random
import re
import string
from datetime import datetime

from db.models import Malicious


def add_domain_to_dataset(domain: str) -> None:
    """ 
    Ajout du nom de domaine à un dataset. 
    !!! Fonction à utiliser lorsque l'implémentation de l'intelligence artificielle sera effectif.
    """
    # Emplacement du dataset
    dataset_location = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets.csv")
    
    data: list = []
    domain: str = domain.lower()
    domain_split: list = domain.split(".")
    domain_body: str = domain_split[0]
    
    # 1. Ajout du nom de domaine certifié
    data.append([domain, "", 1])
    
    # 2. Ajout d'une composante de nom érroné, basé sur le changement de l'extension
    available_extension = ["io", "net", "cm", "com", "fr", "it", "dev", "biz", "de", "ci"]
    for ext in available_extension:
        if not domain.endswith(f".{ext}"):
            data.append([".".join(domain_split[:-1] + [ext]), domain, 0])
    
    # 3. Ajout d'une composante de nom érroné, basé sur la suppression de 1 ou 2 lettres
    step = 1 if len(domain_body) >= 5 else 3
    while step < (3 if len(domain_body) >= 8 else 2):        
        min_ = 0
        max_ = min_ + step
        
        while max_ <= len(domain_body):
            data.append([".".join(["".join(domain_body[:min_] + domain_body[max_:]), ".".join(domain_split[1:])]), domain, 0])    
            
            if max_ >= len(domain_body):
                max_ += 1
            else:
                min_ = max_
                max_ += step
            
                if max_ > len(domain_body):
                    max_ = len(domain_body)
                    min_ = max_ - step
            
        step += 1
    
    # 4. Ajout d'une composante de nom érronée, basé sur l'ajout de  tiret de 6 ou de 8
    for es in ["-", "_"]:
        for _ in range(1, 50):
            data.append([".".join([f"{es}".join([domain_body, "".join(random.sample(string.ascii_lowercase, 8))]), ".".join(domain_split[1:])]), domain, 0])
            
    # 5. Ajout d'une composante de nom érronée, basé sur l'ajout en tant que sous-domaine
    for _ in range(1, 100):
        data.append([".".join([domain_body, "".join(random.sample(string.ascii_lowercase, 8)), ".".join(domain_split[1:])]), domain, 0])

    
    with open(dataset_location, 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
        f.close()
        
    # --
    print(f"[{datetime.now()}] >> Add «{domain.lower()}» to certified domain")



def is_malicious_domain(host_source: str, db) -> bool:
    """
    Détermine si un nom de domaine est dangereux
    """
    host_source = host_source.lower()
    correspondance = ["a", "e", "u", "i", "o", "y"]
    
    domain: Malicious or None = db.get_single_domain(host_source)
    if domain and domain.confirm:
        return True
    
    if re.match(r"^[a-z\-_.]{1,}\.gov\.cm$", host_source):
        if not db.get_certified_domain(host_source):
            return True
        
    for x in db.get_all_pattern():
        if re.match(r"%(pattern)s" % {"pattern": x.value}, host_source):
            if not db.get_certified_domain(host_source):
                return True
          
    if re.match(r"^[0-9]{4,}[a-z\-_.]{0,}$", host_source):
        return True
    
    pattern = "".join(host_source.split(".")[:-1]).replace("www", "")
    matches = 0
    
    for x in pattern:
        if x not in correspondance:
            matches += 1
        else:
            matches = 0
            
        if matches >= 5:
            return True
    
    return False