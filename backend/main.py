from fastapi import Depends, FastAPI, HTTPException, Request
import resend
import json
from config import Settings, get_settings

app = FastAPI()


@app.post("/")
async def receive_email(
    request: Request,
    settings: Settings = Depends(get_settings),
):
    body = await request.body()
    payload = body.decode("utf-8")

    if settings.resend_webhook_secret:
        try:
            resend.Webhooks.verify(
                {
                    "payload": payload,
                    "headers": {
                        "id": request.headers.get("svix-id"),
                        "timestamp": request.headers.get("svix-timestamp"),
                        "signature": request.headers.get("svix-signature"),
                    },
                    "webhook_secret": settings.resend_webhook_secret,
                }
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid webhook signature")
    else:
        raise HTTPException(status_code=400, detail="Resend webhook secret is not set")


    resend.api_key = settings.resend_api_key
    data = json.loads(payload)
    email_id = data.get("data").get("email_id")
    print("email_id", email_id)

    try:
        # Fetch the full email content
        print(f"Fetching email {email_id}...")
        email = resend.Emails.Receiving.get(email_id)

        print(f"From: {email['from']}")
        print(f"To: {', '.join(email.get('to', []))}")
        print(f"Subject: {email['subject']}")
        print(f"Created: {email['created_at']}")
        print()

        if email.get("text"):
            print("Text Body:")
            print(email["text"])
            print()

        if email.get("html"):
            print("HTML Body (truncated):")
            html = email["html"]
            print(html[:500])
            if len(html) > 500:
                print("...")
            print()

        # If there are attachments, list them
        if email.get("attachments"):
            print("Attachments:")
            for attachment in email["attachments"]:
                print(f"  - {attachment['filename']} ({attachment['content_type']})")

    except Exception as e:
        print(f"Error fetching email: {e}")
        print()
        print("Note: To test inbound emails:")
        print("1. Set up an inbound domain in Resend dashboard")
        print("2. Configure a webhook endpoint for email.received events")
        print("3. Use the email_id from the webhook payload")