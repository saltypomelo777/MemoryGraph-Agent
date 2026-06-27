# 这段话大约 40 个 Token
base_sentence = "这是一个用于测试大模型长文本 KV Cache 命中率的背景知识文本。我们需要通过不断重复这段话，将系统的上下文负载强行撑到 60,000 Tokens 以上，以观察底层推理引擎的性能表现。\n"

# 重复它 2000 次，大概就能生成将近 8 万 Token 的长文本
giant_text = base_sentence * 2000

# 写入到一个 txt 文件里
with open("test_long_context.txt", "w", encoding="utf-8") as f:
    f.write(giant_text)

print("✅ 成功！去打开 test_long_context.txt 吧！")