import streamlit as st
import pandas as pd
import datetime

# 데이터 저장용 CSV 파일
DATA_FILE = "tooth_data.csv"

# 초기 데이터 파일 생성
def init_data():
    try:
        pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["date", "brush_count", "brush_time"])
        df.to_csv(DATA_FILE, index=False)

# 데이터 저장 함수
def save_data(date, brush_count, brush_time):
    df = pd.read_csv(DATA_FILE)
    new_data = {"date": date, "brush_count": brush_count, "brush_time": brush_time}
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# 앱 실행
def main():
    st.set_page_config(page_title="나의 구강 건강 매니저", page_icon="🦷")

    st.title("🦷 나의 구강 건강 매니저")
    st.write("양치 습관을 기록하고, 구강 건강을 체크해보는 앱입니다!")

    menu = ["홈", "양치 습관 기록", "자가 진단 퀴즈", "올바른 양치법 가이드", "식습관 분석"]
    choice = st.sidebar.selectbox("메뉴 선택", menu)

    # 1. 홈
    if choice == "홈":
        st.subheader("환영합니다!")
        st.write("""
        이 앱은 치위생사 진로와 관련된 **구강 건강 관리 앱**입니다.  
        왼쪽 사이드바에서 원하는 기능을 선택해보세요!
        """)

    # 2. 양치 습관 기록
    elif choice == "양치 습관 기록":
        st.subheader("🪥 오늘의 양치 습관 기록하기")
        today = datetime.date.today()

        brush_count = st.number_input("오늘 양치 횟수", min_value=0, max_value=10, step=1)
        brush_time = st.selectbox("평균 양치 시간", ["2분 미만", "2분 이상"])

        if st.button("저장하기"):
            save_data(today, brush_count, brush_time)
            st.success("저장되었습니다!")

        # 데이터 불러오기
        df = pd.read_csv(DATA_FILE)
        if not df.empty:
            st.subheader("📊 나의 양치 습관 통계")
            st.bar_chart(df.set_index("date")["brush_count"])

    # 3. 자가 진단 퀴즈
    elif choice == "자가 진단 퀴즈":
        st.subheader("❓ 구강 건강 자가 진단")

        score = 0
        q1 = st.radio("잇몸에서 피가 난 적이 있나요?", ["예", "아니오"])
        q2 = st.radio("단 음식을 자주 먹나요?", ["예", "아니오"])
        q3 = st.radio("하루 양치 횟수가 2회 이하인가요?", ["예", "아니오"])
        q4 = st.radio("치실이나 구강세정기를 사용하지 않나요?", ["예", "아니오"])

        if st.button("결과 확인"):
            if q1 == "예": score += 2
            if q2 == "예": score += 2
            if q3 == "예": score += 3
            if q4 == "예": score += 2

            if score <= 2:
                st.success("양호 👍 구강 건강 상태가 좋아요!")
            elif score <= 5:
                st.warning("주의 🚨 더 꼼꼼한 관리가 필요해요.")
            else:
                st.error("위험 ❗ 치과 검진을 권장합니다.")

    # 4. 올바른 양치법 가이드
    elif choice == "올바른 양치법 가이드":
        st.subheader("🦷 올바른 양치법 가이드")
        st.write("""
        1. 칫솔은 45도 각도로 잇몸과 치아 사이에 대고 원을 그리듯 닦아요.  
        2. 어금니 씹는 면은 앞뒤로 문질러 닦아요.  
        3. 혀도 가볍게 닦아주면 구취 예방에 좋아요.  
        4. 하루 1번은 꼭 치실이나 구강세정기를 사용하세요.
        """)
        st.image("https://www.colgate.com/content/dam/cp-sites/oral-care/oral-care-center/global/articles/hero/2021/hero-716x404-brushing-teeth.jpg", caption="올바른 양치법 예시")

    # 5. 식습관 분석
    elif choice == "식습관 분석":
        st.subheader("🍎 식습관 & 치아 건강")

        foods = st.multiselect("오늘 먹은 음식 선택", 
                               ["사탕", "콜라", "사과", "우유", "커피", "초콜릿", "치즈", "레몬"])

        if st.button("분석하기"):
            bad_foods = {"사탕", "콜라", "초콜릿", "레몬", "커피"}
            good_foods = {"사과", "우유", "치즈"}

            score = 0
            for f in foods:
                if f in bad_foods:
                    score -= 1
                elif f in good_foods:
                    score += 1

            if score > 0:
                st.success("👍 좋은 식습관이에요! 치아 건강에 유리합니다.")
            elif score == 0:
                st.warning("😐 보통 수준이에요. 균형 잡힌 식습관을 유지하세요.")
            else:
                st.error("⚠️ 치아에 해로운 음식이 많아요! 주의하세요.")

# 실행
if __name__ == '__main__':
    init_data()
    main()

