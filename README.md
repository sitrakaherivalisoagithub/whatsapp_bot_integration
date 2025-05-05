# WhatsApp Integration with Twilio and Dialogflow

This project provides an API that integrates WhatsApp messaging (via Twilio) with a Dialogflow conversational agent. It allows users to interact with a chatbot through WhatsApp, with the conversation logic handled by Dialogflow.

## Features

- Receive WhatsApp messages via Twilio webhook
- Process messages through Dialogflow CX
- Send responses back to users via WhatsApp
- Simple FastAPI-based implementation

## Prerequisites

- Python 3.7+
- Twilio account with WhatsApp sandbox or business account
- Dialogflow CX agent
- FastAPI and related dependencies

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/whatsapp-integration.git
cd whatsapp-integration
```

2. Create a virtual environment and install dependencies:

```python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3. Create a .env.twilio file with your credentials
> DIALOGFLOW_URL=https://your-dialogflow-webhook-url.com/api/cx/webhook
>TWILIO_ACCOUNT_SID=your_twilio_account_sid
>TWILIO_AUTH_TOKEN=your_twilio_auth_token
>TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890

## Usage
1. Start the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
2. Configure your Twilio WhatsApp sandbox or business account to use your server's /whatsapp/webhook endpoint as the webhook URL.
3. Users can now send messages to your WhatsApp number, and they will receive responses from your Dialogflow agent.
## API Enpoints
- `POST /whatsapp/webhook`: Webhook endpoint for Twilio WhatsApp messages
- `GET /health`: Check the health of the API.
## How it works
1. A user sends a message to your WhatsApp number
2. Twilio forwards the message to your webhook endpoint
3. The application extracts the message and user information
4. The message is sent to Dialogflow for processing
5. Dialogflow's response is sent back to the user via Twilio's WhatsApp API
## Deployment
For production deployment, consider:
- Using a production ASGI server
- Setting up proper CORS configuration
- Implementing authentication for your API
- Using environment variables for all sensitive information

