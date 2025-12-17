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
        {"nome": "Gestão Empresarial", "emoji": "🏢"},
        {"nome": "Gestão de Pessoas e RH", "emoji": "👥"},
        {"nome": "MBA em Administração", "emoji": "📊"},
        {"nome": "MBA em Gestão Financeira", "emoji": "💰"},
        {"nome": "Gestão Pública", "emoji": "🏛️"},
        {"nome": "Auditoria e Controladoria", "emoji": "🧾"},
        {"nome": "Docência do Ensino Superior", "emoji": "🎓"},
        {"nome": "Psicopedagogia", "emoji": "🧠"},
        {"nome": "Gestão Escolar", "emoji": "🏫"},
        {"nome": "Segurança do Trabalho", "emoji": "🦺"},
        {"nome": "Direito do Trabalho e Previdenciário", "emoji": "⚖️"},
        {"nome": "Enfermagem do Trabalho", "emoji": "🩺"},
        {"nome": "Saúde Pública", "emoji": "🏥"},
        {"nome": "Marketing Digital", "emoji": "💻"},
        {"nome": "Gestão Hospitalar", "emoji": "🏨"},
    ],
    "superior": [
        {"nome": "Administração", "emoji": "🏢"},
        {"nome": "Pedagogia", "emoji": "📚"},
        {"nome": "Serviço Social", "emoji": "🤝"},
        {"nome": "Ciências Contábeis", "emoji": "🧾"},
        {"nome": "Educação Física", "emoji": "🏃‍♂️"},
        {"nome": "Gestão de Recursos Humanos", "emoji": "👥"},
        {"nome": "Gestão Financeira", "emoji": "💰"},
        {"nome": "Logística", "emoji": "🚚"},
        {"nome": "Marketing", "emoji": "📈"},
        {"nome": "Processos Gerenciais", "emoji": "⚙️"},
        {"nome": "Análise e Desenvolvimento de Sistemas", "emoji": "💻"},
        {"nome": "Sistemas de Informação", "emoji": "🖥️"},
        {"nome": "Engenharia de Produção", "emoji": "🏭"},
        {"nome": "Gestão Pública", "emoji": "🏛️"},
    ],
    "medio": [
        {"nome": "Conclusão do Ensino Médio", "emoji": "📝"},
        {"nome": "Certificação por Competência", "emoji": "✅"},
        {"nome": "Histórico Escolar", "emoji": "📄"},
        {"nome": "Declaração de Conclusão", "emoji": "🖋️"},
        {"nome": "Certificado válido nacional", "emoji": "🎖️"},
    ],
    "tecnico": [
        {"nome": "Técnico em Administração", "emoji": "🏢"},
        {"nome": "Técnico em Enfermagem", "emoji": "🩺"},
        {"nome": "Técnico em Segurança do Trabalho", "emoji": "🦺"},
        {"nome": "Técnico em Logística", "emoji": "🚚"},
        {"nome": "Técnico em Informática", "emoji": "💻"},
        {"nome": "Técnico em Eletrotécnica", "emoji": "⚡"},
        {"nome": "Técnico em Mecânica", "emoji": "🔧"},
        {"nome": "Técnico em Recursos Humanos", "emoji": "👥"},
        {"nome": "Técnico em Contabilidade", "emoji": "🧾"},
        {"nome": "Técnico em Edificações", "emoji": "🏗️"},
    ]
}

# ========================
# DOCUMENTOS POR CATEGORIA
# ========================
DOCUMENTOS = {
    "medio": [
        "RG", "CPF", "Comprovante de residência", "Título de eleitor",
        "Certidão de nascimento", "Histórico do fundamental", "Reservista"
    ],
    "superior": [
        "RG", "CPF", "Comprovante de residência", "Título de eleitor",
        "Certidão de nascimento", "Diploma do Ensino Médio", "Certidão de quitação eleitoral"
    ],
    "pos_graduacao": [
        "RG", "CPF", "Comprovante de residência", "Título de eleitor",
        "Certidão de nascimento", "Diploma do Ensino Superior", "Certidão de quitação eleitoral"
    ],
    "tecnico": [
        "RG", "CPF", "Comprovante de residência", "Título de eleitor",
        "Certidão de nascimento", "Histórico do fundamental", "Reservista"
    ],
    "tecnologo": [  # caso queira futuramente incluir tecnólogo
        "RG", "CPF", "Comprovante de residência", "Título de eleitor",
        "Certidão de nascimento", "Diploma do Ensino Superior", "Certidão de quitação eleitoral"
    ]
}

# ========================
# PAGINAÇÃO
# ========================
CURSOS_POR_PAGINA = 6

# ========================
# HANDLER /start
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎓 Pós-Graduação", callback_data="pos_graduacao_0")],
        [InlineKeyboardButton("🎓 Ensino Superior", callback_data="superior_0")],
        [InlineKeyboardButton("🧑‍🎓 Ensino Médio", callback_data="medio_0")],
        [InlineKeyboardButton("🛠️ Cursos Técnicos", callback_data="tecnico_0")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Olá! Bem-vindo(a) ao nosso bot de matrícula.\nEscolha a categoria desejada:",
        reply_markup=reply_markup
    )

# ========================
# CALLBACK DOS BOTÕES
# ========================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "voltar":
        await start(update, context)
        return

    # Curso escolhido
    if data.startswith("curso_"):
        _, categoria, idx = data.split("_")
        idx = int(idx)
        curso = CURSOS[categoria][idx]

        documentos = DOCUMENTOS.get(categoria, [])
        lista_docs = "\n".join(f"• {doc}" for doc in documentos)

        msg = (
            f"{curso['emoji']} *{curso['nome']}*\n\n"
            f"Para efetuar a matrícula, por favor envie os seguintes documentos:\n\n{lista_docs}\n\n"
            "📌 Envie os documentos em formato de foto ou PDF neste chat."
        )

        keyboard = [[InlineKeyboardButton("⬅ Voltar", callback_data=f"{categoria}_0")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg, reply_markup=reply_markup, parse_mode="Markdown")
        return

    # Paginação
    if "_" in data:
        categoria, pagina = data.split("_")
        pagina = int(pagina)
        cursos_categoria = CURSOS[categoria]
        inicio = pagina * CURSOS_POR_PAGINA
        fim = inicio + CURSOS_POR_PAGINA
        subset = cursos_categoria[inicio:fim]

        keyboard = [
            [InlineKeyboardButton(f"{curso['emoji']} {curso['nome']}", callback_data=f"curso_{categoria}_{inicio + i}")]
            for i, curso in enumerate(subset)
        ]

        nav_buttons = []
        if pagina > 0:
            nav_buttons.append(InlineKeyboardButton("⬅ Anterior", callback_data=f"{categoria}_{pagina - 1}"))
        if fim < len(cursos_categoria):
            nav_buttons.append(InlineKeyboardButton("Próximo ➡", callback_data=f"{categoria}_{pagina + 1}"))
        if nav_buttons:
            keyboard.append(nav_buttons)

        keyboard.append([InlineKeyboardButton("⬅ Voltar", callback_data="voltar")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"*Cursos de {categoria.replace('_', ' ').title()}*",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

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
