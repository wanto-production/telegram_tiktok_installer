from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class Chatbot():
    def __init__(self,bot_token):
        self.bot_token = bot_token

    async def start(self,update:Update, context:CallbackContext):
        await update.message.reply_text('hallo selamat datang di @free_downloader_tiktok_bot\n\ndengan bot ini anda bisa mengunduh video tiktok tanpa wm secara gratis!,dengan cara command:\n\n/d <link>')

    async def echo(self,update:Update,context:CallbackContext):
        await update.message.reply_text("untuk mendownload silahkan ketik command:\n\n /d <link>")

    async def install_vid(self,update:Update,context:CallbackContext):
        if len(context.args[0]) == 0:
            await update.message.reply_text("gagal mengambil input, sikahkan ulang")
            return

        link = context.args[0]

        if not any(protocol in link for protocol in ["http", "https"]):
            await update.message.reply_text("link salah!, harus berformat http/https")
        else:
            res = requests.get('https://tiktok-download-without-watermark.p.rapidapi.com/analysis', 
            params={
                'url':link,
                'hd':'0'
           },
           headers={
                'x-rapidapi-key':os.getenv('RAPID_APIKEY'),
                'x-rapidapi-host': 'tiktok-download-without-watermark.p.rapidapi.com'
           })

            if res.status_code == 200:
                data = res.json()
                video_url = data.get('data', {}).get('play', '')

                if video_url:
                    # Kirim video ke chat Telegram
                    await update.message.reply_video(video_url, caption="di unduh menggunakan:\n@free_downloader_tiktok_bot")
                else:
                    await update.message.reply_text("Video tidak di kenali!, gagal generate")
            else:
                await update.message.reply_text(f"gagal download karena: {data.message}")

    def main(self):
        app = Application.builder().token(self.bot_token).pool_timeout(30).build()

        app.add_handler(CommandHandler('start',self.start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,self.echo))
        app.add_handler(CommandHandler('d',self.install_vid))

        app.run_polling()

if __name__ == '__main__':
    Chatbot(
        os.getenv('TELEGRAM_KEY')
    ).main()