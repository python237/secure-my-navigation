from datetime import date

import asyncio
from xml import dom
import orm.exceptions
import sqlite3

from db import *
from db.models import Certified, Malicious, Signal, Pattern
from utils.domain import add_domain_to_dataset


class DBOperation:
    """ Gère les opérations avec la base de données """
    
    def __init__(self) -> None:
        """ Création des tables """
        asyncio.run(models.create_all())

    def drop_all_table(self) -> None:
        """ Suppression des tables """
        models.drop_all()
    
    def get_all_malicious_domain(self) -> [Malicious]:
        """ Listing des noms de domaine confirmé  comme étant dangereux """
        try:
            return [x for x in asyncio.run(Malicious.objects.filter(confirm=True).all())]
        except sqlite3.OperationalError:
            return self.get_all_malicious_domain()
    
    def get_single_domain(self, domain_name: str) -> Malicious or None:
        try:
            return asyncio.run(Malicious.objects.get(domain_name=domain_name.lower()))
        except orm.exceptions.NoMatch:
            return None
        except sqlite3.OperationalError:
            return self.get_single_domain(domain_name)

    def add_domain(self, domain_name: str, danger: str, confirm: bool = False) -> Malicious:
        """ Ajout d'un nom de domaine """
        try:
            assert danger.lower() in danger_choices
            
            domain = self.get_single_domain(domain_name=domain_name.lower())
            if not domain:
                domain = asyncio.run(Malicious.objects.create(
                    domain_name=domain_name.lower(), 
                    type=danger.lower(),
                    confirm=confirm,
                    created_at=date.today()
                ))
            else:
                asyncio.run(domain.update(type=danger.lower(), confirm=confirm, updated_at=date.today()))
                
            return domain
        except sqlite3.OperationalError:
            return self.add_domain(domain_name, danger, confirm)
    
    def add_signal(self, domain: str) -> Signal:
        """ Ajout d'une alerte sur un nom de domaine """
        try:
            try:
                signal: Signal = asyncio.run(Signal.objects.get(domain=domain.lower()))
            except orm.exceptions.NoMatch:
                signal: Signal = None
            finally:
                if signal:
                    asyncio.run(signal.update(number=signal.number + 1))
                else:
                    signal = asyncio.run(Signal.objects.create(domain=domain.lower(), number=1, created_at=date.today()))
                
                return signal
        except sqlite3.OperationalError:
            return self.add_signal(domain)
        
    def add_certified(self, domain: str) -> Certified:
        """ Certifier un nom de domaine """
        try:
            try:
                certif: Certified = asyncio.run(Certified.objects.get(domain=domain.lower()))
            except orm.exceptions.NoMatch:
                certif: Certified = None
            finally:
                if not certif:
                    certif = asyncio.run(Certified.objects.create(domain=domain.lower(), created_at=date.today()))
                    # add_domain_to_dataset(certif.domain)
                
                return certif
        except sqlite3.OperationalError:
            return self.add_certified(domain)
        
    def get_certified_domain(self, domain: str) -> Certified or None:
        try:
            return asyncio.run(Certified.objects.get(domain=domain.lower()))
        except orm.exceptions.NoMatch:
            return None
        except sqlite3.OperationalError:
            return self.get_certified_domain(domain)
        
    def add_pattern(self, value: str) -> Pattern:
        """ Ajout d'un pattern """
        try:
            try:
                pattern: Pattern = asyncio.run(Pattern.objects.get(value=value.lower()))
            except orm.exceptions.NoMatch:
                pattern: Pattern = None
            finally:
                if not pattern:
                    pattern = asyncio.run(Pattern.objects.create(value=value.lower(), created_at=date.today()))
                
                return pattern
        except sqlite3.OperationalError:
            return self.add_pattern(value)
    
    def get_all_pattern(self) -> [Pattern]:
        """ Listing de tous les patterns """
        try:
            return [x for x in asyncio.run(Pattern.objects.all())]
        except sqlite3.OperationalError:
            return self.get_all_pattern()
