import pandas as pd

DatasheetsDF = pd.read_csv('http://wahapedia.ru/wh40k10ed/Datasheets.csv', 
                           delimiter = '|')
DatasheetsDF.to_csv('csvs/DatasheetsDF.csv', sep = '|')

DataAbilitiesDF = pd.read_csv('http://wahapedia.ru/wh40k10ed/Datasheets_abilities.csv',    
                              delimiter = '|')
DataAbilitiesDF.to_csv('csvs/DataAbilitiesDF.csv', sep = '|')

DataKeywordsDF = pd.read_csv('http://wahapedia.ru/wh40k10ed/Datasheets_keywords.csv',    
                             delimiter = '|')
DataKeywordsDF.to_csv('csvs/DataKeywordsDF.csv', sep = '|')


DataModelsDF = pd.read_csv('http://wahapedia.ru/wh40k10ed/Datasheets_models.csv', 
                            delimiter = '|')
DataModelsDF.to_csv('csvs/DataModelsDF.csv', sep = '|')


DataOptionsDF = pd.read_csv('http://wahapedia.ru/wh40k10ed/Datasheets_options.csv', 
                            delimiter = '|')
DataOptionsDF.to_csv('csvs/DataOptionsDF.csv', sep = '|')


DataWargearDF = pd.read_csv('http://wahapedia.ru/wh40k10ed/Datasheets_wargear.csv', 
                            delimiter = '|')
DataWargearDF.to_csv('csvs/DataWargearDF.csv', sep = '|')


DataUnitCompDF = pd.read_csv('http://wahapedia.ru/wh40k10ed/Datasheets_unit_composition.csv', 
                             delimiter = '|')
DataUnitCompDF['description'] =  DataUnitCompDF['description'].apply(lambda x: x.replace(' – <span class="kwb">EPIC</span> <span class="kwb">HERO</span>', ''))
DataUnitCompDF.to_csv('csvs/DataUnitCompDF.csv', sep = '|')


DataModelCostDF = pd.read_csv('http://wahapedia.ru/wh40k10ed/Datasheets_models_cost.csv', 
                              delimiter = '|')
DataModelCostDF.to_csv('csvs/DataModelCostDF.csv', sep = '|')


StratsDF = pd.read_csv('http://wahapedia.ru/wh40k10ed/Stratagems.csv', 
                      delimiter = '|')
StratsDF.to_csv('csvs/StratsDF.csv', sep = '|')

EnhancemnetsDF = pd.read_csv('http://wahapedia.ru/wh40k10ed/Enhancements.csv', 
                           delimiter = '|') 
EnhancemnetsDF.to_csv('csvs/EnhancemnetsDF.csv', sep = '|')

DetachmentsDF = pd.read_csv('http://wahapedia.ru/wh40k10ed/Detachments.csv', 
                             delimiter = '|')
DetachmentsDF = DetachmentsDF[DetachmentsDF['type'] == 'Boarding Actions']  
DetachmentsDF.to_csv('csvs/DetachmentsDF.csv', sep = '|')

DetAbilitiesDF = pd.read_csv('http://wahapedia.ru/wh40k10ed/Detachment_abilities.csv', 
                             delimiter = '|') 
DetAbilitiesDF.to_csv('csvs/DetAbilitiesDF.csv', sep = '|') 



