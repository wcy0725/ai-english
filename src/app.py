import json
import glob
import streamlit as st


def load_dictionaries() -> dict[str, dict]:
    """扫描 data/*.json，返回 {词典名: 词典数据}"""
    dicts = {}
    for path in sorted(glob.glob("data/*.json")):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        dicts[data["name"]] = data
    return dicts


def init_session_state(words: list[dict]):
    """初始化会话状态"""
    if "known" not in st.session_state:
        st.session_state.known = set()
    if "unknown" not in st.session_state:
        st.session_state.unknown = set()
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = {"correct": 0, "total": 0}


def main():
    st.set_page_config(page_title="AI 英语单词", page_icon="📖", layout="wide")

    dictionaries = load_dictionaries()
    if not dictionaries:
        st.error("未找到词典数据，请在 data/ 目录下放置 .json 文件")
        return

    # 侧边栏
    with st.sidebar:
        dict_name = st.selectbox("选择词典", list(dictionaries.keys()))
        mode = st.radio("学习模式", ["闪卡", "列表", "测验"])

        dict_data = dictionaries[dict_name]
        words = dict_data["words"]

        # 词典切换时清除模式相关状态
        if st.session_state.get("current_dict") != dict_name:
            for key in ["fc_order", "fc_was_shuffle", "fc_flipped", "current_index",
                         "quiz_words", "quiz_index", "quiz_score", "quiz_answered",
                         "quiz_num", "quiz_correct"]:
                st.session_state.pop(key, None)
            # 清除 quiz_options_* 缓存
            keys_to_delete = [k for k in st.session_state if k.startswith("quiz_options_")]
            for k in keys_to_delete:
                del st.session_state[k]
            st.session_state.known = set()
            st.session_state.unknown = set()
            st.session_state.current_dict = dict_name

        init_session_state(words)

        # 学习统计
        st.divider()
        st.subheader("学习统计")
        total = len(words)
        known = len(st.session_state.known)
        unknown = len(st.session_state.unknown)
        st.write(f"✅ 已掌握: {known}/{total}")
        st.write(f"❌ 未掌握: {unknown}/{total}")
        st.write(f"📝 未学习: {total - known - unknown}/{total}")

    # 模式路由
    if mode == "闪卡":
        try:
            from flashcard import render_flashcard
            render_flashcard(words)
        except ImportError:
            st.info("闪卡模式即将上线，敬请期待！")
    elif mode == "列表":
        try:
            from word_list import render_word_list
            render_word_list(words)
        except ImportError:
            st.info("列表模式即将上线，敬请期待！")
    elif mode == "测验":
        try:
            from quiz import render_quiz
            render_quiz(words)
        except ImportError:
            st.info("测验模式即将上线，敬请期待！")


if __name__ == "__main__":
    main()
