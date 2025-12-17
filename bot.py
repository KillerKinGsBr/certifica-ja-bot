import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================
# CONFIGURAÇÕES
# =========================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN não configurado")

ADMIN_ID = 1059125588  # Seu ID
LEADS_FILE = "leads.txt"

# Horário de atendimento (opcional)
ATENDIMENTO_INICIO = 8   # 08:00
ATENDIMENTO_FIM = 22     # 22:00

# =========================
# LISTAS DE CURSOS
# =========================
POS = [
    "Gestão Empresarial",
    "Gestão de Pessoas e RH",
    "MBA em Administração",
    "MBA em Gestão Financeira",
    "Gestão Pública",
    "Auditoria e Controladoria",
    "Docência do Ensino Superior",
    "Psicopedagogia",
    "Gestão Escolar",
    "Segurança do Trabalho",
    "Direito do Trabalho e Previdenciário",
    "Enfermagem do Trabalho",
    "Saúde Pública",
    "Marketing Digital",
    "Gestão Hospitalar"
]

GRAD = [
    "Administração",
    "Pedagogia",
    "Serviço Social",
    "Ciências Contábeis",
    "Educação Física",
    "Gestão de Recursos Humanos",
    "Gestão Financeira",
    "Logística",
    "Marketing",
    "Processos Gerenciais",
    "Análise e Desenvolvimento de Sistemas",
    "Sistemas de Informação",
    "Engenharia de Produção",
    "Gestão Pública"
]

MEDIO = [
    "Conclusão do Ensino Médio",
    "Certificação por Competência",
    "Histórico Escolar",
    "Declaração de Conclusão",
    "Certificado válido nacional"
]

TECNICO = [
    "Técnico em Administração",
    "Técnico em Enfermagem",
    "Técnico em Segurança do Trabalho",
    "Técnico em Logística",
    "Técnico em Informática",
    "Técnico em Eletrotécnica",
    "Técnico em Mecânica",
    "Técnico em Recursos Humanos",
    "Técnico em Contabilidade",
    "Técnico em Edificações"
]

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    keyboard = [
        [InlineKeyboardButton("📘 Ensino Médio", callback_data="medio")],
        [InlineKeyboardButton("🛠 Cursos Técnicos", callback_data="tecnico")],
        [InlineKeyboardButton("🎓 Graduação", callback_data="graduacao")],
        [InlineKeyboardButton("📚 Pós-graduação", callback_data="pos")],
        [InlineKeyboardButton("❓ Não encontrei meu curso", callback_data="outro")]
    ]
    await update.message.reply_text(
        "👋 *Bem-vindo à Certifica Já Brasil*\n\n"
        "📚 Cursos e certificados reconhecidos pelo MEC\n"
        "⏰ Atendimento 24h\n\n"
        "Escolha uma opção:",
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
        texto = montar_lista("📘 *Ensino Médio*", MEDIO)
    elif query.data == "tecnico":
        texto = montar_lista("🛠 *Cursos Técnicos*", TECNICO)
    elif query.data == "graduacao":
        texto = montar_lista("🎓 *Graduação*", GRAD)
    elif query.data == "pos":
        texto = montar_lista("📚 *Pós-graduação*", POS)
    elif query.data == "outro":
        context.user_data["etapa"] = "curso"
        await query.edit_message_text(
            "📌 *Informe o nome do curso que você procura:*",
            parse_mode="Markdown"
        )
        return
    elif query.data == "voltar":
        await start(query, context)
        return
    else:
        texto = "Opção inválida."

    await query.edit_message_text(
        texto,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❓ Não encontrei meu curso", callback_data="outro")],
            [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
        ])
    )

# =========================
# FUNÇÃO AUXILIAR MONTAR LISTA
# =========================
def montar_lista(titulo, lista):
    texto = f"{titulo}\n\n"
    for item in lista:
        texto += f"• {item}\n"
    texto += "\n💬 Atendimento exclusivo via Telegram"
    return texto

# =========================
# FUNÇÃO CAPTURA TEXTO
# =========================
async def capturar_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hora_atual = datetime.now().hour
    etapa = context.user_data.get("etapa")
    texto_usuario = update.message.text
    usuario = update.message.from_user

    # =======================
    # Resposta fora do horário
    # =======================
    if hora_atual < ATENDIMENTO_INICIO or hora_atual >= ATENDIMENTO_FIM:
        await update.message.reply_text(
            "⏰ Olá! Estamos fora do horário comercial (08:00 - 22:00).\n"
            "Mas não se preocupe, seus dados foram registrados e você será atendido em breve!"
        )

    # =======================
    # IA básica para dúvidas
    # =======================
    respostas_ia = {
        "como funciona": "📄 Você escolhe o curso desejado e um consultor irá te orientar pelo Telegram.",
        "preço": "💰 Os valores são sob consulta. Informe seu curso que enviamos o orçamento.",
        "duração": "⏱ Depende do curso, alguns têm certificado imediato e outros têm duração de semanas.",
        "certificado": "📄 Todos os certificados são reconhecidos pelo MEC e válidos em todo o Brasil."
    }

    # verifica se mensagem do usuário contém alguma dúvida
    for chave, resposta in respostas_ia.items():
        if chave.lower() in texto_usuario.lower():
            await update.message.reply_text(resposta)
            return

    # =======================
    # Captura lead normal
    # =======================
    if etapa == "curso":
        context.user_data["curso"] = texto_usuario
        context.user_data["etapa"] = "nome"
        await update.message.reply_text("✍️ Agora informe seu *nome completo*:", parse_mode="Markdown")
        return

    elif etapa == "nome":
        nome = texto_usuario
        curso = context.user_data.get("curso")
        context.user_data.clear()

        lead = f"Nome: {nome} | Curso: {curso} | Telegram: @{usuario.username} | ID: {usuario.id}\n"
        with open(LEADS_FILE, "a", encoding="utf-8") as f:
            f.write(lead)

        # Notifica admin
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "📥 *NOVO LEAD*\n\n"
                f"👤 Nome: {nome}\n"
                f"📚 Curso: {curso}\n"
                f"🔗 Usuário: @{usuario.username}\n"
                f"🆔 ID: {usuario.id}"
            ),
            parse_mode="Markdown"
        )

        await update.message.reply_text(
            "✅ *Recebido com sucesso!*\n\n"
            "Um consultor entrará em contato com você pelo Telegram.\n"
            "⏰ Atendimento 24h",
            parse_mode="Markdown"
        )
        return

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_texto))

    print("🤖 Bot rodando 24h com captura de leads e IA básica")
    app.run_polling()

if __name__ == "__main__":
    main()
