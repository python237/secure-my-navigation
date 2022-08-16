import databases
import orm


database = databases.Database("sqlite:///db.sqlite")  # Connecter à la BD
models = orm.ModelRegistry(database=database)  # ORM

danger_choices = ["phishing", "scam", "ransomware"]  # Type de danger associés aux domaines fiché