# monday-hackathon

## how to deploy

```bash
cp .env.example .env
# add OPENAI_API_KEY key to .env
# add MONDAY_API_KEY key to .env
docker compose up -d --build

# to download, format and import data use
localhost:8800/init

# to see magic use
localhost:8800/kowalskiAnalysis
```
