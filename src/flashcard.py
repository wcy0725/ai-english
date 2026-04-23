import streamlit as st
import random


def render_flashcard(words: list[dict]):
    """渲染闪卡模式"""
    total = len(words)

    # 侧边栏选项
    with st.sidebar:
        st.divider()
        shuffle = st.checkbox("随机浏览", value=True)

    # 初始化/重置浏览顺序
    if "fc_order" not in st.session_state or shuffle != st.session_state.get("fc_was_shuffle"):
        st.session_state.fc_order = list(range(total))
        if shuffle:
            random.shuffle(st.session_state.fc_order)
        st.session_state.fc_was_shuffle = shuffle
        st.session_state.current_index = 0

    if "fc_flipped" not in st.session_state:
        st.session_state.fc_flipped = False

    order_len = len(st.session_state.fc_order)
    idx = st.session_state.current_index
    if idx >= order_len:
        unknown_words = st.session_state.unknown
        if not unknown_words:
            st.success("🎉 恭喜！你已学完所有单词！")
            if st.button("重新开始"):
                st.session_state.current_index = 0
                st.session_state.fc_order = list(range(total))
                if shuffle:
                    random.shuffle(st.session_state.fc_order)
                st.session_state.fc_flipped = False
                st.rerun()
        else:
            st.warning(f"还有 {len(unknown_words)} 个未掌握的单词，继续学习吧！")
            if st.button("重学未掌握"):
                # 只保留未掌握的词
                unknown_indices = [i for i, w in enumerate(words) if w["word"] in unknown_words]
                if shuffle:
                    random.shuffle(unknown_indices)
                st.session_state.fc_order = unknown_indices
                st.session_state.current_index = 0
                st.session_state.fc_flipped = False
                st.rerun()
        return

    word_idx = st.session_state.fc_order[idx]
    word = words[word_idx]

    # 进度条（基于当前学习批次）
    st.progress((idx + 1) / order_len, text=f"进度: {idx + 1}/{order_len}")

    # 卡片
    st.markdown(f"<h1 style='text-align:center'>{word['word']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;font-size:1.2em;color:gray'>{word['phonetic']}  |  出现 {word['frequency']} 次</p>", unsafe_allow_html=True)

    # 翻转按钮
    if not st.session_state.fc_flipped:
        if st.button("翻转", use_container_width=True):
            st.session_state.fc_flipped = True
            st.rerun()
    else:
        # 显示详情
        st.markdown(f"**词性:** {word['pos']}")
        st.markdown(f"**释义:** {word['meaning']}")
        st.markdown(f"**出现次数:** {word['frequency']} 次")
        st.divider()
        st.markdown(f"📝 **例句:** {word['example_en']}")
        st.markdown(f"📝 **翻译:** {word['example_zh']}")

        # 认识 / 不认识
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ 认识", use_container_width=True):
                st.session_state.known.add(word["word"])
                st.session_state.unknown.discard(word["word"])
                _next_word()
        with col2:
            if st.button("❌ 不认识", use_container_width=True):
                st.session_state.unknown.add(word["word"])
                st.session_state.known.discard(word["word"])
                _next_word()


def _next_word():
    st.session_state.current_index += 1
    st.session_state.fc_flipped = False
    st.rerun()
