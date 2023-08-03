import os
import openai
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from statistics import mean
import textstat
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage

def ask_openai(
        # we tell the model to answer our question using the results from the query_message as source of information
        query: str,
        model: str = "gpt-3.5-turbo",
        # token_budget: int = 4096 - 500,
        print_message: bool = False,
        prompt: str = ""
) -> str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    messages = [
        {"role": "system", "content": f"""
        You are a German AI assistant. 
        {prompt}"""},
        {"role": "user", "content": query},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )
    #print(prompt)
    response_message = response["choices"][0]["message"]["content"]
    return response_message

def ask_azure(
    #we tell the model to answer our question using the results from the query_message as source of information
    query: str,
    deployment: str = "gpt-35-turbo_SZ",
    #api_key: str=""
):

    DEPLOYMENT_NAME = "chat"
    model = AzureChatOpenAI(
            openai_api_base="https://dtc-genai-sandbox.openai.azure.com/",
            openai_api_version="2023-05-15",
            deployment_name=deployment,
            openai_api_key=os.environ.get('OPENAI_API_KEY'),
            openai_api_type="azure",
            )

    response_message= model([HumanMessage(content=query)]).content
    return response_message

def getFleschGer(inputStr):
    return textstat.textstat.flesch_reading_ease(inputStr)

def getWiener(inputStr):
    return textstat.textstat.wiener_sachtextformel(inputStr,4)

def getLix(inputStr):
    return textstat.textstat.lix(inputStr)

def FleschNiveau(inputStr):
    value=textstat.textstat.flesch_reading_ease(inputStr)
    if 0<value<=30:
        return 7
    elif 30<value<=50:
        return 6
    elif 50<value<=60:
        return 5
    elif 60<value<=70:
        return 4
    elif 70<value<=80:
        return 3
    elif 80<value<=90:
        return 2
    else:
        return 1

def LIXNiveau(inputStr):
    value=textstat.textstat.lix(inputStr)
    if value<25:
        return 1
    elif 25<value<=35:
        return 2
    elif 35<value<=42.5:
        return 3
    elif 42.5<value<=47.5:
        return 4
    elif 47.5<value<=52.5:
        return 5
    elif 52.5<value<=60:
        return 6
    else:
        return 7

def WienerNiveau(inputStr):
    value= textstat.textstat.wiener_sachtextformel(inputStr,4)
    if value<5:
        return 1
    elif 5<value<=6:
        return 2
    elif 6<value<=8:
        return 3
    elif 8<value<=10:
        return 4
    elif 10<value<=11:
        return 5
    elif 11<value<=12:
        return 6
    else:
        return 7

def calculateDifficultyPercentage(inputStr):
    #calculate the 3 niveaus
    flesch=FleschNiveau(inputStr)
    lix=LIXNiveau(inputStr)
    wiener=WienerNiveau(inputStr)
    #print(str(flesch)+" - "+str(lix)+" - "+ str(wiener))

    #calculate average
    average= mean([flesch,lix,wiener])

    #normalise by dividing by 7
    return average/7*100

def calulateDifficultyNiveau(inputStr):
    #calculate the 3 niveaus
    flesch=FleschNiveau(inputStr)
    lix=LIXNiveau(inputStr)
    wiener=WienerNiveau(inputStr)
    #print(str(flesch)+" - "+str(lix)+" - "+ str(wiener))

    #calculate average
    average= mean([flesch,lix,wiener])

    if 0<average<=1:
        return "Sehr einfach"
    elif 1<average<=2:
        return "Einfach"
    elif 2<average<=3:
        return "Mitteleinfach"
    elif 3<average<=4:
        return "Mittel"
    elif 4<average<=5:
        return "Mittelschwer"
    elif 5<average<=6:
        return "Schwer"
    else:
        return "Sehr schwer"

def create_horizontal_bar_chart(value):
    plt.figure(figsize=(10, 1))
    colors = ['green', 'yellow', 'red']
    cmap = mcolors.LinearSegmentedColormap.from_list('custom_colormap', colors, N=100)
    normalized_value = int((value - 0) / (100 - 0) * 100)
    plt.barh(['Schwierigkeit:'], [value], color=cmap(normalized_value))
    plt.yticks(['Schwierigkeit:'])
    plt.xticks(range(0, 101, 10), [''] * 11)
    plt.axis('on')
    return plt.gcf()