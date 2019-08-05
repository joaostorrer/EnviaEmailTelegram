import email
import imaplib
import telebot
import time
import getpass

#De quanto em quanto tempo verifica os emails
minutos = 1

#Para ver o token, basta abrir um conversa com o @BotFather e clicar em /editBots
bot_token = 'token_do_bot'
bot = telebot.TeleBot(bot_token)

#Para pegar o id da conversa acessar pelo navegador: https://api.telegram.org/<token>/getUpdates
#Informar os ids na lista abaixo
id = []

EMAIL = 'joao@tecnoage.com.br'
PASSWORD = ''
SERVER = 'mail.tecnoage.com.br'

def getEmail():
    body = []
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
	
	#Apenas e-mails não visualizados, com remetente informatica@policlinicacapaoraso e assunto 'Alerta'
	#Após verificar os emails, marca como visualizado
    status, data = mail.search(None, '(FROM "informatica@policlinicacapaoraso.com.br" SUBJECT "Alerta" UNSEEN)')
    mail_ids = []

    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                mail_content = message.get_payload()
                body.append(mail_content)

    return body


def enviaMsgTelegram(msg):
	for ids in id:
		bot.send_message(ids,msg)

if __name__ == "__main__":
    PASSWORD = getpass.getpass(prompt='Informe a senha para o email joao@tecnoage.com.br: ')
    while True:
        for alerta in getEmail():
            enviaMsgTelegram(alerta)
        time.sleep(60*minutos)