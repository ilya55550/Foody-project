import json


def country_definition(phone_country_code):
    name_country = 'Неопределено'
    if phone_country_code == '+7':  # для оптимизации
        return 'Russia'
    with open('foodapp/tools/Country_codes.json', 'r', encoding='utf-8') as f:
        country_codes = json.load(f)
        name_country = [country for country in country_codes['countries'] if
                        country['code'] == '+' + str(phone_country_code)][0]['name']
    return name_country
