import streamlit as st

st.set_page_config(page_title="✨MBTI 맞춤 직업 추천✨", page_icon="🧭", layout="wide")

st.markdown("""
# 🌟 MBTI 맞춤 직업 추천 사이트 🌟
MBTI 유형에 따라 어울리는 직업과 강점을 확인해보세요! 🚀💼✨
""", unsafe_allow_html=True)

# -----------------------------
# 데이터 정의 (간단 예시)
# -----------------------------
MBTI_DATA = {
    "INTJ": {
        "설명": "🧠 전략가형 | 장기 계획과 체계 설계를 선호 ✨",
        "강점": ["🎯 전략적 사고", "🦾 독립성", "📊 분석력"],
        "유의점": ["⚠️ 과도한 완벽주의", "🤝 협업 시 융통성 부족"],
        "직업": [
            ("💻 데이터 사이언티스트", ["🔎 분석", "📚 연구", "⚙️ 기술"]),
            ("📈 전략 컨설턴트", ["📊 전략", "💼 비즈니스"]),
        ],
        "산업": ["💻 테크", "💰 금융", "📊 컨설팅"]
    },
    "ENFP": {
        "설명": "🎉 활동가형 | 호기심 많고 아이디어가 풍부 🌈",
        "강점": ["💡 브레인스토밍", "🤝 네트워킹", "📖 스토리텔링"],
        "유의점": ["⚡ 집중 분산", "⏳ 루틴 어려움"],
        "직업": [
            ("🎨 브랜드 마케터", ["✨ 브랜딩", "📣 캠페인"]),
            ("🎬 기획 PD", ["🎥 제작", "📋 기획"]),
        ],
        "산업": ["🎥 미디어", "📚 콘텐츠", "🚀 스타트업"]
    }
}

# -----------------------------
# Streamlit UI
# -----------------------------
st.sidebar.title("🔮 내 MBTI는?")
mbti_type = st.sidebar.selectbox("👉 MBTI 유형을 선택하세요:", list(MBTI_DATA.keys()))

st.markdown(f"## 🧭 {mbti_type} 직업 추천 결과")
data = MBTI_DATA[mbti_type]

st.write(f"### ✨ 설명: {data['설명']}")

st.write("### 💪 강점:")
st.markdown(" ".join(data["강점"]))

st.write("### ⚠️ 유의할 점:")
st.markdown(" ".join(data["유의점"]))

st.write("### 💼 추천 직업:")
for job, tags in data["직업"]:
    st.markdown(f"- {job} — {' '.join([f'#{t}' for t in tags])}")

st.write("### 🏢 추천 산업:")
st.markdown(" ".join(data["산업"]))

st.success("🌟 나의 성향에 맞는 직업을 찾아보세요! ✨")
