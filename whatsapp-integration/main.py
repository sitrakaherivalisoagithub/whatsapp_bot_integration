from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
from dotenv import load_dotenv
from twilio.rest import Client


app = FastAPI()

# CORS configuration
origins = [
    # "http://localhost:3000",
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv(".env.twilio")
DIALOGFLOW_URL = os.getenv("DIALOGFLOW_URL", "https://bot-****.com/api/cx/webhook")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")  # format: whatsapp:+1234567890

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.get("/")
async def home():
    return {"message": "Hello whatsapp channel api"}

@app.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    user_number = form.get("From")
    user_text = form.get("Body")
    print(f"Received message from {user_number}: {user_text}")

    if not user_number or not user_text:
        return PlainTextResponse("Missing data", status_code=400)

    df_payload = {
        "text": user_text,
        "sessionInfo": {"session": user_number},
    }
    print(f'payload: {df_payload}')

    responses = []
    async with httpx.AsyncClient() as client:
        df_resp = await client.post(DIALOGFLOW_URL, json=df_payload, timeout=50.0)

        if df_resp.status_code != 200:
            return PlainTextResponse("Dialogflow call failed", status_code=502)
        df_data = df_resp.json()

        for msg in df_data.get("fulfillmentResponse", {}).get("messages", []):
            print(msg)
            if "text" in msg:
                for t in msg["text"]["text"]:
                    responses.append(t)

    # Envoi des réponses via Twilio API (maintenant en dehors du context manager)
    for text in responses:
        message = twilio_client.messages.create(
            body=text,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=user_number
        )
        print(f"Message envoyé : SID = {message.sid}")

    return {"success": True}

#uvicorn main:app --reload --host 0.0.0.0 --port 8000
