from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {
        "afspraken": {
            "afspraak1": {
                "titel": "Docter Appointment",
                "dag": 12,
                "maand": "januari",
                "jaar": 2025,
            },
            "afspraak2": {
                "titel": "cinema",
                "dag": 30,
                "maand": "januari",
                "jaar": 2025,
            },
            "afspraak3": {
                "titel": "verjaardag",
                "dag": 1,
                "maand": "februari",
                "jaar": 2025,
            },
        }
    }
