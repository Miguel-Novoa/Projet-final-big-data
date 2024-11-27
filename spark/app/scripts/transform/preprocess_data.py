from scripts.transform.storm_events import decompress_storm_events_files, preprocess_storm_events
from scripts.transform.gsod import clean_gsod_data


decompress_storm_events_files()
preprocess_storm_events()

years = range(2015, 2021)
clean_gsod_data(years)
