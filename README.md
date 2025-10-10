# GGZ Heuvelrug Vragenlijst

Web-applicatie voor anonieme werkbeleving vragenlijst.

## Functionaliteit

- Anonieme vragenlijsten met 0-10 scoring
- Eenmalige toegang via unieke tokens
- Admin interface voor beheer
- Statistieken en gemiddelde scores
- SQLite database

## Installatie

### 1. Configuratie

Kopieer `.env.example` naar `.env`

```bash
cp .env.example .env
```

en configureer de vereiste waarden:

- `SECRET_KEY` (sterke willekeurige sleutel)
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `PORT` (per default ingesteld op 5000, ook in `Dockerfile`)

### 2. Docker Setup

```bash
# Build container
docker build -t survey-app .

# Run applicatie
docker run -d --name survey \
  -p 5000:5000 \
  -v $(pwd)/data:/app/instance \
  --env-file .env \
  --restart unless-stopped \
  survey-app
```

Applicatie beschikbaar op `http://localhost:5000`
## Beheer

```bash
# Stop applicatie
docker stop survey

# Start applicatie
docker start survey

# Logs bekijken
docker logs survey

# Backup data
cp -r ./data ./backup-$(date +%Y%m%d)
```

## Admin Panel

URL: `http://your-server:5000/admin/login`

## Technische Specificaties

- Flask 3.0 + Flask-WTF
- Python 3.11
- SQLite3
- python-dotenv 
- openpyxl 