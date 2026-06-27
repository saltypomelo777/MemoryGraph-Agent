import os
import time
# ⚠️ 注意：根据你实际使用的模型大厂 SDK（通常是 openai），确保已安装
try:
    from openai import OpenAI
except ImportError:
    print("❌ 请先在终端运行: pip install openai")
    exit()

# =====================================================================
# 🛠️ 核心配置（请根据你项目的 .env 或实际配置进行修改）
# =====================================================================
# =====================================================================
# 🛠️ 核心配置（已根据你的截图完美对齐）
# =====================================================================
# 1. 填入你截图中那一长串 sk- 开头的真实密钥
API_KEY = "sk-kbdunsmezysyaihvnmxbcmxnirkubyypddkxrxcadfxaksuk"

# 2. 填入硅基流动的官方标准 OpenAI 兼容接口地址
BASE_URL = "https://api.siliconflow.cn/v1"

# 3. 填入硅基流动里最常用的标准模型名称（这里用 V3 作为压测模型）
MODEL_NAME = "deepseek-ai/DeepSeek-V3"
# 初始化客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

CONTEXT_FILE = "test_long_context.txt"

print("==================================================")
print("📂 正在读取超长测试文本...")
print("==================================================")

# 确保测试文本文件存在，不存在则自动生成一个约 4.2 万字的《三体》假数据用于测试
if not os.path.exists(CONTEXT_FILE):
    print(f"⚠️ 未找到 {CONTEXT_FILE}，正在自动生成 42500 字符的测试文本...")
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        f.write("【物理学不存在了】汪淼觉得眼前的倒计时正在疯狂闪烁。杨冬自杀了，丁仪在痛苦中抽烟。常伟思将军面色凝重地看着他...\n" * 900)

# 读取文件
with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
    long_context = f.read()

print(f"✅ 文本读取成功，大约包含 {len(long_context)} 个字符。")
print("🚀 开始进行 A 侧 [静态基准压测]...")
print("==================================================\n")

# 构造纯净的 Prompt：将超长文本死死固定在 System Prompt 中（前缀隔离机制的原型）
messages = [
    {
        "role": "system", 
        "content": f"你是一个精通《三体》小说的严谨助手。请完全基于以下给出的超长上下文回答问题，不得瞎编：\n\n{long_context}"
    },
    {
        "role": "user", 
        "content": "常伟思在将会上面对科学家自杀时，对汪淼说了什么核心的话？"
    }
]

# 连续发起 3 轮请求，观察 KV Cache 的威力
for turn in range(1, 4):
    print(f"🔄 [第 {turn} 轮请求] 正在发送至大模型...")
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.0  # 压测时务必将随机性设为 0，保证前缀和输出的高度稳定
        )
        
        elapsed_time = time.time() - start_time
        usage = response.usage
        
        # 提取各个云厂商通用的缓存统计字段（兼容 OpenAI/DeepSeek 标准）
        prompt_tokens = usage.prompt_tokens
        hit_tokens = 0
        
        # 兼容 DeepSeek / OpenAI 的缓存详情读取
        if hasattr(usage, 'prompt_tokens_details') and usage.prompt_tokens_details is not None:
            hit_tokens = getattr(usage.prompt_tokens_details, 'cached_tokens', 0)
        elif hasattr(usage, 'prompt_cache_hit_tokens'): # 部分旧版 SDK 的兼容
            hit_tokens = usage.prompt_cache_hit_tokens

        # 计算命中率
        hit_rate = (hit_tokens / prompt_tokens * 100) if prompt_tokens > 0 else 0.0
        
        print(f"⏱️ 本轮单次交互总耗时: {elapsed_time:.2f} 秒")
        print(f"📊 [KV缓存] 本轮 prompt_tokens={prompt_tokens} | hit_tokens={hit_tokens} | hit_rate={hit_rate:.2f}%")
        
    except Exception as e:
        print(f"❌ 请求失败，可能遭遇了云厂商熔断或网络波动: {e}")
        
    print("-" * 50)

print("\n📊 A 侧静态基准压测全部结束！")
print("💡 提示：请注意看第 2 轮和第 3 轮的 hit_rate 是否瞬间飙升至 98% 以上，耗时是否大幅缩短。")