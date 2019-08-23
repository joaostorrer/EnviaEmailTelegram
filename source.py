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

#Para pegar o id da conversa acessar pelo navegador: https://api.telegram.org/bot<token>/getUpdates
#Informar os ids na lista abaixo
id = []

#Informar o e-mail, senha (pode informar pelo getpass também) e SERVER (GMail: imap.gmail.com)
EMAIL = ''
PASSWORD = ''
SERVER = ''

def getEmail():
    body = []
    mail = imaplib.IMAP4_SSL(SERVER)

    try:
        mail.login(EMAIL, PASSWORD)
    except Exception as e:
        print('Ocorreu um erro ao logar no e-mail:')
        print(e)
    else:
        mail.select('inbox')

        #Apenas e-mails não visualizados, com remetente email_desejado@dominio.com e assunto 'Alerta'
        #Após verificar os emails, marca como visualizado
        status, data = mail.search(None, '(FROM "email_desejado@dominio.com" SUBJECT "Alerta" UNSEEN)')
        mail_ids = []

        for block in data:
            mail_ids += block.split()

        for i in mail_ids:
            try:
                status, data = mail.fetch(i, '(RFC822)')
            except Exception as e:
                print('Erro ao buscar informações do e-mail:')
                print(e)
            else:
                for response_part in data:
                    if isinstance(response_part, tuple):
                        message = email.message_from_bytes(response_part[1])
                        if message.is_multipart():
                            mail_content = ''
                            for part in message.get_payload():
                                if part.get_content_type() == 'text/plain':
                                    mail_content += part.get_payload()
                        else:
                            mail_content = message.get_payload()
                        body.append(mail_content)

        return body


def enviaMsgTelegram(msg):
    for ids in id:
        try:
            bot.send_message(ids,msg)
        except Exception as e:
            print('Erro ao enviar mensagem ao Telegram!')
            print(e)

if __name__ == "__main__":
    PASSWORD = getpass.getpass(prompt='Informe a senha para o email: ')
    while True:
        for alerta in getEmail():
            enviaMsgTelegram(alerta)
        time.sleep(60*minutos)