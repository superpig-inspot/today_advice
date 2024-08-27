import streamlit as st
import math
from datetime import datetime

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def cal_biorhythms(birthdate):
    # 생년월일을 datetime 객체로 변환
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.today()

    # 오늘까지의 일수를 계산
    days_since_birth = (today - birthdate).days

    # 바이오리듬 주기
    physical_cycle = 23
    emotional_cycle = 28
    intellectual_cycle = 33

    # 바이오리듬 계산
    physical_biorhythm = math.sin(2 * math.pi * days_since_birth / physical_cycle)
    emotional_biorhythm = math.sin(2 * math.pi * days_since_birth / emotional_cycle)
    intellectual_biorhythm = math.sin(
        2 * math.pi * days_since_birth / intellectual_cycle
    )

    return {
        "physical": physical_biorhythm,
        "emotional": emotional_biorhythm,
        "intellectual": intellectual_biorhythm,
    }


def processing(mbti, biorythm, llmModel):
    st.subheader("오늘 당신은?")
    # line1 = "당신의 MBTI는 **" + mbti + "** 입니다."
    # st.markdown(line1)

    baseUrl = "http://211.202.65.151:11434"

    if llmModel == "colab":
        llmModel = "gemma2:9b"
        baseUrl = "https://deee-34-143-150-41.ngrok-free.app"

    # gpt 연동
    model = ChatOllama(
        model=llmModel,
        temperature=1.5,
        base_url=baseUrl,
        callbacks=[StreamingStdOutCallbackHandler()], 
    )
    prompt = ChatPromptTemplate.from_template(
        """당신은 MBTI와 바이오리듬 관련 전문상담사 입니다. 
        MBTI가 {mbti} 이고 바이오리듬이 신체: {p}, 감성 {e}, 지성{i} 인 사람의 오늘에 대해서 구체적인 활동에 대한 예를 들어 한글로만 재미있게 조언해주세요.
        """
    )

    chain = prompt | model | StrOutputParser()

    response = st.write_stream(
        chain.stream(
            {"mbti": mbti, "p": biorythm["p"], "e": biorythm["e"], "i": biorythm["i"]}
        )
    )


def main():
    st.title("나의 오늘은 어떨까?")

    llmModel = st.radio(
        "답변에 사용할 LLM Model",
        [
            "gemma2:2b",
            "gemma2:latest",
            "colab",
            "EEVE-korean-10.8B:latest",
            "llama-3-Korean-Bllossom:latest",
        ],
        captions=[
            "Google Gemma2 2b",
            "Google Gemma2 9b",
            "Colab Google Gemma2 9b",
            "EEVE Model(야놀자에서 한국어로 조정한 버젼)",
            "llama-3-Korean-Bllossom(llama-3의 Bllosom 한글화 버젼)",
        ],
    )

    # mbti = st.text_input("당신의 MBTI는?", "")
    lstMbti = {
        "선택": "",
        "ISTJ (세심한 관리자)": "ISTJ",
        "ISFJ (온화한 수호자)": "ISFJ",
        "INFJ (통찰력 있는 상담가)": "INFJ",
        "INTJ (전략적인 계획자)": "INTJ",
        "ISTP (논리적인 장인)": "ISTP",
        "ISFP (호기심 많은 예술가)": "ISFP",
        "INFP (열정적인 중재자)": "INFP",
        "INTP (논리적인 사색가)": "INTP",
        "ESTP (현실적인 사업가)": "ESTP",
        "ESFP (자유로운 영혼)": "ESFP",
        "ENFP (창의적인 활동가)": "ENFP",
        "ENTP (논쟁적인 발명가)": "ENTP",
        "ESTJ (체계적인 관리자)": "ESTJ",
        "ESFJ (사교적인 돌봄이)": "ESFJ",
        "ENFJ (카리스마 있는 지도자)": "ENFJ",
        "ENTJ (단호한 통솔자)": "ENTJ",
    }
    mbti = st.selectbox("당신의 MBTI는?", list(lstMbti.keys()))
    if mbti:
        st.write("당신의 MBTI는 ", mbti, " 입니다.")

        birthday = st.date_input(
            "당신의 생일은?", datetime(2000, 1, 1), format="YYYY-MM-DD"
        )

        if birthday:
            st.write("당신의 생일은  ", birthday, " 입니다.")

    if mbti and birthday:
        if st.button("확인"):
            today_biorythm = cal_biorhythms(birthday.strftime("%Y-%m-%d"))
            p = str(round(today_biorythm["physical"], 2))
            e = str(round(today_biorythm["emotional"], 2))
            i = str(round(today_biorythm["intellectual"], 2))

            biorythm = {"p": p, "e": e, "i": i}

            # show_text1 = "당신의 MBTI는 "+ mbti + "이고, 당신의 생일은 " + birthday + " 입니다."

            # st.text(show_text1)

            # st.text("오늘의 바이오리듬은 : " + p)

            processing(lstMbti[mbti], biorythm, llmModel)


if __name__ == "__main__":
    main()
