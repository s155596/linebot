from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('SMqDx91Xf8+Gklga1y63YzCKGnt74ASDB7Uufucotd2AFCDTVD2jUDFsBHS0XYEjvDDBIdiEOwnNcb0vY6tjtCwTFYMyz0UVl1isJdM8m/pkC8snD8xkUDxE078CTfYeIxoJMjndDW3uD0W8neGZwgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8bacf185c049440035d39b8c9f9c69fe')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()