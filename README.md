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
# Start applicatie
docker-compose up -d

# Stop applicatie
docker-compose down

# Logs bekijken
docker-compose logs -f

# Database backup maken
docker-compose exec survey-app tar -czf /app/backup.tar.gz -C /app/instance .
docker cp ggz-survey:/app/backup.tar.gz ./backup-$(date +%Y%m%d).tar.gz
```

Applicatie beschikbaar op `http://localhost:5000`

## Beheer

```bash
# Stop applicatie
docker-compose down

# Start applicatie
docker-compose up -d

# Logs bekijken
docker-compose logs -f

# Volume informatie
docker volume ls
docker volume inspect ggz-heuvelrug-vragenlijst_survey-data

# Database backup
docker-compose exec survey-app tar -czf /app/backup.tar.gz -C /app/instance .
docker cp ggz-survey:/app/backup.tar.gz ./backup-$(date +%Y%m%d).tar.gz
```

## Data Migratie

Als je al een draaiende container hebt zonder persistent volume:

```bash
# 1. Backup bestaande database
docker cp survey:/app/instance/survey.db ./survey.db.backup

# 2. Stop en verwijder oude container
docker stop survey
docker rm survey

# 3. Start met docker-compose
docker-compose up -d

# 4. Kopieer database terug (indien nodig)
docker cp ./survey.db.backup ggz-survey:/app/instance/survey.db
docker-compose restart
```

## Admin Panel

URL: `http://your-server:5000/admin/login`

## Technische Specificaties

- Flask 3.0 + Flask-WTF
- Python 3.11
- SQLite3
- python-dotenv 
- openpyxl