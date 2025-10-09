# GGZ Heuvelrug Vragenlijst

Web-applicatie voor anonieme werkbeleving vragenlijst.

## Functionaliteit

- Anonieme vragenlijsten met 0-10 scoring
- Eenmalige toegang via unieke tokens
- Admin interface voor beheer
- Statistieken en gemiddelde scores
- SQLite database

## Installatie

```bash
apt-get update
apt-get install -y python3 python3-pip python3-venv

chmod +x setup.sh
./setup.sh
```

## Starten

```bash
source venv/bin/activate
python3 app.py
```

Applicatie beschikbaar op `http://localhost:8000`

Andere port gebruiken:
```bash
PORT=5000 python3 app.py
```

## Configuratie

Optioneel environment variabelen:

```bash
export PORT=5000
export SECRET_KEY='your-secret-key'
export ADMIN_USERNAME='admin'
export ADMIN_PASSWORD='admin'
```

Defaults: port 8000, admin / admin

## Admin Panel

URL: `http://your-server:PORT/admin/login`


## Database Backup

```bash
cp instance/survey.db instance/survey.db.backup-$(date +%Y%m%d)
```

## Technische Specificaties

- Flask 3.0
- Python 3.8+
- SQLite3