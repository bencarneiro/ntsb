from fatalities.data_dictionary import FARS_DATA_DICTIONARY
from fatalities.models import City, County, State

def get_column_history(column):
    return FARS_DATA_DICTIONARY[column]

def get_data_source(column, year):
    for period in FARS_DATA_DICTIONARY[column]:
        if period['range']['start'] <= year and ((not period['range']['end']) or period['range']['end'] >= year):
            return period['key']
    return None

def get_multiple_data_sources(column, year):
    locations = []
    for period in FARS_DATA_DICTIONARY[column]:
        if period['range']['start'] <= year and ((not period['range']['end']) or period['range']['end'] >= year):
            locations += [period['key']]
    return locations
    
def get_county(state_id, county_id):
    return County.objects.get(state_id=state_id, county_id=county_id)
