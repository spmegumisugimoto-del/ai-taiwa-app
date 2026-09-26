from openai import AzureOpenAI
import streamlit as st
import os

azure_endpoint = os.environ["CHATBOT_AZURE_OPENAI_ENDPOINT"] 
api_key = os.environ["CHATBOT_AZURE_OPENAI_API_KEY"]
deployment_name = "gpt-5-mini" # 先ほど作成したモデルのデプロイ名に置き換えてください
api_version = "2024-12-01-preview" # 先ほど作成したモデルの API バージョンに置き換えてください

# Azure OpenAI クライアントを作成  
client = AzureOpenAI(  
    azure_endpoint=azure_endpoint,  
    api_key=api_key,  
    api_version=api_version 
)

# チャットの履歴を保持するためのセッションステートを初期化
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ユーザーからのメッセージに対して応答を生成する関数
def get_response(prompt: str = ""):  
    # ユーザーのメッセージを履歴に追加 
    st.session_state.chat_history.append({"role": "user", "content": prompt})  
    # モデルに送信するメッセージを作成, セキュリティの観点から chat_history オブジェクトは直接渡さない
    system_message = [{"role": "system", "content": "あなたは親切で共感力のあるアシスタントです。明るく博多弁で回答します"}]
    chat_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.chat_history
    ]
    
    response = client.chat.completions.create(  
        model=deployment_name, 
        messages=system_message + chat_messages,
        stream=True
    )
    return response

def add_history(response):
    st.session_state.chat_history.append({"role": "assistant", "content": response}) 


# Streamlit アプリケーションの UI を構築
st.title("AI Taiwa App")

# チャット履歴の表示 
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])
        
# ユーザーの入力を受け取る  
if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        stream = get_response(prompt)
        response = st.write_stream(stream)
        add_history(response)