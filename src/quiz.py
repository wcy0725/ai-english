import random
import streamlit as st


def render_quiz(words: list[dict]):
    """渲染测验模式"""
    # 侧边栏选项
    with st.sidebar:
        st.divider()
        num_options = [10, 20, len(words)]
        num_labels = ["10题", "20题", f"全部({len(words)}题)"]
        num_choice = st.selectbox("题目数量", num_labels)
        num_questions = num_options[num_labels.index(num_choice)]

    total_words = len(words)
    if num_questions > total_words:
        num_questions = total_words

    # 初始化测验
    if "quiz_words" not in st.session_state or st.session_state.get("quiz_num") != num_questions:
        st.session_state.quiz_words = random.sample(range(total_words), num_questions)
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = {"correct": 0, "total": 0}
        st.session_state.quiz_answered = False
        st.session_state.quiz_num = num_questions

    q_idx = st.session_state.quiz_index
    score = st.session_state.quiz_score

    # 测验完成
    if q_idx >= num_questions:
        st.success(f"测验完成！得分: {score['correct']}/{score['total']}")
        if st.button("再来一次"):
            # 清除所有 quiz 相关缓存
            keys_to_delete = [k for k in st.session_state if k.startswith("quiz_options_")]
            for k in keys_to_delete:
                del st.session_state[k]
            del st.session_state.quiz_words
            st.rerun()
        return

    # 当前题目
    word = words[st.session_state.quiz_words[q_idx]]
    correct_meaning = word["meaning"]

    # 生成选项（每道题只生成一次，存入 session_state 避免重渲染时打乱顺序）
    if f"quiz_options_{q_idx}" not in st.session_state:
        others = [w for w in words if w["meaning"] != correct_meaning]
        distractors = random.sample(others, min(3, len(others)))
        options = [correct_meaning] + [d["meaning"] for d in distractors]
        random.shuffle(options)
        st.session_state[f"quiz_options_{q_idx}"] = options
    options = st.session_state[f"quiz_options_{q_idx}"]

    # 显示题目
    st.markdown(f"<h2 style='text-align:center'>{word['word']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:gray'>{word['phonetic']}  |  {word['pos']}  |  出现 {word['frequency']} 次</p>", unsafe_allow_html=True)
    st.progress((q_idx + 1) / num_questions, text=f"第 {q_idx + 1}/{num_questions} 题")

    # 选择
    choice = st.radio("选择正确释义:", options, index=None)

    if not st.session_state.quiz_answered:
        if st.button("提交答案", disabled=(choice is None)):
            st.session_state.quiz_answered = True
            score["total"] += 1
            if choice == correct_meaning:
                score["correct"] += 1
                st.session_state.quiz_correct = True
            else:
                st.session_state.quiz_correct = False
                st.session_state.known.discard(word["word"])
            st.rerun()
    else:
        # 显示结果
        if st.session_state.quiz_correct:
            st.success("✅ 回答正确！")
        else:
            st.error(f"❌ 回答错误！正确答案: {correct_meaning}")
            st.markdown(f"📝 **例句:** {word['example_en']}")
            st.markdown(f"📝 **翻译:** {word['example_zh']}")

        if st.button("下一题"):
            st.session_state.quiz_index += 1
            st.session_state.quiz_answered = False
            st.rerun()

    # 分数
    st.divider()
    st.write(f"当前得分: {score['correct']}/{score['total']}")
