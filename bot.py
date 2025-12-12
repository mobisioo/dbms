# bot.py
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import db

TOKEN = os.environ["8396092811:AAHKWkw8lZ4DejbAeRdIhwsQZMTaVTc1c6w"] 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! دستورها:\n"
        "/tables\n"
        "/cols <table>\n"
        "/select <table>\n"
        "/insert <table> key=value key=value ...\n"
    )

async def tables(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = db.list_tables()
    await update.message.reply_text("\n".join(t) if t else "هیچ جدولی نیست.")

async def cols(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("مثال: /cols employees")
    table = context.args[0]
    c = db.list_columns(table)
    await update.message.reply_text(", ".join(c) if c else "ستونی پیدا نشد.")

async def select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("مثال: /select employees")
    table = context.args[0]
    cols, rows = db.select_all(table)

    # تلگرام پیام طولانی رو محدود می‌کنه؛ خروجی رو خلاصه می‌کنیم
    lines = [" | ".join(cols)]
    for r in rows[:20]:
        lines.append(" | ".join(map(str, r)))
    if len(rows) > 20:
        lines.append(f"... ({len(rows)-20} ردیف دیگر)")

    await update.message.reply_text("\n".join(lines))

async def insert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text(
            "مثال: /insert employees id=1 name=Ali"
        )
    table = context.args[0]
    pairs = context.args[1:]

    values = {}
    for p in pairs:
        if "=" not in p:
            return await update.message.reply_text(f"فرمت اشتباه: {p}")
        k, v = p.split("=", 1)
        # یه تبدیل ساده: عددها رو int کن
        if v.isdigit():
            v = int(v)
        values[k] = v

    db.insert_row(table, values)
    await update.message.reply_text("ثبت شد ✅")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tables", tables))
    app.add_handler(CommandHandler("cols", cols))
    app.add_handler(CommandHandler("select", select))
    app.add_handler(CommandHandler("insert", insert))
    app.run_polling()

if __name__ == "__main__":
    main()
