# AI English - 单词记忆应用

基于 Streamlit 的英语单词记忆应用，支持闪卡、列表浏览、测验三种学习模式。

## 功能

- **闪卡模式** — 逐词展示，翻转查看释义和例句，标记认识/不认识
- **列表模式** — 表格浏览所有单词，支持搜索过滤和按频次排序
- **测验模式** — 四选一选择题，实时统计正确率
- **多词典支持** — 自动扫描 `data/` 目录下的 JSON 词典，侧边栏切换
- **学习统计** — 会话内追踪已掌握/未掌握/未学习数量

## 安装与运行

需要 [uv](https://docs.astral.sh/uv/) 管理环境。

```bash
# 安装依赖
uv sync

# 启动应用
uv run streamlit run src/app.py
```

## 项目结构

```
ai-english/
├── pyproject.toml         # 项目配置与依赖
├── src/
│   ├── app.py             # 主入口：侧边栏 + 模式路由
│   ├── flashcard.py       # 闪卡模式
│   ├── word_list.py       # 列表模式
│   └── quiz.py            # 测验模式
├── data/
│   └── 228words.json      # 高考高频词汇词典
├── scripts/
│   ├── build_dict.py      # txt → json 转换脚本
│   └── split_dict.py      # 按数量均分词典
└── docs/
    └── 228words.txt       # 原始词汇数据
```

## 工具脚本

### 从 txt 生成词典

```bash
uv run python scripts/build_dict.py
```

### 均分词典

按数量将词典分为指定份数（先按 frequency 排序）：

```bash
uv run python scripts/split_dict.py data/228words.json 3
```

输出 `data/228words_1.json`、`data/228words_2.json`、`data/228words_3.json`，每份约 76 个单词，description 中标注 frequency 范围。

## 词典 JSON 格式

```json
{
  "name": "词典名称",
  "description": "词典描述",
  "words": [
    {
      "id": 1,
      "word": "mature",
      "frequency": 25,
      "phonetic": "/məˈtʃʊər/",
      "pos": "a.",
      "meaning": "成熟的；深思熟虑的",
      "example_en": "She is mature for her age.",
      "example_zh": "以她的年龄来说，她很成熟。"
    }
  ]
}
```

添加新词典只需将 JSON 文件放入 `data/` 目录，应用会自动识别。
