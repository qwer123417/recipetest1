import streamlit as st
import openai

# 🔐 OpenAI API 키는 Streamlit Cloud의 Secrets에 저장되어 있음
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("자취생 레시피 도우미")
st.write("냉장고 속 재료를 입력하면, 간단한 요리를 추천해줘요! 🍳")

ingredients = st.text_area("🍅 식재료를 입력해주세요 (예: 계란, 양파, 두부)", height=150)

if st.button("레시피 추천받기"):
    if not ingredients.strip():
        st.warning("식재료를 입력해주세요!")
    else:
        with st.spinner("레시피 생성 중...🍽️"):
            prompt = f"""
            나는 한국에 사는 자취생이야. 냉장고에는 다음 식재료들이 있어: {ingredients}.
            이 재료들로 만들 수 있는 간단한 요리 3가지를 추천해줘.
            각 요리의 이름과, 짧고 간단한 1인분 기준 조리법도 함께 알려줘.
            인터넷에 있는 검증된 레시피를 알려줘.
            그 레시피의 출처와, 링크를 달아서 자세히 볼 수 있게해줘.
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "넌 요리 전문가야."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                result = response.choices[0].message.content
                st.success("🍽️ 요리 추천이 도착했어요!")
                st.markdown(result)

            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")
