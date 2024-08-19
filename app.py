import streamlit as st
import math
from datetime import datetime

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def cal_biorhythms (birthdate) :
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
    intellectual_biorhythm = math.sin(2 * math.pi * days_since_birth / intellectual_cycle)
    
    return {
        "physical": physical_biorhythm,
        "emotional": emotional_biorhythm,
        "intellectual": intellectual_biorhythm
    }

def processing (mbti, biorythm) :
    st.subheader("오늘 당신은?" )
    #line1 = "당신의 MBTI는 **" + mbti + "** 입니다."
    #st.markdown(line1)

    #gpt 연동
    model = ChatOllama(model="gemma2:2b", temperature=1.5, base_url="http://192.168.1.230:11434", callbacks=[StreamingStdOutCallbackHandler()])
    prompt = ChatPromptTemplate.from_template(
        """당신은 MBTI와 바이오리듬 관련 전문상담사 입니다. 
        MBTI가 {mbti} 이고 바이오리듬(신체: {p}, 감성 {e}, 지성{i}) 이 인 사람의 오늘에 대해서 간략히게 조언해주세요.
        """
    )

    chain = prompt | model | StrOutputParser()

    response = st.write_stream(chain.stream({"mbti" : mbti, "p":biorythm["p"], "e":biorythm["e"], "i":biorythm["i"]}))


def main () :
    st.title("나의 오늘은 어떨까?")

    #mbti = st.text_input("당신의 MBTI는?", "")
    mbti = st.selectbox(
        "당신의 MBTI는?",
        ("선택", "ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"),
    )
    if mbti :
        st.write("당신의 MBTI는 ", mbti , " 입니다." )

        birthday = st.text_input("당신의 생일은?", "")
    
        if birthday :
            st.write("당신의 생일은  ", birthday , " 입니다." )
            

    if mbti and birthday :
        if st.button("확인") :
            today_biorythm = cal_biorhythms(birthday)
            p = str(round(today_biorythm['physical'], 2))
            e = str(round(today_biorythm['emotional'], 2))
            i = str(round(today_biorythm['intellectual'],2 ))

            biorythm = {"p":p, "e":e, "i":i}
            
            #show_text1 = "당신의 MBTI는 "+ mbti + "이고, 당신의 생일은 " + birthday + " 입니다."

            #st.text(show_text1)
            
            #st.text("오늘의 바이오리듬은 : " + p)

            processing(mbti, biorythm)

if __name__ == '__main__':
    main()
