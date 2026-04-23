import streamlit as st


def render_word_list(words: list[dict]):
    """渲染列表模式"""
    # 搜索与排序
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("搜索单词", placeholder="输入单词或释义...")
    with col2:
        sort_by = st.selectbox("排序", ["默认顺序", "出现频次↑", "出现频次↓"])

    # 过滤
    filtered = words
    if search:
        search_lower = search.lower()
        filtered = [
            w for w in words
            if search_lower in w["word"].lower() or search_lower in w["meaning"]
        ]

    # 排序
    if sort_by == "出现频次↑":
        filtered = sorted(filtered, key=lambda w: w["frequency"])
    elif sort_by == "出现频次↓":
        filtered = sorted(filtered, key=lambda w: w["frequency"], reverse=True)

    st.write(f"共 {len(filtered)} 个单词")

    # 展示
    for w in filtered:
        with st.expander(f"**{w['word']}** {w['phonetic']}  —  {w['pos']} {w['meaning']}  |  出现 {w['frequency']} 次"):
            st.markdown(f"出现频次: **{w['frequency']}次**")
            st.markdown(f"📝 **例句:** {w['example_en']}")
            st.markdown(f"📝 **翻译:** {w['example_zh']}")
