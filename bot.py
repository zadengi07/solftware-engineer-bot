from telegram import Update, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

Admin_id = 7705097820

# Savol yuborish jarayonidagi foydalanuvchilarni saqlash
waiting_for_question = {}

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Assalomu alaykum.\n\n"
        "Ushbu bot orqali biz haqimizdagi ma’lumotlar va loyihalar bilan tanishishingiz mumkin.\n\n"
        "Yangilik va qo‘shimcha materiallarni kuzatib borish uchun quyidagi telegram kanalimizga obuna bo‘ling:\n"
        "https://t.me/khujaboevv_ceo"
    )

    keyboard = [
        [KeyboardButton("GitHub sahifa"), KeyboardButton("Помощник")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(text, reply_markup=reply_markup)


# /git komandasi
async def git_repo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("GitHub sahifamizga o‘tish", web_app=WebAppInfo(url="https://github.com/zadengi07"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Bizning barcha loyihalarimizni GitHub sahifamiz orqali ko‘rishingiz mumkin:",
        reply_markup=reply_markup
    )


# Oddiy tugmalarni ishlatish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    username = update.message.from_user.username or "Mavjud emas"
    fullname = update.message.from_user.full_name

    if text == "GitHub sahifa":
        keyboard = [
            [InlineKeyboardButton("GitHub sahifamizga o‘tish", web_app=WebAppInfo(url="https://github.com/zadengi07"))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Bizning barcha loyihalarimizni GitHub sahifamiz orqali ko‘rishingiz mumkin:",
            reply_markup=reply_markup
        )

    elif text == "Помощник":
        await update.message.reply_text(
            "Savol yuborish uchun quyidagi tugmalardan foydalaning:",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("Savol yuborish")], [KeyboardButton("Orqaga qaytish")]],
                resize_keyboard=True
            )
        )

    elif text == "Savol yuborish":
        waiting_for_question[user_id] = True
        await update.message.reply_text("Savolingizni yozib yuboring yoki orqaga qayting:")

    elif text == "Orqaga qaytish":
        waiting_for_question[user_id] = False
        await update.message.reply_text(
            "Asosiy menyuga qaytdingiz.",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("GitHub sahifa"), KeyboardButton("Помощник")]],
                resize_keyboard=True
            )
        )

    elif user_id in waiting_for_question and waiting_for_question[user_id]:
        msg = (
            f"Yangi savol keldi:\n\n"
            f"Ism: {fullname}\n"
            f"Username: @{username}\n"
            f"ID: {user_id}\n\n"
            f"Savol: {text}\n\n"
            f"Admin, javob yuborish uchun:\n"
            f"/reply {user_id} javob_matni"
        )
        await context.bot.send_message(Admin_id, msg)
        await update.message.reply_text("Savolingiz yuborildi. Tez orada javob beriladi.")
        waiting_for_question[user_id] = False

    else:
        await update.message.reply_text("Iltimos, mavjud tugmalardan birini tanlang.")


# Admin foydalanuvchiga javob berishi
async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != Admin_id:
        await update.message.reply_text("Siz admin emassiz.")
        return

    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("Foydalanish: /reply user_id javob_matni")
            return

        user_id = int(args[0])
        answer_text = " ".join(args[1:])

        await context.bot.send_message(user_id, f"Admin javobi:\n\n{answer_text}")
        await update.message.reply_text("Javob foydalanuvchiga yuborildi.")

    except Exception as e:
        await update.message.reply_text(f"Xatolik: {e}")


# Botni ishga tushirish
app = Application.builder().token("8442233859:AAFMynyQ0MHBAdeXIK5gMRBVQ0WlqM9tx38").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("git", git_repo))
app.add_handler(CommandHandler("reply", reply_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Работа наху")
app.run_polling()
