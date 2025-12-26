import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import os

# 1. 页面配置
st.set_page_config(page_title="KOLB 学习风格深度测评", layout="centered")

# 科技风样式
st.markdown("""
    <style>
    .main { background-color: #0F172A; }
    div.stButton > button { width: 100%; background-color: #38BDF8; color: #0F172A; font-weight: bold; height: 3.5rem; border-radius: 12px; }
    .stExpander { border: 1px solid #38BDF8 !important; border-radius: 10px; background-color: #1E293B !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 初始化状态
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.scores = {"CE": 0, "RO": 0, "AC": 0, "AE": 0}
    st.session_state.submitted = False

questions = [
    ["我凭感受学习", "我凭观察学习", "我凭思考学习", "我凭行动学习"],
    ["我喜欢感受事物", "我喜欢四处观察", "我喜欢分析拆解", "我喜欢尝试做做看"],
    ["我倾向于直觉", "我倾向于观望", "我倾向于逻辑", "我倾向于务实"],
    ["我学习时全情投入", "我学习时深思熟虑", "我学习时理智客观", "我学习时充满动力"],
    ["我关注当下", "我关注过程", "我关注理论", "我关注结果"],
    ["我喜欢具体的体验", "我喜欢观察他人", "我喜欢抽象的概念", "我喜欢动手实验"],
    ["我容易受情感驱动", "我容易受观察驱动", "我容易受逻辑驱动", "我容易受任务驱动"],
    ["我乐于接触人", "我乐于思考意义", "我乐于理解原理", "我乐于解决问题"],
    ["对我而言,感受最重要", "对我而言,观察最重要", "对我而言,思考最重要", "对我而言,实践最重要"],
    ["我重视直观感受", "我重视多角度看", "我重视客观分析", "我重视实际效果"],
    ["我是一个感性的人", "我是一个静观的人", "我是一个理性的人", "我是一个积极的人"],
    ["我接受当下的环境", "我评估周围的环境", "我分析周围的环境", "我改变周围的环境"]
]

# 3. 答题逻辑
if st.session_state.current_q < len(questions):
    st.title("🚀 KOLB 学习风格测评")
    st.write(f"进度: {st.session_state.current_q + 1} / 12")
    st.progress((st.session_state.current_q + 1) / len(questions))
    
    q_idx = st.session_state.current_q
    st.info("4分(最符合) ↔ 1分(最不符合)。组内数字不可重复。")

    v1 = st.select_slider(f"A: {questions[q_idx][0]}", options=[1, 2, 3, 4], key=f"q{q_idx}a")
    v2 = st.select_slider(f"B: {questions[q_idx][1]}", options=[1, 2, 3, 4], key=f"q{q_idx}b")
    v3 = st.select_slider(f"C: {questions[q_idx][2]}", options=[1, 2, 3, 4], key=f"q{q_idx}c")
    v4 = st.select_slider(f"D: {questions[q_idx][3]}", options=[1, 2, 3, 4], key=f"q{q_idx}d")

    if st.button("下一步"):
        if len(set([v1, v2, v3, v4])) < 4:
            st.error("❌ 同一组内的分数不能重复！")
        else:
            st.session_state.scores["CE"] += v1; st.session_state.scores["RO"] += v2
            st.session_state.scores["AC"] += v3; st.session_state.scores["AE"] += v4
            st.session_state.current_q += 1
            st.rerun()

# 4. 提交信息
elif not st.session_state.submitted:
    st.title("✅ 请登记个人信息")
    u_name = st.text_input("学生姓名")
    u_id = st.text_input("学号")
    
    if st.button("提交数据并生成报告"):
        if u_name and u_id:
            # 判定风格
            y_v = st.session_state.scores["AC"] - st.session_state.scores["CE"]
            x_v = st.session_state.scores["AE"] - st.session_state.scores["RO"]
            if y_v >= 0: style = "聚合型" if x_v >= 0 else "同化型"
            else: style = "适应型" if x_v >= 0 else "发散型"

            # 存入本地CSV
            res = {"时间": datetime.now(), "姓名": u_name, "学号": u_id, "结论": style, "X": x_v, "Y": y_v}
            df = pd.DataFrame([res])
            df.to_csv('results.csv', mode='a', index=False, header=not os.path.exists('results.csv'), encoding='utf-8-sig')
            
            st.session_state.submitted = True
            st.rerun()
        else:
            st.warning("请输入完整的姓名和学号")

# 5. 详细报告页
else:
    st.header("🎯 测评报告详细解析")
    y_v = st.session_state.scores["AC"] - st.session_state.scores["CE"]
    x_v = st.session_state.scores["AE"] - st.session_state.scores["RO"]
    
    # 绘制 Plotly 坐标
    fig = go.Figure()
    for t, x, y in [("聚合型",20,20), ("同化型",-20,20), ("发散型",-20,-20), ("适应型",20,-20)]:
        fig.add_annotation(x=x, y=y, text=t, showarrow=False, font=dict(color="#38BDF8", size=16))
    fig.add_hline(y=0, line_color="#334155"); fig.add_vline(x=0, line_color="#334155")
    fig.add_trace(go.Scatter(x=[x_v], y=[y_v], mode='markers', marker=dict(size=25, color='#F43F5E', line=dict(width=3, color='white'))))
    fig.update_layout(template="plotly_dark", xaxis=dict(range=[-40,40]), yaxis=dict(range=[-40,40]), width=450, height=450, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    if y_v >= 0: res_key = "聚合型" if x_v >= 0 else "同化型"
    else: res_key = "适应型" if x_v >= 0 else "发散型"

    st.markdown(f"<h2 style='text-align: center; color: #38BDF8;'>您的风格是：{res_key}</h2>", unsafe_allow_html=True)

    # 详细分析块
    with st.expander("🔍 深度风格特征分析 (点击展开)", expanded=True):
        analyses = {
            "聚合型": "您是典型的技术专家与逻辑执行者。具备极强的演绎推理能力，擅长解决具体的技术难题而非复杂的人际情感。在面对挑战时，您能迅速锁定最优解。",
            "同化型": "您是深邃的理论家与架构师。具备极强的归纳能力，在意理论的严密性。您习惯行动前详尽观察，倾向于构建系统化的知识体系。",
            "发散型": "您是极具魅力的创意家与感知者。拥有敏锐洞察力，擅长从多角度审视事物。您的动力源于感性体验，在创意策划中总是能提供独特视角。",
            "适应型": "您是天生的探险家与实干派。相信实践出真知，具备极强的环境适应力。即便在信息不全时，也敢于凭借直觉采取行动。"
        }
        st.write(analyses[res_key])

    with st.expander("🎓 针对大学生的学习建议"):
        pro_advice = {
            "聚合型": "建议多参与科研竞赛，发挥逻辑优势；但在小组合作中要学习倾听感性反馈，提升协作温度。",
            "同化型": "图书馆是您的天堂，但要警惕纸上谈兵。多参加社会实践，看理论如何在现实中转化为成果。",
            "发散型": "创意是您的武器，但执行是短板。尝试用思维导图系统化灵感，设定明确的DDL防止拖延。",
            "适应型": "实践能力极强，但不要忽略专业课理论。尝试在动手前阅读5分钟原理，会让您的行动更高效。"
        }
        st.write(pro_advice[res_key])

    with st.expander("📖 科学原理：Kolb 学习循环"):
        st.write("Kolb 认为学习是一个循环：从**具体经验**出发，经过**反思观察**，形成**抽象概括**，最后进行**主动实践**。")
        st.write("每个人在这个循环中都有自己的'舒适区'。了解自己的风格，是为了让我们学会在不擅长的象限中练习，从而成为全能学习者。")

    if st.button("重新开始 (新用户)"):
        st.session_state.current_q = 0; st.session_state.scores = {"CE": 0, "RO": 0, "AC": 0, "AE": 0}
        st.session_state.submitted = False; st.rerun()