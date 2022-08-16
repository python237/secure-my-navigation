from db import *


class Malicious(orm.Model):
    """Table d'enregistrement des liens défini comme dangereux pour l'utilisateur.

    Args:
        orm ([domain_name]): le nom de domaine jugée dangereux.
        orm ([type]): le type de malveillance associée à l'adresse url.
        orm ([confirm]): détermine si la menace à été confirmé ou est en attente de confirmation.
    """
    tablename = "malicious"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "domain_name": orm.String(max_length=255, unique=True),
        "type": orm.String(max_length=255),
        "confirm": orm.Boolean(default=False),
        "created_at": orm.Date(),
        "updated_at": orm.Date(allow_null=True)
    }


class Signal(orm.Model):
    """ Table d'enregistrement des liens signalés par les utilisateurs lambda
    
    Args:
        orm ([domain]): Le nom de domaine signalée
        orm ([number]): Le nombre de signalement reçu
    """
    tablename = "signaled"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "domain": orm.String(max_length=255, unique=True),
        "number": orm.Integer(),
        "created_at": orm.Date()
    }


class Certified(orm.Model):
    """Table d'enregistrement des domaines certifiés

    Args:
        orm ([domain]): Domaine certifié
    """
    tablename = "domain_certify"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "domain": orm.String(max_length=255, unique=True),
        "created_at": orm.Date()
    }


class Pattern(orm.Model):
    """Table d'enregistrement des patterns

    Args:
        orm ([value]): La valeur du pattern
    """
    tablename = "patterns"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "value": orm.String(max_length=255, unique=True),
        "created_at": orm.Date()
    }
