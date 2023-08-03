import streamlit as st
import utils
import os
import openai


# ---- helper functions ----
def generateAItext(query, prompt):
    #with OpenAI
    #return utils.ask_openai(query=query, prompt=prompt)
    
    #with Azure OpenAI
    return utils.ask_azure("Schreibe den Text zwischen ``` entsprechend den Regeln der Einfachen Sprache. Verwende kurze und einfache Sätze.``` "+query+ "```")


# ---- initialize ----

st.set_page_config(page_title="Einfache Sprache", layout="wide")
inputstr = ""
aistr = ""
prompt = ""
query = ""
#save here value api key if you don't want to input it at every app run
os.environ['OPENAI_API_KEY']=""
openai.api_key=""

# ---- Header Section ----
with st.container():
    #utils.init()
    st.title("Einfache Sprache")
    prompt = "Schreibe diesen Text entsprechend den Regeln der Einfachen Sprache. Verwende kurze und einfache Sätze."
    st.session_state["promptState"] = prompt

#API Key
api_key= st.text_input("ApiKey: ","", key="api_key_input", type="password")
if api_key:
    os.environ['OPENAI_API_KEY']=api_key
    openai.api_key  = api_key
    st.write("ApiKey entered successfully")

# ---- Check einfache Sprache ----
with st.container():
    st.write('---')
    col1,col2,col3,col4,col5=st.columns(5)
    
    left_column, middle_column, right_column = st.columns(3)
    st.write('---')
    left_res_column, right_res_column = st.columns(2)


    # ---- text check ----
    with col3:        
        center_button = st.button('Einfachen Text generieren')
        if center_button:
            st.session_state["response"] = generateAItext(st.session_state["queryState"], st.session_state["promptState"])
            st.generatedText = st.session_state["response"]

    with left_column:
        st.subheader("Ausgangstext:")
        query = st.text_area("Eigener Text:", height=300)
        st.session_state["queryState"] = query
        if st.button("Check"):
            with left_res_column:
                aistr = st.session_state["response"]
                st.subheader("Ergebnis der Prüfung des eigenen Textes:")
                st.write("Niveau: " + utils.calulateDifficultyNiveau(query))
                st.pyplot(utils.create_horizontal_bar_chart(utils.calculateDifficultyPercentage(query)))
                with st.expander(label="Mehr Infos"):
                    d = {"Readability index":
                             ["Flesch-Reading-Ease German",
                              "Wiener Sachtextformel",
                              "Lesbarkeitsindex (LIX)"],
                         "Result":
                             [utils.getFleschGer(query),
                              utils.getWiener(query),
                              utils.getLix(query)],
                         "Bad-Good":
                             ["0-100",
                              "15-4",
                              "60-20"]}

                    st.table(d)

                with right_res_column:
                    st.subheader("Ergebnis der Prüfung des generierten Textes:")
                    st.write("Niveau: " + utils.calulateDifficultyNiveau(aistr))
                    st.pyplot(utils.create_horizontal_bar_chart(utils.calculateDifficultyPercentage(aistr)))
                    with st.expander(label="Mehr Infos"):
                        d2 = {"Readability index":
                                  ["Flesch-Reading-Ease German",
                                   "Wiener Sachtextformel",
                                   "Lesbarkeitsindex (LIX)"],
                              "Result":
                                  [utils.getFleschGer(aistr),
                                   utils.getWiener(aistr),
                                   utils.getLix(aistr)],
                              "Bad-Good":
                                  ["0-100",
                                   "15-4",
                                   "60-20"]}
                        st.table(d2)


    # ---- AI generated easy-text ----

    if "response" not in st.session_state:
        st.session_state["response"] = ""
    if "queryState" not in st.session_state:
        st.session_state["queryState"] = ""
    if "promptState" not in st.session_state:
        st.session_state["promptState"] = ""

    with right_column:
        st.subheader("Generierter \"leichter\" Text")
        aistr = st.text_area("AI:", height=300, key="generatedText", value=st.session_state["response"])

# --- results container with plot
#with st.expander("Visualise results"):
#    image = Image.open('results_table.png')
#    st.image(image, caption='Metrics calculated on generated texts')

