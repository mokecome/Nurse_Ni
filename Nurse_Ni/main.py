# -*- coding: utf-8 -*-
"""
Created on Sun May 19 22:13:05 2024

@author: User
"""
import os
from LLM import speech_to_text, aac_to_mp3

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioMessage, FlexSendMessage, AudioSendMessage

from web_crawler import spider
from get_json import get_one_json,add_json

import threading
import time
from LLM import speech_to_text, generate_summary, process_text_with_azure_llm
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk

# 設定你的Channel Access Token
channel_access_token = "2QLWPhwWHlP042/SWl5T9Ggzm0gla1WFI/MhakwTpfkqebE7MkvaeWI6zzhge4uO4h+sk7P7R2Md6+0v1rVxVt/VgASoa5iBsXcfMSoJ6ioMb9nCDcWgapg6O7w+jEgp00Om2eT5UJztpuF3P9JvHAdB04t89/1O/w1cDnyilFU="

# 創建Line Bot API物件
line_bot_api = LineBotApi(channel_access_token)

# 用戶ID，這是你想要發送訊息的用戶
user_id = "Ua6ea0a6dd4cc87b870cfcc3a78b5df11"

# 要發送的訊息
message = TextSendMessage(text="歡迎使用Line Bot！")

# 發送訊息
line_bot_api.push_message(user_id, messages=message)


#Audio message
from linebot.exceptions import InvalidSignatureError


# 設定你的Channel Access Token
app = Flask(__name__)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler('662b00819baa9dedb7e1971e9122c54c')

@app.route("/", methods=['GET'])
def hello():
    return "and suger"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

USER_ID = 'U6ea0a6dd4cc87b870cfcc3a78b5df11'

# def save_message(user_id, message):
#     with open('message_records.txt', 'a+') as f:
#         f.write(f"{user_id}: {message}\n")

# 保存總結到文件
def save_summary(summary):
    with open('message_records.txt', 'a+') as f:
        f.write(f"Summary: {summary}\n")

    
# 讀取文件中的最新消息
def read_latest_message():
    try:
        with open('message_records.txt', 'r') as f:
            lines = f.readlines()
            return lines[-1] if lines else ""
    except FileNotFoundError:
        return ""

def aac_to_mp3(aac_file, mp3_file):
    try:
        audio = AudioSegment.from_file(aac_file, format="aac")
        if audio.channels > 2:  # 如果聲道數量大於2，則轉換為單聲道
            audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)  # 设置采样率
        audio.export(mp3_file, format="mp3")
    except Exception as e:
        print(f"Error converting file: {e}")

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = event.source.user_id
    text = event.message.text

    if "健康新知" in text:
        title_urls, title, img_urls = spider()
        flex_contents = [get_one_json(i[0], i[1], i[2]) for i in zip(title_urls, title, img_urls)]
        flex_message = add_json(flex_contents)
        try:
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text="健康新知",
                    contents=flex_message
                )
            )
        except Exception as e:
            print(f"Error: {e}")
        else:
            response_text = process_text_with_azure_llm(text)
            print(response_text)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_text))
    elif "觀看紀錄" in text:
        all_messages = read_latest_message()
        detailed_info = generate_summary(all_messages)  # 使用 generate_summary 進行總結
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=detailed_info))
    
    elif "名人語音" in text:
        latest_message = read_latest_message()
        
        # Creates an instance of a speech config with specified subscription key and service region.
        speech_key = "05548e76a5a54536bfd1aa9dedd57108"
        service_region = "southeastasia"

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        # Note: the voice setting will not overwrite the voice element in input SSML.
        speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"

        text = latest_message

        # use the default speaker as audio output.
        audio_config = speechsdk.audio.AudioOutputConfig(filename="./file.mp3")
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        # Synthesize the text to speech and wait for it to complete
        result = speech_synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        else:
            print("Speech synthesis failed. Error details: {}".format(result.error_details))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="語音合成失敗"))
            return
        
        # Check if the MP3 file was created
        if not os.path.exists("./file.mp3"):
            print("MP3 file was not generated successfully.")
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="MP3 文件生成失敗"))
            return
        
        # Use FFmpeg to convert MP3 to AAC
        os.system("ffmpeg -y -i ./file.mp3 -c:a aac -b:a 128k ./static/file.aac")
        
        # Check if the AAC file was created
        if not os.path.exists("./static/file.aac"):
            print("Failed to convert MP3 to AAC.")
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="MP3 轉 AAC 失敗"))
            return
        
        # Confirm ngrok URL
        ngrok_url = "https://cb25-150-116-47-93.ngrok-free.app"
        
        # Create and send audio message
        try:
            song = AudioSegment.from_file("./static/file.aac", format="aac")
            audio_message = AudioSendMessage(
                original_content_url=f"{ngrok_url}/static/file.aac",
                duration=len(song)
            )
            line_bot_api.reply_message(event.reply_token, audio_message)
        except Exception as e:
            print(f"Error processing audio file: {e}")
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="處理音檔時出錯"))
    else:
        response_text = process_text_with_azure_llm(text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_text))


@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    user_id = event.source.user_id
    UserSendAudio = line_bot_api.get_message_content(event.message.id)

    path = './test.aac'
    outpath = './test.mp3'
    with open(path, 'wb') as fd:
        for chunk in UserSendAudio.iter_content():
            fd.write(chunk)
    aac_to_mp3(path, outpath)
    text = speech_to_text(outpath).text
    response_text = process_text_with_azure_llm(text)  # 使用 Azure OpenAI 進行文本處理
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_text))
    # save_message(user_id, text)  # 保存消息到文件


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
