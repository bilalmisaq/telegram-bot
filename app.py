import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import openai

# Get the secret passwords from the environment
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

async def handle_message(update: Update, context):
    user_text = update.message.text
    # *** YOUR GRADING PROMPT GOES HERE ***
    # You'll craft a specific message to send to the AI with your rubric.
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Grade this essay: {user_text}"}]
    )
    await update.message.reply_text(response.choices[0].message.content)

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()