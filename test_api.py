import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 自动读取 .env 文件中的密钥
load_dotenv()
api_key = os.getenv("SILICONFLOW_API_KEY")

# 2. 初始化客户端（强行指定硅基流动的官方服务器地址）
client = OpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

print("🚀 正在向硅基流动服务器发送思考请求...")

try:
    # 3. 呼叫大模型（这里我们先用极其便宜且聪明的 deepseek-ai/DeepSeek-V3）
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3", 
        messages=[
            {"role": "user", "content": "你好！我是计算机系本科生，请用一句话祝贺我的保研AI项目成功开机！"}
        ],
        stream=False
    )
    
    # 4. 打印大模型吐出来的回答
    print("\n🧠 大脑回应成功：")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"\n❌ 打火失败，报错原因: {e}")