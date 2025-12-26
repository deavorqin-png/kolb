import streamlit as st
import plotly.graph_objects as go

# 1. 页面配置
st.set_page_config(page_title="KOLB 学习风格专业测评", layout="centered")

# 科技风样式
st.markdown("""
    <style>
    .main { background-color: #0F172A; }
    div.stButton > button { width: 100%; background-color: #38BDF8; color: #0F172A; font-weight: bold; height: 3.5rem; border-radius: 12px; }
    .stSelectbox label, .stSlider label { color: #38BDF8 !important; font-size: 1.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 初始化数据逻辑
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.scores = {"CE": 0, "RO": 0, "AC": 0, "AE": 0}

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
    st.title("📊 KOLB 学习风格测评")
    st.write(f"进度: {st.session_state.current_q + 1} / 12")
    st.progress((st.session_state.current_q + 1) / len(questions))
    
    q_idx = st.session_state.current_q
    st.info("请分配 1-4 分 (4=最符合, 1=最不符合)，每组数字不可重复。")

    # 手机友好型滑动条
    v1 = st.select_slider(f"选项 A: {questions[q_idx][0]}", options=[1, 2, 3, 4], key=f"q{q_idx}1")
    v2 = st.select_slider(f"选项 B: {questions[q_idx][1]}", options=[1, 2, 3, 4], key=f"q{q_idx}2")
    v3 = st.select_slider(f"选项 C: {questions[q_idx][2]}", options=[1, 2, 3, 4], key=f"q{q_idx}3")
    v4 = st.select_slider(f"选项 D: {questions[q_idx][3]}", options=[1, 2, 3, 4], key=f"q{q_idx}4")

    if st.button("进入下一组"):
        vals = [v1, v2, v3, v4]
        if len(set(vals)) < 4:
            st.error("⚠️ 注意：同一组内的四个分数不能重复，请重新选择。")
        else:
            st.session_state.scores["CE"] += v1
            st.session_state.scores["RO"] += v2
            st.session_state.scores["AC"] += v3
            st.session_state.scores["AE"] += v4
            st.session_state.current_q += 1
            st.rerun()

# 4. 结果与可视化
else:
    st.balloons()
    st.header("🎯 测评分析报告")
    
    y_val = st.session_state.scores["AC"] - st.session_state.scores["CE"]
    x_val = st.session_state.scores["AE"] - st.session_state.scores["RO"]

    # 使用 Plotly 绘制高度交互且不乱码的坐标图
    fig = go.Figure()
    # 背景象限标注
    fig.add_annotation(x=20, y=20, text="聚合型 (Converging)", showarrow=False, font=dict(color="#38BDF8", size=14))
    fig.add_annotation(x=-20, y=20, text="同化型 (Assimilating)", showarrow=False, font=dict(color="#38BDF8", size=14))
    fig.add_annotation(x=-20, y=-20, text="发散型 (Diverging)", showarrow=False, font=dict(color="#38BDF8", size=14))
    fig.add_annotation(x=20, y=-20, text="适应型 (Accommodating)", showarrow=False, font=dict(color="#38BDF8", size=14))
    
    # 绘制坐标轴
    fig.add_hline(y=0, line_color="#94A3B8", line_dash="dash")
    fig.add_vline(x=0, line_color="#94A3B8", line_dash="dash")
    
    # 绘制得分点
    fig.add_trace(go.Scatter(x=[x_val], y=[y_val], mode='markers+text', 
                             marker=dict(size=20, color='#F43F5E', line=dict(width=2, color='white')),
                             text=["您的位置"], textposition="top center"))

    fig.update_layout(
        title="学习风格坐标分布图", template="plotly_dark",
        xaxis=dict(title="主动实践 (AE) ← ↔ → 反思观察 (RO)", range=[-40, 40]),
        yaxis=dict(title="具体经验 (CE) ← ↔ → 抽象概括 (AC)", range=[-40, 40]),
        width=500, height=500, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    # 风格判定与详细描述
    if y_val >= 0:
        res_key = "聚合型" if x_val >= 0 else "同化型"
    else:
        res_key = "适应型" if x_val >= 0 else "发散型"

    st.markdown(f"<h2 style='text-align: center; color: #38BDF8;'>您的类型：{res_key}</h2>", unsafe_allow_html=True)

    analysis = {
        "聚合型": """**深度分析：** 您是典型的“技术专家”与“逻辑执行者”。在学习过程中，您展现出卓越的演绎推理能力，擅长通过抽象的理论推导来解决具体的实际问题。您更倾向于处理具体的技术任务，而非复杂的社交或人际情感。在面对挑战时，您能够迅速过滤掉干扰信息，锁定问题的唯一最优解。
        
**职业与发展：** 这种风格在工程学、计算机科学及物理研究领域极具优势。建议在团队协作中，适当增加对他人的情感关注，避免因过于追求逻辑效率而忽略了协作中的感性需求。在处理开放式、无标准答案的问题时，可以尝试多倾听发散性的建议，以增强方案的灵活性。""",
        
        "同化型": """**深度分析：** 您是一位深邃的“理论家”与“思想架构师”。您具备极强的归纳推理能力，能够从零散的信息中提取出宏观的逻辑模型。相比于实际应用，您更在意理论的严密性与逻辑的优雅。您习惯于在行动前进行详尽的观察与思考，倾向于构建系统化的知识体系。
        
**职业与发展：** 您在科研、法律、战略规划等领域具有天然优势。在学习时，请注意防止陷入“理论孤岛”，尝试将您的逻辑模型与实际操作相结合。建议多进行一些实验性质的尝试，通过现实反馈来修正您的理论预判，这样能让您的智慧更具落地价值。""",
        
        "发散型": """**深度分析：** 您是极具魅力的“创意家”与“全局感知者”。您拥有敏锐的洞察力，擅长从多个角度审视同一事物。您的学习动力往往源于丰富的感性体验和人际交流，在头脑风暴和创意策划中，您总是能提供令人惊喜的独特视角。您重视文化、情感以及事物背后的深层意义。
        
**职业与发展：** 您非常适合从事艺术、咨询、人力资源或社会科学工作。虽然您的想象力是巨大的财富，但在执行阶段，您可能会感到决策困难。建议练习使用逻辑评估工具，在众多创意中筛选出最具可行性的方案，将“感性观察”转化为“理性产出”。""",
        
        "适应型": """**深度分析：** 您是天生的“探险家”与“实干派”。您相信实践出真知，比起书本上的理论，您更信任亲手实验获得的第一手反馈。您具备极强的环境适应能力和危机处理能力，即便在信息不全的情况下，也敢于凭借直觉采取行动并不断迭代方案。您在团队中往往是那个冲在最前面的执行者。
        
**职业与发展：** 您在销售、市场开拓、创业或项目管理领域表现卓越。由于您倾向于快速行动，有时会显得缺乏耐心或忽略长远规划。建议在重大决策前预留“反思时间”，结合同化型或聚合型同事的建议，进行系统的风险评估，以避免盲目试错带来的资源浪费。"""
    }

    st.markdown(f"<div style='line-height: 1.8; font-size: 1.1rem;'>{analysis[res_key]}</div>", unsafe_allow_html=True)

    if st.button("重新测试"):
        st.session_state.current_q = 0
        st.session_state.scores = {"CE": 0, "RO": 0, "AC": 0, "AE": 0}
        st.rerun()