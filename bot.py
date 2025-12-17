import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# =========================
# TOKEN
# =========================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN não configurado")

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 Ensino Médio", callback_data="medio")],
        [InlineKeyboardButton("🛠 Cursos Técnicos", callback_data="tecnico")],
        [InlineKeyboardButton("🎓 Graduação", callback_data="graduacao")],
        [InlineKeyboardButton("📚 Pós-graduação", callback_data="pos")],
        [InlineKeyboardButton("💬 Falar com atendente", callback_data="atendente")]
    ]

    await update.message.reply_text(
        "👋 *Bem-vindo à Certifica Já Brasil*\n\n"
        "📚 Cursos e certificados reconhecidos pelo MEC.\n"
        "Escolha uma opção abaixo:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================
# CALLBACK MENU
# =========================
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "medio":
        texto = (
            "📘 *Ensino Médio*\n\n"
            "✔ Conclusão do ensino médio\n"
            "✔ Certificado reconhecido pelo MEC\n"
            "✔ Válido em todo o Brasil"
        )

    elif query.data == "tecnico":
        texto = (
            "🛠 *Cursos Técnicos*\n\n"
            "• Técnico em Enfermagem\n"
            "• Técnico em Segurança do Trabalho\n"
            "• Técnico em Administração\n"
            "• Técnico em Informática"
        )

    elif query.data == "graduacao":
        texto = (
            "🎓 *Graduação (Ensino Superior)*\n\n"
            "• Administração\n"
            "• Pedagogia\n"
            "• Serviço Social\n"
            "• Ciências Contábeis"
        )

    elif query.data == "pos":
        texto = (
            "📚 *Pós-graduação*\n\n"
            "✔ Especializações reconhecidas\n"
            "✔ Certificado válido em todo o Brasil"
        )

    elif query.data == "atendente":
        texto = (
            "💬 *Atendimento Humano*\n\n"
            "Clique no botão abaixo para falar com um consultor
