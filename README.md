# KK2 - AI-driven Speldataanalys

KK2 är en FastAPI-baserad applikation designad för att ladda upp, processa och analysera speldata från CSV-filer. Applikationen kombinerar traditionell dataanalys med lokala språkmodeller (LLM) för att svara på frågor om datan.

## Funktioner

*   **CSV-uppladdning:** Ladda upp dataset (t.ex. `games.csv`) för omedelbar analys.
*   **Regelbaserad analys:** Snabba svar på vanliga frågor (t.ex. "Vilket är det dyraste spelet?").
*   **AI-integration:** Använder `SmolLM2-135M-Instruct` via HuggingFace Transformers för att svara på frågor baserat på uppladdad statistik.
*   **Datarensning:** Hanterar automatiskt felaktiga priser och rensar data vid uppladdning.

## Installation

1.  Klona repot:
    ```bash
    git clone <https://github.com/din-användare/KK2.git>
    cd KK2
    ```

2.  Skapa och aktivera en virtuell miljö:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # På Windows: .venv\Scripts\activate
    ifall du använder uv behövs det ingen aktivering av .venv
    ```


3.  Installera beroenden:
    ```bash
    pip install -r requerments.txt
    uv sync 
    ```


4.  Installera Dataset: 
    ```Webbläsare 
    gå in på denna sidan: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/data 

    tryck på download och sedan unzipa filen och använd csv filen. 
    ```

## Användning

1.  Starta servern:
    ```bash
    uv run uvicorn app.main:app --reload
    ```

2.  Öppna dokumentationen i webbläsaren:
    Gå till `http://127.0.0.1:8000/docs` för att interagera med API:et via Swagger UI.

## API-Endpoints

### Datahantering
*   `POST /data/upload`: Laddar upp CSV-filen eller ifall du har en annan steam data så kör på det. Filen förväntas innehålla kolumner som `Name` och `Price`.
*   `GET /data/stats`: Returnerar statistik om det dyraste spelet i det uppladdade datasetet.

### AI & Analys
*   `POST /ai/ask`: Ställ en fråga om dina spel.
    *   *Exempel:* "Vilket spel kostar mest?" eller "Ge mig en sammanfattning av listan".
    *   Applikationen väljer automatiskt mellan ett regelbaserat svar eller att skicka datan till AI-modellen.
    *   Just nu fungerar ändast att fråga vilket som är det dyraste spelet.

### Data stats
*   `GET /data/stats` Kontrollerar att data är inläst.

### System
*   `GET /health`: Kontrollerar att tjänsten är online.

## Teknikstack
*   **Ramverk:** FastAPI
*   **Data:** Pandas & NumPy
*   **AI-modell:** HuggingFace `SmolLM2-135M-Instruct`
*   **Server:** Uvicorn

### Testing

1. För att starta tester så kör commandot förutsatt att du står i root directory: 
uv run pytest app/tests/ -v