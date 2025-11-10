
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

musteringRulesDF = pd.read_csv('CSVs\MusteringRules.csv')


DetachmentsDF = pd.read_csv('csvs/DetachmentsDF.csv', sep = '|')
DatasheetsDF = pd.read_csv('csvs/DatasheetsDF.csv', sep = '|')
DataOptionsDF = pd.read_csv('csvs/DataOptionsDF.csv', sep = '|')

NameDict = DatasheetsDF[['id', 'name']].set_index('id').to_dict()['name']

selected_Units = pd.DataFrame(columns=['id', 'Unit Name', 'Quantity', 'Points'])
potCounts = {}

#only pull thorugh detahcments with muserting rules
activateDetats = musteringRulesDF.merge(DetachmentsDF, 'inner', on = 'id')
activateDetats = activateDetats.groupby('id').first().reset_index()[['id', 'name']]
detats = []

for i in range(len(activateDetats)):
    detats.append([activateDetats['id'][i], activateDetats['name'][i]])

def getTables(detID):
    global potCounts
    tables_html = []
    Headers = []
    _ = musteringRulesDF[musteringRulesDF['id'] == detID]
    dataTable = _
    for i in _['Pot'].unique():
        newTable = _[_['Pot'] == i]
        potCounts[i] = 0
        Headers.append(newTable['Header'].iloc[0])
        #you can only select one unit from this pot
        newNames = newTable['Unit'].replace(NameDict)
        newTable['Names'] = newNames
        newTable = newTable[['Unit', 'Names']].fillna('nan')
        newTable['Quantity'] = 0
        newTable['Quantity'] = newTable.apply(lambda row: f"""<button class='btn' onclick='updateQuantity(this, "minus", {row.name})'>-</button><span id='quantity_{row.name}'>{row["Quantity"]}</span><button class='btn' onclick='updateQuantity(this, "plus", {row.name})'>+</button>""", axis=1)
        newTableHTML = newTable.to_html(classes='data', index=False, border=0, escape = False)
        #add Html elements to the table
        tables_html.append(newTableHTML)
    return Headers, dataTable, tables_html

def clear_selections(): 
    global selected_Units 
    selected_Units = pd.DataFrame(columns=['id', 'Unit Name', 'Quantity', 'Points'])

def update_selections(id, action):

    def addUnit(id):
        global selected_Units 
        newRow = {'id': [id], 'Unit Name': [NameDict[int(id)]], 'Quantity':[''] , 'Points':['']}
        selected_Units = pd.concat([selected_Units, pd.DataFrame(newRow)]).reset_index(drop=True)
        potCounts[musteringRulesDF[musteringRulesDF['Unit'] == int(id)]['Pot'].iloc[0]] += 1
        print(potCounts)
    
    global selected_Units 
    #get the value counts of the units we've selected, then check if we've selected this unit before
    counts = selected_Units['id'].value_counts()
    if action == 'plus':
        unitlimit = musteringRulesDF[musteringRulesDF['Unit'] == int(id)]['Unit Limit'].iloc[0]
        potlimit = musteringRulesDF[musteringRulesDF['Unit'] == int(id)]['Pot Limit'].iloc[0]
        potCount = potCounts[musteringRulesDF[musteringRulesDF['Unit'] == int(id)]['Pot'].iloc[0]]
        if id in counts:
            count = counts[id]
            #if we're below both, we can add a new row
            if (count < unitlimit) and ((potlimit<0) or (potCount<potlimit)):
                addUnit(id)
                count = selected_Units['id'].value_counts()[id]
            return count, selected_Units.to_html(classes='data', index=False, border=0, escape = False)
        else:
            #if the unit isn't in the list then we can select it
            if (potlimit<0) or (potCount<potlimit):
                addUnit(id)
                count = selected_Units['id'].value_counts()[id]
                return count, selected_Units.to_html(classes='data', index=False, border=0, escape = False)
            else:
                return 0, selected_Units.to_html(classes='data', index=False, border=0, escape = False)
        #if we dont meet either condition, return the curretn values
    else:
        if id in counts:
            #drop the unit using the index position of ultimate row
            index_to_drop = selected_Units[selected_Units['id'] == id].index[-1]
            selected_Units = selected_Units.drop(index_to_drop).reset_index(drop=True)
            potCounts[musteringRulesDF[musteringRulesDF['Unit'] == int(id)]['Pot'].iloc[0]] -= 1
            #check to see if there are any units with the id still in the dataframe
            counts = selected_Units['id'].value_counts()
            if id in counts:
                count = selected_Units['id'].value_counts()[id]
            else:
                count = 0
            return count, selected_Units.to_html(classes='data', index=False, border=0, escape = False)
        return 0, selected_Units.to_html(classes='data', index=False, border=0, escape = False)
        
    

def getSelected():
    return selected_Units.to_html(classes='data', index=False, border=0, escape = False)


    

