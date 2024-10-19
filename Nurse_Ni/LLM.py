#Note: The openai-python library support for Azure OpenAI is in preview.
      #Note: This code sample requires OpenAI Python library version 1.0.0 or higher.

import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
from openai import AzureOpenAI
from pydub import AudioSegment

# 將音頻文件轉換為WAV格式
def aac_to_mp3(aac_file, mp3_file):
    # Load the AAC file
    audio = AudioSegment.from_file(aac_file, format="aac")

    # Export the audio as MP3
    audio.export(mp3_file, format="mp3")


# 使用Azure語音服務進行語音轉文字
def speech_to_text(audio_path):    
    client = AzureOpenAI(
        api_key='acac56ce0a894d04afdf3ec32a1c1d3b',  
        api_version="2024-02-01",
        azure_endpoint ='https://whisper-moke-20240523.openai.azure.com/'
    )
    
    deployment_id = "whisper_model" #This will correspond to the custom name you chose for your deployment when you deployed a model."
    audio_test_file = audio_path
    
    result = client.audio.transcriptions.create(
        file=open(audio_test_file, "rb"),            
        model=deployment_id
    ) 
    return result 

# 使用Azure OpenAI進行文本處理
def process_text_with_azure_llm(text):
    client = AzureOpenAI(
        azure_endpoint = "https://azure-openai-20240521.openai.azure.com/", 
        api_key="ace19f5375874341b4d913e051f1b389",
        api_version="2024-02-01"
    )

    # 醫囑內容的識別關鍵字
    medical_keywords = ["看病","醫囑", "病人", "診斷", "治療", "看醫生", "醫生", "病歷"]

    # 判斷是否為醫囑內容
    if any(keyword in text for keyword in medical_keywords):
        message_text = [
            {"role": "system", "content": '''
                您現在是擁有醫學背景的助理，專長是醫囑紀錄及整理，會將使用者輸入的文字生成表格，並附上相關參考資料和連結，以及過往紀錄位。若沒有相關資訊，則不顯示該欄位。請確保每個項目字數限制在200字內，至少包含以下內容：
                1. 醫囑紀錄時間
                2. 病人基本信息：病人姓名、性別、年齡、診斷
                3. 治療目標：說明治療後的方向
                4. 治療方案：詳細的治療步驟和說明、每日藥物劑量和服用時間、飲食和生活方式建議、運動建議、定期檢查和追蹤方案
                5. 醫生資訊：醫生姓名和職稱
                6. 備註：任何其他需要注意的事項
                7. 參考資料：從網路找相關文章網站連結

                文字排列方式請參照如下:
                【2024/5/18(五) 醫囑紀錄】
               
                ・姓名：張三
                ・年齡：55歲
                ・診斷方向：高血壓
                ・治療目標：
                    控制血壓，降低心血管風險
             
                ・治療方案：
                    1. 每日服用某藥5毫克，每日一次，早餐後服用
                    2. 每日測量血壓，並記錄在血壓日誌中 
                    3. 飲食限制鹽分攝入，多攝取蔬菜水果
                    4. 每週至少進行30分鐘有氧運動，如散步或游泳
                    5. 定期追蹤血壓，據情況調整治療方案
             
                ・醫生資訊：王醫生，內科醫生
                ・備註：病人需定期復診，隨時監控血壓情況
                ・參考資料： 
                    1. 高血壓治療指南2024：
                    https://www.example.com/hypertension-guidelines 
                    2. 飲食控制高血壓：
                    https://www.example.com/dietary-management
            '''},
            {"role":"user","content":text}
        ]
    else:
        message_text = [
            {"role": "system", "content": "你的名字叫護理小妮，是一個專業護理師，擅長回答各類問題的助手。請根據以下內容生成合適的回應。"},
            {"role": "user", "content": text}
        ]

    completion = client.chat.completions.create(
        model="GPT4o-Ni-20240523",  
        messages=message_text,
        temperature=0.7,
        max_tokens=1500,
        top_p=0.90,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    
    return completion.choices[0].message.content

def generate_summary(text):
    client = AzureOpenAI(
        azure_endpoint = "https://azure-openai-20240521.openai.azure.com/",
        api_key="ace19f5375874341b4d913e051f1b389",
        api_version="2024-02-01"
    )
    message_text = [
        {"role": "system", "content": "你是一個擅長總結的助手。請將以下內容總結成100字內的結論。"},
        {"role": "user", "content": text}
    ]
    
    completion = client.chat.completions.create(
        model="GPT4o-Ni-20240523",
        messages=message_text,
        temperature=0.7,
        max_tokens=1500,
        top_p=0.90,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":
    audio_path ='./test.mp3'
    aac_to_mp3('./test.aac',audio_path)

    text=speech_to_text(audio_path)
    print(speech_to_text(audio_path))

