import streamlit as st
import pandas as pd
import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

DATA_FILE = "tooth_data.csv"

# =========================
# 데이터 초기화
# =========================
def init_data():
    try:
        pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["date", "brush_count", "brush_time"])
        df.to_csv(DATA_FILE, index=False)

def save_data(date, brush_count, brush_time):
    df = pd.read_csv(DATA_FILE)
    new_data = {"date": date, "brush_count": brush_count, "brush_time": brush_time}
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# =========================
# PDF 보고서 생성 함수
# =========================
def generate_pdf(title, feedback_list):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate("report.pdf")
    story = [Paragraph(f"<b>{title}</b>", styles["Title"]), Spacer(1, 20)]

    for item in feedback_list:
        story.append(Paragraph(f"- {item}", styles["Normal"]))
        story.append(Spacer(1, 10))

    doc.build(story)
    with open("report.pdf", "rb") as f:
        return f.read()

# =========================
# 메인 앱
# =========================
def main():
    st.set_page_config(page_title="구강 건강 매니저", page_icon="🦷", layout="centered")

    # 🎨 CSS (배경 섹션 색상: 하늘색, 청록색, 흰색 번갈아)
    st.markdown(
        """
        <style>
        .section-blue {background-color:#e6f7ff; padding:20px; border-radius:15px;}
        .section-green {background-color:#e6fff9; padding:20px; border-radius:15px;}
        .section-white {background-color:#ffffff; padding:20px; border-radius:15px; border:1px solid #ddd;}
        .stButton>button {
            background-color: #5bc0de;
            color: white;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            border: none;
        }
        .stButton>button:hover {background-color: #31b0d5;}
        </style>
        """, unsafe_allow_html=True
    )

    st.title("🦷 구강 건강 매니저")
    st.caption("치위생사의 관점으로 만든 구강 건강 관리 앱")

    menu = ["🏠 홈", "🪥 양치 습관 기록", "❓ 자가 진단 퀴즈", "📖 올바른 양치법 가이드", "🍎 식습관 분석"]
    choice = st.sidebar.radio("메뉴 선택", menu)

    # ------------------------
    # 홈 화면
    # ------------------------
    if choice == "🏠 홈":
        st.markdown('<div class="section-blue">', unsafe_allow_html=True)
        st.subheader("환영합니다 👋")
        st.info("이 앱은 **양치 습관 관리, 자가 진단, 식습관 분석**을 통해 구강 건강을 도와주는 프로그램입니다.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------
    # 2. 자가 진단 퀴즈
    # ------------------------
    elif choice == "❓ 자가 진단 퀴즈":
        st.markdown('<div class="section-green">', unsafe_allow_html=True)
        st.subheader("🩺 구강 건강 자가 진단")

        score = 0
        feedback = []

        q1 = st.radio("잇몸에서 피가 난 적이 있나요?", ["예", "아니오"])
        q2 = st.radio("단 음식을 자주 먹나요?", ["예", "아니오"])
        q3 = st.radio("하루 양치 횟수가 2회 이하인가요?", ["예", "아니오"])
        q4 = st.radio("치실이나 구강세정기를 사용하지 않나요?", ["예", "아니오"])
        q5 = st.radio("정기적으로 치과 검진을 받지 않나요?", ["예", "아니오"])
        q6 = st.radio("흡연을 하나요?", ["예", "아니오"])

        if st.button("결과 확인"):
            if q1 == "예": score += 2; feedback.append("잇몸 출혈은 치주질환의 초기 증상일 수 있어요.")
            if q2 == "예": score += 2; feedback.append("단 음식은 충치 발생 위험을 높입니다.")
            if q3 == "예": score += 3; feedback.append("하루 2회 이상 양치해야 충치 예방이 됩니다.")
            if q4 == "예": score += 2; feedback.append("치실은 칫솔이 닿지 않는 부분을 청결하게 유지해줍니다.")
            if q5 == "예": score += 2; feedback.append("정기 검진은 구강 문제를 조기 발견하는 데 중요합니다.")
            if q6 == "예": score += 3; feedback.append("흡연은 잇몸병과 구강암의 위험을 크게 높입니다.")

            if score <= 3:
                st.success("👍 양호: 전반적으로 구강 건강 상태가 좋아요.")
            elif score <= 7:
                st.warning("⚠️ 주의: 개선이 필요합니다.")
            else:
                st.error("🚨 위험: 전문적인 검진이 필요할 수 있습니다.")

            st.subheader("📌 맞춤 피드백")
            for f in feedback:
                st.write(f"• {f}")

            # PDF 다운로드 기능
            pdf_bytes = generate_pdf("자가 진단 결과", feedback)
            st.download_button(
                label="📄 결과 보고서 PDF 다운로드",
                data=pdf_bytes,
                file_name="dental_report.pdf",
                mime="application/pdf"
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------
    # 식습관 분석
    # ------------------------
    elif choice == "🍎 식습관 분석":
        st.markdown('<div class="section-white">', unsafe_allow_html=True)
        st.subheader("🍎 오늘의 식습관 분석")

        foods = st.multiselect("오늘 먹은 음식 선택", 
                               ["사탕", "콜라", "사과", "우유", "커피", "초콜릿", "치즈", "레몬", "채소", "빵"])

        if st.button("분석하기"):
            details = {
                "사탕": "🍬 당분이 높아 충치 발생 위험이 큽니다.",
                "콜라": "🥤 산성이 강해 치아 부식 위험이 있습니다.",
                "사과": "🍏 침 분비를 촉진해 구강 세정 효과가 있습니다.",
                "우유": "🥛 칼슘이 풍부해 치아 강화에 좋습니다.",
                "커피": "☕ 착색을 유발할 수 있어 양치가 필요합니다.",
                "초콜릿": "🍫 당분이 높아 충치 위험이 있습니다.",
                "치즈": "🧀 산성도를 중화시켜 충치 예방에 도움이 됩니다.",
                "레몬": "🍋 산성이 강해 치아 부식을 유발할 수 있습니다.",
                "채소": "🥦 섬유질이 풍부해 치아 표면 청소에 도움이 됩니다.",
                "빵": "🍞 전분이 당으로 변해 충치를 유발할 수 있습니다."
            }

            score = 0
            feedback = []
            for f in foods:
                feedback.append(details[f])
                if f in ["사탕", "콜라", "초콜릿", "레몬", "커피", "빵"]:
                    score -= 1
                elif f in ["사과", "우유", "치즈", "채소"]:
                    score += 1

            if score > 0:
                st.success("✅ 전반적으로 치아 건강에 좋은 식습관입니다.")
            elif score == 0:
                st.warning("😐 보통 수준이에요. 균형 잡힌 식습관을 유지하세요.")
            else:
                st.error("⚠️ 치아에 해로운 음식 섭취가 많습니다. 주의하세요.")

            st.subheader("📌 세부 분석 결과")
            for f in feedback:
                st.write(f"- {f}")

            # PDF 다운로드 기능
            pdf_bytes = generate_pdf("식습관 분석 결과", feedback)
            st.download_button(
                label="📄 식습관 분석 보고서 PDF 다운로드",
                data=pdf_bytes,
                file_name="diet_report.pdf",
                mime="application/pdf"
            )
        st.markdown("</div>", unsafe_allow_html=True)

# 실행
if __name__ == '__main__':
    init_data()
    main()
