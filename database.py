from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import sqlite3

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("images.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY,
            label TEXT NOT NULL,
            file_id TEXT NOT NULL
        )
    """)
    # Example: Pre-populate with a sample image (replace file_id with actual Telegram file_id)
    cursor.execute("INSERT OR IGNORE INTO images (label, file_id) VALUES (?, ?)",
                  ("apple", "YOUR_TELEGRAM_FILE_ID"))
    conn.commit()
    conn.close()

# Handle /search command
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args).lower()  # Get the word after /search
    if not query:
        await update.message.reply_text("Please provide a word, e.g., /search apple")
        return

    # Query database
    conn = sqlite3.connect("images.db")
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM images WHERE label = ?", (query,))
    result = cursor.fetchone()
    conn.close()

    if result:
        file_id = result[0]
        await update.message.reply_photo(photo=file_id)
    else:
        await update.message.reply_text(f"No photo found for '{query}'")

# Main function
async def main():
    init_db()
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("search", search))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())