import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import openai

# Get passwords
TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

if not TOKEN or not OPENAI_KEY:
    print("❌ Missing passwords!")
    exit(1)

openai.api_key = OPENAI_KEY

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        essay = update.message.text
        
        # Simple grading
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a TOEFL grader. Grade 0-6. Be strict."},
                {"role": "user", "content": f"Grade this essay: {essay}"}
            ]
        )
        
        await update.message.reply_text(response.choices[0].message.content)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    print("🤖 Bot starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot is running!")
    app.run_polling()

if __name__ == "__main__":
    main()
