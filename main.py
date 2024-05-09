import json
from openai import OpenAI
import os
import sqlite3
from time import time
import build
from db import create_connection
from schema import get_schema

print("Running main.py")

fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

conn = create_connection(getPath("database.db"))

# build the database
build.main()

def runSql(query):
    
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
    return result

configPath = getPath("config.json")
with open(configPath) as configFile:
    config = json.load(configFile)

openAiClient = OpenAI(
    api_key = config["openaiKey"],
    organization = config["orgId"],
    project=config["projectId"],
)

def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": content}],
        stream=True
    )

    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)
    result = "".join(responseList)
    return result


commonSqlOnlyRequest = "Give me an sqlite select statement that answers the question. Only respond with the sqlite syntax, and do not explain any errors."
schemaString = get_schema()
strategies = {
    "zero_shot": schemaString + commonSqlOnlyRequest,
    "single_domain_double_shot": (schemaString + 
                                  "Here is an example question and sqlite statement:" + 
                                  "What is the average duration of the workouts?" + 
                                  "\nSELECT AVG(duration) \nFROM workout;" + 
                                  commonSqlOnlyRequest)
            }
questions = [
    "What is the average duration of the workouts?",
    "What is the total number of workouts?",
    "What is the average sleep score?",
    "What is the average resting heart rate?",
    "What workouts did the coach with the highest id assign?",
    "What is the total number of workouts assigned by the coach with the highest id?"
]

def sanitizeForJustSql(value):
    startSqlMarker = "```sql"
    endSqlMarker = "```"
    if startSqlMarker in value:
        value = value.split(startSqlMarker)[1]
    if endSqlMarker in value:
        value = value.split(endSqlMarker)[0]

    return value

for strategy in strategies:
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    for question in questions:
        print(question)
        error = "None"
        try:
            sqlSyntaxResponse = getChatGptResponse(strategies[strategy] + " " + question)
            sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
            print(sqlSyntaxResponse)
            queryRawResponse = str(runSql(sqlSyntaxResponse))
            print(queryRawResponse)
            friendlyResultsPrompt = "I asked a question \"" + question + "\" and received the following response: " + queryRawResponse + "\n\"Please, just give a concise response in a more fiendly way? Please do not give any other suggestions or chatter."
            friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
            print(friendlyResponse)
        except Exception as e:
            error = str(e)
            print(error)


        questionResults.append({"question": question, 
                                "sql": sqlSyntaxResponse,
                                "queryRawResponse" : queryRawResponse,
                                "friendlyResponse": friendlyResponse,
                                "error": error
                                })
        responses["questions"] = questionResults

        with open(getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
            json.dump(responses, outFile, indent = 2)
            print("Done writing file")

conn.close()
print("Done!")