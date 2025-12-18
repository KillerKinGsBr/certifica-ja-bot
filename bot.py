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
# TERMO DE USO
# ========================
TERMO_USO = (
    "🛡️ *TERMO DE USO – SAMUEL CERTIFICAÇÕES*\n\n"
    "Declaro que estou contratando os serviços da *Samuel Certificações* "
    "(CNPJ nº 48.005.112/0001-61), referentes à *prestação de serviços educacionais*, "
    "incluindo *Educação de Jovens e Adultos (EJA)* e *Cursos de Graduação*, "
    "na modalidade *EAD*.\n\n"
    "Estou ciente de que:\n"
    "✔️ O serviço refere-se à formação educacional escolhida\n"
    "✔️ A entrega do diploma ou certificado é garantida mediante cumprimento das exigências do curso\n"
    "✔️ O ensino ocorre na modalidade EAD\n"
    "✔️ O não cumprimento de atividades, avaliações ou exigências documentais pode atrasar ou impedir a conclusão\n"
    "✔️ *Não há reembolso após o início do processo ou curso*\n"
    "✔️ Informações ou documentos falsos resultam em cancelamento imediato, sem devolução\n"
    "✔️ O aceite eletrônico possui plena validade jurídica\n\n"
    "📌 *Clique em ACEITAR para continuar.*"
)

# ========================
# CURSOS
# ========================
CURSOS = {
    "pos_graduacao": [
        {"nome": "Gestão Empresarial", "emoji": "🏢"},
        {"nome": "Gestão de Pessoas e RH", "emoji": "👥"},
        {"nome": "MBA em Administração", "emoji": "📊"},
        {"nome": "MBA em Gestão Financeira", "emoji": "💰"},
        {"nome": "Gestão Pública", "emoji": "🏛️"},
        {"nome": "Auditoria e Controladoria", "emoji": "🧾"},
    ],
    "superior": [
        {"nome": "Administração", "emoji": "🏢"},
        {"nome": "Pedagogia", "emoji": "📚"},
        {"nome": "Serviço Social", "emoji": "🤝"},
        {"nome": "Ciências Contábeis", "emoji": "🧾"},
    ],
    "medio": [
        {"nome": "Conclusão do Ensino Médio", "emoji": "📝"},
        {"nome": "Certificação por Competência", "emoji": "✅"},
    ],
    "tecnico": [
        {"nome": "Técnico em Administração", "emoji": "🏢"},
        {"nome": "Técnico em Enfermagem", "emoji": "🩺"},
    ]
}

# ========================
# DOCUMENTOS
# ========================
DOCUMENTOS = {
    "medio": ["RG", "CPF", "Comprovante de residência"],
    "superior": ["RG", "CPF", "Comprovante de residência", "Diploma do Ensino Médio"],
    "pos_graduacao": ["RG", "CPF", "Comprovante de residência", "Diploma do Ensino Superior"],
    "tecnico": ["RG", "CPF", "Comprovante de residência"],
}

CURSOS_POR_PAGINA = 6

# ========================
# START
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["aceitou_termo"] = False

    keyboard = [
        [InlineKeyboardButton("✅ ACEITAR", callback_data="aceitar_termo")],
        [InlineKeyboardButton("❌ NÃO ACEITO", callback_data="recusar_termo")]
    ]
    await update.message.reply_text(
        TERMO_USO,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ========================
# MENU PRINCIPAL
# ========================
async def mostrar_menu(query):
    keyboard = [
        [InlineKeyboardButton("🎓 Pós-Graduação", callback_data="pos_graduacao_0")],
        [InlineKeyboardButton("🎓 Ensino Superior", callback_data="superior_0")],
        [InlineKeyboardButton("🧑‍🎓 Ensino Médio", callback_data="medio_0")],
        [InlineKeyboardButton("🛠️ Cursos Técnicos", callback_data="tecnico_0")]
    ]
    await query.edit_message_text(
        "👋 *Bem-vindo(a)!*\nEscolha a categoria desejada:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ========================
# CALLBACK
# ========================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Aceite do termo
    if data == "aceitar_termo":
        context.user_data["aceitou_termo"] = True
        await mostrar_menu(query)
        return

    if data == "recusar_termo":
        await query.edit_message_text(
            "❌ Para utilizar nossos serviços, é obrigatório aceitar o Termo de Uso."
        )
        return

    if not context.user_data.get("aceitou_termo"):
        await query.edit_message_text("⚠️ É necessário aceitar o Termo de Uso para continuar.")
        return

    if data == "voltar":
        await mostrar_menu(query)
        return

    if data.startswith("curso_"):
        _, categoria, idx = data.split("_")
        curso = CURSOS[categoria][int(idx)]
        docs = DOCUMENTOS.get(categoria, [])
        lista = "\n".join(f"• {d}" for d in docs)

        await query.edit_message_text(
            f"{curso['emoji']} *{curso['nome']}*\n\n"
            f"📄 *Documentos necessários:*\n{lista}\n\n"
            "📌 Envie os documentos neste chat.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅ Voltar", callback_data=f"{categoria}_0")]]
            )
        )
        return

    if "_" in data:
        categoria, pagina = data.split("_")
        pagina = int(pagina)

        cursos = CURSOS[categoria]
        inicio = pagina * CURSOS_POR_PAGINA
        fim = inicio + CURSOS_POR_PAGINA

        keyboard = [
            [InlineKeyboardButton(f"{c['emoji']} {c['nome']}", callback_data=f"curso_{categoria}_{inicio+i}")]
            for i, c in enumerate(cursos[inicio:fim])
        ]

        keyboard.append([InlineKeyboardButton("⬅ Voltar", callback_data="voltar")])

        await query.edit_message_text(
            f"*Cursos de {categoria.replace('_', ' ').title()}*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

# ========================
# MAIN
# ========================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("🤖 Bot rodando...")
    app.run_polling()
