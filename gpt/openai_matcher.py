#!pip install openai
import openai
import json

config_message = """
    Your response must contain no explanation. Your response format must strictly be json with two fields.
    Input is two company entries in format: company name, latitude, longitude.
    The first is called match, it should be 1 if two companies are refrerring to the same company.
    and 0 if they are not. 
    
    The second field is called match_confidence which should represent how confident you are in your judgment.
    It should be a value between 0 and 1.
    Higher value means that you are more certain that companies are either a match or not.
    Match field must not have an impact on match_confidence field only the certainty of your judgament. 

    Response must be of format {match: number, match_confidence: number}. Do not explain your answer.

    If you cannot accept inputted entries return match -1 and match_confidence -1.
"""

openai.api_key = "ENTER_YOUR_KEY_HERE"

def parse_company_data(company):
    comp_data = company['name']

    if 'long' in company and 'lang' in company:
        comp_data += ',' + str(company['long']) + ',' + str(company['latitude'])

    return comp_data

def create_company_query(companyA, companyB):
    return parse_company_data(companyA) + '\n' + parse_company_data(companyB)

def match_companies(companyA, companyB):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": config_message},
                {"role": "user", "content": create_company_query(companyA, companyB)},
            ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    return json.loads(result)
