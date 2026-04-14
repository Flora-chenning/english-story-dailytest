import os
import json
from anthropic import Anthropic

# 从 GitHub Secrets 读取 API Key
api_key = os.environ.get("CLAUDE_API_KEY")
client = Anthropic(api_key=api_key)

# 提示词（可自行修改难度、字数）
prompt = """请生成一篇英文短故事，用于英语学习网站“每日一篇”。

要求：
- 难度：L2（初级偏上，适合有基础的学习者）
- 类型：从日常生活、幽默、小冒险、童话、科幻中随机选一个
- 字数：200-250词
- 故事结构：开头 → 小冲突或趣事 → 温暖或有趣结尾
- 输出格式：纯 JSON，不要有其他文字，如下：
{
  "title": "故事标题",
  "content": "完整英文故事正文...",
  "type": "daily",
  "difficulty": "L2",
  "wordCount": 数字
}

请直接输出 JSON。"""

response = client.messages.create(
    model="claude-3-haiku-20240307",  # 便宜，够用
    max_tokens=800,
    temperature=0.7,
    messages=[{"role": "user", "content": prompt}]
)

# 解析 Claude 返回的 JSON
text = response.content[0].text
if text.startswith("```json"):
    text = text[7:-3]  # 去掉 markdown 标记
story = json.loads(text)

# 精确计算字数（英文单词数）
story["wordCount"] = len(story["content"].split())

# 保存到文件
with open("story_of_today.json", "w", encoding="utf-8") as f:
    json.dump(story, f, ensure_ascii=False, indent=2)

print("✅ 今日故事已生成并保存")
