import sys

from errors import CommandError, CommandUnknown
from db.migrations import DBOperation
from website import runserver
from scrap import search_phishing_site


def add_default():
    db = DBOperation()
    
    # Add certified domain
    certified = [
        "portal.passcam.cm", 
        "www.prc.cm",
        "www.snh.cm", 
        "www.douanescustoms-cm.net", 
        "www.impots.cm", 
        "www.legicam.org", 
        "www.minfof.cm", 
        "www.minesep.gov.cm", 
        "www.mintour.gov.cm", 
        "www.minpmeesa.gov.cm", 
        "www.minesec.cm", 
        "www.minsante.gov.cm", 
        "www.minepat.cm", 
        "www.minresi.gov.cm", 
        "www.minproff.gov.cm", 
        "www.minpostel.gov.cm", 
        "www.minjeun.gov.cm", 
        "www.minfopra.gov.cm", 
        "www.minepia.cm", 
        "www.minep.gov.cm",
        "www.minesup.gov.cm", 
        "www.minefop.gov.cm", 
        "www.mindaf.gov.cm", 
        "www.minduh.gov.cm", 
        "www.mincom.gov.cm", 
        "www.mincommerce.gov.cm", 
        "www.minatd.net", 
        "www.spm.gov.cm", 
        "www.assnat.cm", 
        "www.presidenceducameroun.com",
        "camtel.cm",
        "ubacameroon.com",
        "www.ubacameroon.com",
        "dgsn.cm",
    ]
    
    # Add pattern
    pattern = [
        r"[a-z\-_.]{0,}passcam[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}prc\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}snh[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}legicam[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}gicam[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}impots[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?f[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?to[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?se[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?pme[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?pat[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?pia[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?\-?at[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}camtel[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?sa[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?r[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?p[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?j[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?p[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?sup[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?sup[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?daf[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?duh[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}mine?com[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}spm[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}dgsn[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}ass?\-?nat[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}presidenced?u?\-?cam[a-z\-_.]{0,}\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}camtel\.[a-z\-_.]{1,}$",
        r"[a-z\-_.]{0,}ubacam[a-z\-_.]{0,}\.[a-z\-_.]{1,}$"
    ]
    for p in pattern:
        db.add_pattern(str(p))


def exec_command(cmd: str, *extras):
    if cmd not in ["runserver", "search", "certified", "default"]:
        raise CommandUnknown(cmd)
    
    if cmd == "runserver":
        runserver()
    elif cmd == "search":
        search_phishing_site()
    elif cmd == "certified":
        db = DBOperation()
        
        if not extras:
            raise CommandError("domain to be certified has required")
        else:
            for dom in extras:
                db.add_certified(dom)
    else:
        add_default()


if __name__ == '__main__':
    try:
        exec_command(sys.argv[1], *sys.argv[2:])
    except IndexError:
        raise CommandError("command is required")
