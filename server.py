#pip install "fastapi[all]"
#pip install "uvicorn[standard]"
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import jsonlines
from ditto_light.summarize import Summarizer
import matcher
import uuid
from pydantic import BaseModel
import json
from server_config import SERVER_CONFIG
import os
import webbrowser
import gpt.openai_matcher

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")

models = {}
  
class obj:
    def __init__(self, dict1):
        self.__dict__.update(dict1)
  
def to_obj(dict1):
    return json.loads(json.dumps(dict1), object_hook=obj)

class CompanyData(BaseModel):
    name: str
    long: int
    lat: int

class CompanyPair(BaseModel):
    matcher: str
    country: str
    companyA: CompanyData
    companyB: CompanyData

def parse_company_type(name):
    return 'co'

def parse_company_name(name):
    return name.lower()

def to_col_val(comp_type, company: CompanyData):
    if comp_type == 'full':
        return 'COL COMPANY VAL ' + parse_company_name(company['name']) + \
               ' COL CO_CATEGORY VAL ' + parse_company_type(company['name']) + \
               ' COL LONG VAL ' + str(round(company['long'], 2)) + \
               ' COL LAT VAL ' + str(round(company['lat'], 2))

    return 'COL COMPANY VAL ' + company['name']

def create_input(pair_data: CompanyPair):
    pair_type = get_pair_type(pair_data)
    file_name = 'query-' + pair_data['country'] + '-' + pair_type + '-' + uuid.uuid4().hex + '.jsonl'

    target_file = jsonlines.open(SERVER_CONFIG['input_folder'] + file_name, mode='w')
    target_file.write([to_col_val(pair_type, pair_data['companyA']), to_col_val(pair_type, pair_data['companyB'])])

    return file_name

def get_pair_type(pair_data: CompanyPair):
    compA = pair_data['companyA']
    compB = pair_data['companyB']

    if 'long' not in compA or 'lat' not in compA or 'long' not in compB or 'lat' not in compB:
        return 'no_loc'
    
    if compA['long'] == None or compA['lat'] == None or compB['long'] == None or compB['lat'] == None:
        return 'no_loc'

    return 'full'

def get_task(country, type):
    return SERVER_CONFIG['task'][type][country.upper()]

def preload_models():
    for model_type in SERVER_CONFIG['task'].values():
        for task in model_type.values():
            config, model = matcher.load_model(
                task, 
                SERVER_CONFIG['checkpoint_path'],
                SERVER_CONFIG['language_model'], 
                SERVER_CONFIG['use_gpu'], 
                SERVER_CONFIG['use_fp16']    
            )
            
            threshold = matcher.tune_threshold(config, model, to_obj({
                'task': task, 
                'lm': SERVER_CONFIG['language_model'], 
                'max_len': SERVER_CONFIG['max_len'],
                'summarize': False,
                'dk': None
            }))

            #summarizer = Summarizer(config, SERVER_CONFIG['language_model'])
            summarizer = None
            models[task] = [config, model, threshold, summarizer]

def get_model(pair_data: CompanyPair):
    return models[get_task(pair_data['country'], get_pair_type(pair_data))]

def get_ditto_estimation(pair_data: CompanyPair): 
    file_name = create_input(pair_data)

    matcher.set_seed(123)
    config, model, threshold, summarizer = get_model(pair_data)

    matcher.predict(
        SERVER_CONFIG['input_folder'] + file_name, 
        SERVER_CONFIG['output_folder'] + file_name, 
        config, model,
        summarizer=summarizer,
        max_len=SERVER_CONFIG['max_len'],
        lm=SERVER_CONFIG['language_model'],
        dk_injector=None,
        threshold=threshold
    )
    
    result = jsonlines.open(SERVER_CONFIG['output_folder'] + file_name, mode="r").read()

    os.remove(SERVER_CONFIG['input_folder'] + file_name)    
    os.remove(SERVER_CONFIG['output_folder'] + file_name)    

    return { 
        'match': result['match'],
        'match_confidence': result['match_confidence']
    }

@app.post("/match")
async def match_companies(request: Request):
    pair_data = await request.json()

    if pair_data['matcher'] == 'chat-gpt':
        return openai_matcher.match_companies(pair_data['companyA'], pair_data['companyB'])

    return get_ditto_estimation(pair_data)

preload_models()

if __name__ == "__main__":
    webbrowser.open(url='http://' + SERVER_CONFIG['base_url'] + ':' + str(SERVER_CONFIG['port']) + '/static/index.html', new=2)
    uvicorn.run(app, host=SERVER_CONFIG['base_url'], port=SERVER_CONFIG['port'])