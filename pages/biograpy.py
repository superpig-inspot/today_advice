import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 바이오리듬 주기
PHYSICAL_CYCLE = 23
EMOTIONAL_CYCLE = 28
INTELLECTUAL_CYCLE = 33


# 바이오리듬 함수
def calculate_biorhythm(birth_date, target_date):
    days_lived = (target_date - birth_date).days
    physical = np.sin(2 * np.pi * days_lived / PHYSICAL_CYCLE)
    emotional = np.sin(2 * np.pi * days_lived / EMOTIONAL_CYCLE)
    intellectual = np.sin(2 * np.pi * days_lived / INTELLECTUAL_CYCLE)
    return physical, emotional, intellectual


# Streamlit 앱 제목
st.title("Biorhythm Chart")

# 사용자 입력 - 생일
birth_date = st.date_input("Enter your birth date", datetime(2000, 1, 1))

# 사용자 입력 - 타겟 날짜
target_date = st.date_input("Select target date", datetime.today())

# 날짜 타입 변환 (datetime.date -> datetime)
birth_date = pd.to_datetime(birth_date).date()
target_date = pd.to_datetime(target_date).date()

# 차트 표시 날짜 범위 설정
date_range = st.slider("Select date range (days)", 15, 60, 30)

# 타겟 날짜 기준으로 앞뒤 날짜 계산
start_date = target_date - timedelta(days=date_range)
end_date = target_date + timedelta(days=date_range)

# 날짜 리스트 생성
dates = pd.date_range(start_date, end_date)

# 바이오리듬 값 계산
physical_values = []
emotional_values = []
intellectual_values = []

for date in dates:
    physical, emotional, intellectual = calculate_biorhythm(birth_date, date.date())
    physical_values.append(physical)
    emotional_values.append(emotional)
    intellectual_values.append(intellectual)

# DataFrame 생성
df = pd.DataFrame(
    {
        "Date": dates,
        "Physical": physical_values,
        "Emotional": emotional_values,
        "Intellectual": intellectual_values,
    }
)

# 차트 그리기
st.subheader("Biorhythm Chart")
plt.figure(figsize=(10, 6))
plt.plot(df["Date"], df["Physical"], label="Physical", color="red")
plt.plot(df["Date"], df["Emotional"], label="Emotional", color="green")
plt.plot(df["Date"], df["Intellectual"], label="Intellectual", color="blue")
plt.axhline(0, color="black", linestyle="--")
plt.title("Biorhythm")
plt.xlabel("Date")
plt.ylabel("Rhythm Value")
plt.legend(loc="upper right")
plt.grid(True)
st.pyplot(plt)
