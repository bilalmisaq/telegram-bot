import os
PORT = int(os.environ.get("PORT", 10000))
import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import openai

# Get passwords from Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    print("❌ Missing TELEGRAM_TOKEN or OPENAI_API_KEY!")
    exit(1)

openai.api_key = OPENAI_API_KEY

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text
        
        # Your grading prompt
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a TOEFL essay grader. Grade on 0-6 scale."},
                {"role": "user", "content": f"Grade this essay: {user_message}"}
            ]
        )
        
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    print("🤖 Starting TOEFL Essay Grader Bot...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot is running! Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
