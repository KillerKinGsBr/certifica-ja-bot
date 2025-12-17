import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext
)

# =========================
# CONFIGURAÇÃO
# =========================
TOKEN = os.getenv("BOT_TOKEN")

ATENDENTE = "https://t.me/seu_usuario_aqui"  # troque depois

# =========================
# LISTAS DE CURSOS
# =========================

POS_GRADUACAO = [
    "Pós em Gestão Empresarial",
    "Pós em Educação Inclusiva",
    "Pós em Psicopedagogia",
    "Pós em Docência do Ensino Superior",
    "Pós em Gestão Pública"
]

ENSINO_MEDIO = [
    "Conclusão do Ensino Médio (EJA)"
]

SUPERIOR = [
    "Administração",
    "Pedagogia",
    "Gestão de Recursos Humanos",
    "Ciências Contábeis",
    "Serviço Social"
]

TECNICO = [
    "Técnico em Enfermagem",
    "Técnico em Segurança do Trabalho",
    "Técnico em Administração",
    "Técnico em Informática"
]

# =========================
# COMANDOS
# =========================

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🎓 Pós-Graduação", callback_data="pos")],
        [InlineKeyboardButton("📘 Ensino Médio", callback_data="medio")],
        [InlineKeyboardButton("🏫 Ensino Superior", callback_data="superior")],
        [InlineKeyboardButton("🛠 Técnico", callback_data="tecnico")],
        [InlineKeyboardButton("❓ Não encontrei meu curso", callback_data="atendente")]
    ]

    update.message.reply_text(
        "👋 *Bem-vindo à Certifica Já Brasil*\n\n"
        "📚 Vendas 24h de certificados e cursos reconhecidos pelo MEC.\n"
        "Escolha uma opção abaixo:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def menu_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    data = query.data

    if data == "pos":
        send_list(query, "🎓 *Pós-Graduação*", POS_GRADUACAO)
    elif data == "medio":
        send_list(query, "📘 *Ensino Médio*", ENSINO_MEDIO)
    elif data == "superior":
        send_list(query, "🏫 *Ensino Superior*", SUPERIOR)
    elif data == "tecnico":
        send_list(query, "🛠 *Cursos Técnicos*", TECNICO)
    elif data == "atendente":
        query.edit_message_text(
            "❗ Não encontrou o curso desejado?\n\n"
            "👉 Clique abaixo e fale com um atendente:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 Falar com atendente", url=ATENDENTE)]
            ])
        )

def send_list(query, title, items):
    text = f"{title}\n\n"
    for item in items:
        text += f"• {item}\n"

    text += (
        "\n💰 Valores sob consulta\n"
        "📄 Certificados válidos em todo território nacional\n\n"
        "👉 Para comprar, fale com um atendente."
    )

    query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Falar com atendente", url=ATENDENTE)],
            [InlineKeyboardButton("⬅️ Voltar ao menu", callback_data="voltar")]
        ])
    )

def voltar_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    start(query, context)

# =========================
# MAIN
# =========================

def main():
    if not TOKEN:
        raise Exception("BOT_TOKEN não configurado")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(menu_callback))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()            "• Marketing Digital\n\n"
            "📌 Caso seu curso não esteja na lista,\n"
            "clique em *Meu curso não está na lista*"
        )

    elif msg == "🎓 Ensino Superior":
        texto = (
            "🎓 *Graduação disponíveis:*\n\n"
            "• Administração\n"
            "• Pedagogia\n"
            "• Serviço Social\n"
            "• Ciências Contábeis\n\n"
            "📌 Caso seu curso não esteja na lista,\n"
            "clique em *Meu curso não está na lista*"
        )

    elif msg == "🧑‍🎓 Ensino Médio":
        texto = (
            "🧑‍🎓 *Ensino Médio:*\n\n"
            "• Conclusão do Ensino Médio\n"
            "• Certificação por Competência\n\n"
            "📌 Clique em falar com atendente"
        )

    elif msg == "🛠️ Curso Técnico":
        texto = (
            "🛠️ *Cursos Técnicos:*\n\n"
            "• Administração\n"
            "• Enfermagem\n"
            "• Segurança do Trabalho\n"
            "• Informática\n\n"
            "📌 Caso seu curso não esteja na lista,\n"
            "clique em *Meu curso não está na lista*"
        )

    if texto:
        await update.message.reply_text(
            texto,
            reply_markup=ReplyKeyboardMarkup(
                [["📌 Meu curso não está na lista"], ["🔙 Voltar"]],
                resize_keyboard=True
            ),
            parse_mode="Markdown"
        )

async def outros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == "📌 Meu curso não está na lista":
        await update.message.reply_text(
            "Sem problemas 👍\n\n"
            "Informe:\n"
            "• Nome do curso\n"
            "• Nível desejado\n\n"
            "Um atendente fará a cotação personalizada.",
            reply_markup=ReplyKeyboardMarkup(
                [["💬 Falar com atendente"], ["🔙 Voltar"]],
                resize_keyboard=True
            )
        )

    elif msg == "💬 Falar com atendente":
        await update.message.reply_text(
            "📲 Um consultor irá atendê-lo em breve.\n"
            "Aguarde alguns instantes.",
            reply_markup=menu_principal
        )

    elif msg == "🔙 Voltar":
        await start(update, context)

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cursos))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, outros))

app.run_polling()
