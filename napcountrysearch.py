#!/usr/bin/python3

from napcountrydb import valid_country_data
from napcountrydb import valid_countries


valid_country_data_short = {
    'Ирландия': ['IE', 'IRL', 'Ireland'],
    'Австралия': ['AU', 'AUS', 'Australia'],
    'Великобритания': ['GB', 'GBR', 'United Kingdom', 'Great Britain', 'Британия', 'ЮК', 'Острова', 'Кралството'],
    'САЩ': ['US', 'USA', 'United States of America', 'Съединени Американски Щати', 'Съединените Американски Щати', 'Щатите', 'США', 'Съединените Щати', 'Съединени Щати' ],
    'Нидерландия (Холандия)': ['NL', 'NLD', 'Kingdom of the Netherlands','Нидерландия', 'Холандия'],
    'Остров Ман': ['IM', 'IMN', 'Isle of Man', 'Ман'],
    'Виржински о-ви (Брит.)': ['VG', 'VGB', 'British Virgin Islands', 'BVI','Вирджински острови', 'Виржински острови', 'Британски Вирджински острови', 'Британски Виржински острови'],
    'Кайманови о-ви': ['KY', 'CYM', 'Cayman Islands', 'Cayman', 'Кайманови острови', 'Каймановите острови' 'Каймански острови', 'Каймани', 'Кайманите' ],
    'Маршалски о-ви': ['MH', 'MHL', 'Republic of the Marshall Islands', 'Marshall Islands', "Маршалски острови", "Маршалските острови", "Маршалови острови", "Маршаловите острови", "Островите на маршалите", "Маршалите"],
    'Остров Джърси (Великобритания)': ['JE', 'JEY', 'Jersey', 'Джърси', 'Остров Джърси'],
    'Хонконг': ['HK', 'HKG', 'Hong Kong Special Administrative Region', 'Hong Kong', "Honk Konk", "Хонконг", "Хонг Конг", "Хонг Конк", "Хонконк"],
    'Израел': ['IL', 'ISR', 'State of Israel', 'Israel'],
    'Русия': ['RU', 'RUS', 'Russian Federation','Russia','Руска федерация','Мордор','Московия'],
    'Китай': ['CN', 'CHN', 'People\'s Republic of China', 'PRC', 'Китай','Република Китай', 'Народна република Китай', 'Китайска народна република'],
    'Япония': ['JP', 'JPN', 'Japan'],
    'Франция': ['FR', 'FRA', 'French Republic', 'France'],
    'Германия': ['DE', 'DEU', 'Federal Republic of Germany', 'Germany', "Република Германия", "Федерална република Германия"],
    'Швейцария': ['CH', 'CHE', 'Swiss Confederation', 'Switzerland', "Swiss", "Швейцарска конфедерация"],
}

# TODO:
# To search with "Republic of $string", "People's Republic of $string",  "Republic of the $string", "State of $string"
# And also search by removing "Republic of", etc. from the search queary, by replacing "Democratic Republic" with "Republic", etc.

def get_country(search_term):
    search_term = search_term.strip() # clean whitespace at the beginning and at the end
    # First search in valid_country_data_short
    search_term_upper = search_term.upper()
    for country, codes in valid_country_data_short.items():
        if search_term_upper in [code.upper() for code in codes]:
            return country
    
    # If not found, continue searching in valid_country_data
    for country, codes in valid_country_data.items():
        if search_term.lower() == country.lower() or search_term.lower() in [code.lower() for code in codes]:
            return country
    return None


def find_country_v1(input_country):
    input_country = input_country.strip().lower()  # Remove leading/trailing whitespace and convert to lowercase
    
    for country, abbreviations in valid_country_data.items():
        if input_country in [abbr.lower() for abbr in abbreviations.values()]:
            return country
    
    # Check if the input is a full country name
    for country, abbreviations in valid_country_data.items():
        if input_country == country.lower():
            return country
    
    # Check if the input is an abbreviation or part of an abbreviation
    for country, abbreviations in valid_country_data.items():
        for abbreviation in abbreviations.values():
            if input_country in abbreviation.lower():
                return country
    
    return None  # Return None if no match is found



