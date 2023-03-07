from flask import Flask, request, session
from chatbot import ask, append_interaction_to_chat_log
from dotenv import load_dotenv
import json
import os
import pandas as pd

app = Flask(__name__)
# if for some reason your conversation with the bot gets weird, change the secret key 
app.config['SECRET_KEY'] = '\xdbn\xd5?Q-i\x12'

def medication(jsondict):
    df = pd.read_excel('cleaned_data2.xlsx',index_col=False,dtype='unicode')
    sizedict = len(jsondict[0])
    medijson = {}
    for i in range(sizedict):
        diagnose = jsondict[i]['Diagnosis']
        print (diagnose)
        if(df['diagnosis_name'].str.contains(str(diagnose))).any():
            # test = df_diagnose[df_diagnose['diagnosis_name']].str.contains(diagnose) is not None
            indexloc = (df.loc[df['diagnosis_name'].str.contains(diagnose)]).sort_values('count',ascending=False).head(5)
            result_medi = ', '.join([str(value) for value in indexloc['medication_name']])
            medijson = {'Possible Medication':result_medi}
            jsondict[i].update(medijson) #write new input into existing json
        else:
            print ("The diagnosis is not exist in database")
    
    return jsondict


@app.route('/chatbot', methods=['POST'])
def chat():
    age = request.values['age']
    gender = request.values['gender']
    symptoms = request.values['symptoms']
    
    


    incoming_msg = "Im a " +  age + " and a " + gender + ". Im having a " + symptoms +  ". What the 3 possible Diagnosis,short Desc and Treatment that I might had for diagnoses in json array"
    chat_log =  session.get('chat_log')
    answer = ask(incoming_msg, chat_log)
    # session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,
    #                                                      chat_log)
    
    jsondict = json.loads(answer)
    medication(jsondict)
    print(jsondict)

    return (jsondict)

if __name__ == '__main__':
    load_dotenv()
    envport = (os.getenv('PORT_FACEDETECTION'))
    app.run(host = '0.0.0.0',port=envport,debug=True)