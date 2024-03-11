#!/usr/bin/python3

from napcountrydb import valid_country_data
from napcountrydb import valid_countries

valid_country_data_example = {
    'България': ['BG', 'BGR', 'Republic of Bulgaria'],
    'Австралия': ['AU', 'AUS', 'Commonwealth of Australia'],
    'Австрия': ['AT', 'AUT', 'Republic of Austria'],
    'Азербайджан': ['AZ', 'AZE', 'Republic of Azerbaijan']
}

valid_countries_example = ['България', 'Австралия', 'Австрия', 'Азербайджан']

def search_valid_country_data_left(valid_countries, valid_country_data):
    for country in valid_countries:
        if country in valid_country_data:
            print(f"{country} exists in valid_country_data.")
        else:
            print(f"{country} DOES NOT exists in valid_country_data.")


def search_valid_countries_in_data(valid_countries, valid_country_data):
    for country_left in valid_country_data:
        if country_left in valid_countries:
            print(f"{country_left} matches a country in valid_countries.")
        else:
            print(f"{country_left} DOES NOT matches a country in valid_countries.")


# Test the functions
print("Valid countries in valid_country_data:")
search_valid_country_data_left(valid_countries, valid_country_data)

print("\nCountries in valid_country_data matching with valid_countries:")
search_valid_countries_in_data(valid_countries, valid_country_data)

