from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

menu_principal = ReplyKeyboardMarkup(
    [
        ["🎓 Pós-graduação", "🎓 Ensino Superior"],
        ["🧑‍🎓 Ensino Médio", "🛠️ Curso Técnico"],
        ["💬 Falar com atendente"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🇧🇷 *Certifica Já Brasil*\n\n"
        "Grupo educacional com atuação nacional.\n"
        "Trabalhamos com instituições reconhecidas pelo MEC.\n\n"
        "📌 Certificados válidos em todo o Brasil\n"
        "📌 Processo rápido, seguro e sigiloso\n\n"
        "Escolha uma opção abaixo:",
        reply_markup=menu_principal,
        parse_mode="Markdown"
    )

async def cursos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    texto = ""

    if msg == "🎓 Pós-graduação":
        texto = (
            "🎓 *Pós-graduação disponíveis:*\n\n"
            "• Gestão de Pessoas\n"
            "• MBA em Administração\n"
            "• Gestão Pública\n"
            "• Docência do Ensino Superior\n"
            "• Marketing Digital\n\n"
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
