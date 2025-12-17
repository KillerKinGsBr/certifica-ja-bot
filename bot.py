import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ========================
# TOKEN
# ========================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN não configurado")

# ========================
# CURSOS COM DESCRIÇÃO
# ========================
CURSOS = {
    "pos_graduacao": [
        {"nome": "Gestão Empresarial", "emoji": "🏢", "url": "https://link-para-matricula.com"},
        {"nome": "Gestão de Pessoas e RH", "emoji": "👥", "url": "https://link-para-matricula.com"},
        {"nome": "MBA em Administração", "emoji": "📊", "url": "https://link-para-matricula.com"},
        {"nome": "MBA em Gestão Financeira", "emoji": "💰", "url": "https://link-para-matricula.com"},
        {"nome": "Gestão Pública", "emoji": "🏛️", "url": "https://link-para-matricula.com"},
        {"nome": "Auditoria e Controladoria", "emoji": "🧾", "url": "https://link-para-matricula.com"},
        {"nome": "Docência do Ensino Superior", "emoji": "🎓", "url": "https://link-para-matricula.com"},
        {"nome": "Psicopedagogia", "emoji": "🧠", "url": "https://link-para-matricula.com"},
        {"nome": "Gestão Escolar", "emoji": "🏫", "url": "https://link-para-matricula.com"},
        {"nome": "Segurança do Trabalho", "emoji": "🦺", "url": "https://link-para-matricula.com"},
        {"nome": "Direito do Trabalho e Previdenciário", "emoji": "⚖️", "url": "https://link-para-matricula.com"},
        {"nome": "Enfermagem do Trabalho", "emoji": "🩺", "url": "https://link-para-matricula.com"},
        {"nome": "Saúde Pública", "emoji": "🏥", "url": "https://link-para-matricula.com"},
        {"nome": "Marketing Digital", "emoji": "💻", "url": "https://link-para-matricula.com"},
        {"nome": "Gestão Hospitalar", "emoji": "🏨", "url": "https://link-para-matricula.com"},
    ],
    "superior": [
        {"nome": "Administração", "emoji": "🏢", "url": "https://link-para-matricula.com"},
        {"nome": "Pedagogia", "emoji": "📚", "url": "https://link-para-matricula.com"},
        {"nome": "Serviço Social", "emoji": "🤝", "url": "https://link-para-matricula.com"},
        {"nome": "Ciências Contábeis", "emoji": "🧾", "url": "https://link-para-matricula.com"},
        {"nome": "Educação Física", "emoji": "🏃‍♂️", "url": "https://link-para-matricula.com"},
        {"nome": "Gestão de Recursos Humanos", "emoji": "👥", "url": "https://link-para-matricula.com"},
        {"nome": "Gestão Financeira", "emoji": "💰", "url": "https://link-para-matricula.com"},
        {"nome": "Logística", "emoji": "🚚", "url": "https://link-para-matricula.com"},
        {"nome": "Marketing", "emoji": "📈", "url": "https://link-para-matricula.com"},
        {"nome": "Processos Gerenciais", "emoji": "⚙️", "url": "https://link-para-matricula.com"},
        {"nome": "Análise e Desenvolvimento de Sistemas", "emoji": "💻", "url": "https://link-para-matricula.com"},
        {"nome": "Sistemas de Informação", "emoji": "🖥️", "url": "https://link-para-matricula.com"},
        {"nome": "Engenharia de Produção", "emoji": "🏭", "url": "https://link-para-matricula.com"},
        {"nome": "Gestão Pública", "emoji": "🏛️", "url": "https://link-para-matricula.com"},
    ],
    "medio": [
        {"nome": "Conclusão do Ensino Médio", "emoji": "📝", "url": "https://link-para-matricula.com"},
        {"nome": "Certificação por Competência", "emoji": "✅", "url": "https://link-para-matricula.com"},
        {"nome": "Histórico Escolar", "emoji": "📄", "url": "https://link-para-matricula.com"},
        {"nome": "Declaração de Conclusão", "emoji": "🖋️", "url": "https://link-para-matricula.com"},
        {"nome": "Certificado válido nacional", "emoji": "🎖️", "url": "https://link-para-matricula.com"},
    ],
    "tecnico": [
        {"nome": "Técnico em Administração", "emoji": "🏢", "url": "https://link-para-matricula.com"},
        {"nome": "Técnico em Enfermagem", "emoji": "🩺", "url": "https://link-para-matricula.com"},
        {"nome": "Técnico em Segurança do Trabalho", "emoji": "🦺", "url": "https://link-para-matricula.com"},
        {"nome": "Técnico em Logística", "emoji": "🚚", "url": "https://link-para-matricula.com"},
        {"nome": "Técnico em Informática", "emoji": "💻", "url": "https://link-para-matricula.com"},
        {"nome": "Técnico em Eletrotécnica", "emoji": "⚡", "url": "https://link-para-matricula.com"},
        {"nome": "Técnico em Mecânica", "emoji": "🔧", "url": "https://link-para-matricula.com"},
        {"nome": "Técnico em Recursos Humanos", "emoji": "👥", "url": "https://link-para-matricula.com"},
        {"nome": "Técnico em Contabilidade", "emoji": "🧾", "url": "https://link-para-matricula.com"},
        {"nome": "Técnico em Edificações", "emoji": "🏗️", "url": "https://link-para-matricula.com"},
    ]
}

# ========================
# HANDLER /start
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎓 Pós-Graduação", callback_data="pos_graduacao")],
        [InlineKeyboardButton("🎓 Ensino Superior", callback_data="superior")],
        [InlineKeyboardButton("🧑‍🎓 Ensino Médio", callback_data="medio")],
        [InlineKeyboardButton("🛠️ Cursos Técnicos", callback_data="tecnico")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Olá! Bem-vindo(a) ao nosso bot de cursos.\nEscolha a categoria desejada:",
        reply_markup=reply_markup
    )

# ========================
# CALLBACK DOS BOTÕES
# ========================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Mostrar lista de cursos conforme categoria
    if data in CURSOS:
        cursos_categoria = CURSOS[data]
        keyboard = [
            [InlineKeyboardButton(f"{curso['emoji']} {curso['nome']}", callback_data=f"curso_{data}_{idx}")]
            for idx, curso in enumerate(cursos_categoria)
        ]
        keyboard.append([InlineKeyboardButton("⬅ Voltar", callback_data="voltar")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"*Cursos de {data.replace('_', ' ').title()}*",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    # Mostrar informações sobre curso selecionado
    elif data.startswith("curso_"):
        parts = data.split("_")
        categoria = parts[1]
        idx = int(parts[2])
        curso = CURSOS[categoria][idx]
        msg = f"{curso['emoji']} *{curso['nome']}*\n\n✅ Certificado reconhecido pelo MEC.\nClique no botão abaixo para matrícula."
        keyboard = [
            [InlineKeyboardButton("⬅ Voltar", callback_data=categoria)],
            [InlineKeyboardButton("📋 Matricular", url=curso["url"])]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg, reply_markup=reply_markup, parse_mode="Markdown")

    # Voltar para menu inicial
    elif data == "voltar":
        await start(update, context)

# ========================
# FUNÇÃO PRINCIPAL
# ========================
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("Bot rodando...")
    await app.run_polling()

# ========================
# INÍCIO
# ========================
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
