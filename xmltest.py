# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 22:09:15 2025

@author: Georg
"""

import CacheBSData

parsed = CacheBSData.getFaction("AE")
allUnits = parsed['sharedSelectionEntries']['selectionEntry']
musteringRules = CacheBSData.musteringRules

#Aelari test
autarchWayleaper = '497a-263e-966a-5a15'
strikingScorpions = 'c90f-a8e5-6afa-eb91'
stormGuardians = '5452-c4a7-59fb-f05c'
warlockConclave = 'd61-c058-6bd1-112f'
warpSpiders = '57ec-47a8-a59a-6a46'

#AM Test
cadians = 'a2aa-7688-dcb1-4132'


unitsToSelect = [autarchWayleaper, 
                 strikingScorpions, 
                 stormGuardians,
                 warlockConclave,
                 warpSpiders]



"""
cadian veteran guards man profile 
if eab2-28bb-3bf5-8179
type id c547-1836-d8a-ff4f


ea09-3364-e6cd-2ffe

"""



#unitsToSelect = [cadians]

selectedUnits = {}
selectableUnits = {}

ignoreList = ['Warlord']

def findEntryWithID(ID, dicToCheck = allUnits, AuditString = ""):
    """
    Recursively interates through a dictionary's value to find and dictionarys
    where the type is model
    """
    if type(dicToCheck) == dict:
        print('is a dict')
        #check to see if the dictionary relates to a model
        if '@name' in dicToCheck:
            AuditString += dicToCheck['@name'] +'/'
        if '@id' in dicToCheck and dicToCheck['@id'] == ID:
            print(AuditString)
            print(dicToCheck['@name'])
        for value in dicToCheck.values():
                findEntryWithID(ID)
    elif type(dicToCheck) == list:
        print('not a dict')
        for i in dicToCheck:
            print(i)
            findEntryWithID(ID)

def findFusionGun(dicToCheck, AuditString):
    """
    Recursively interates through a dictionary's value to find and dictionarys
    where the type is model
    """
    if type(dicToCheck) == dict:
        #check to see if the dictionary relates to a model
        if '@name' in dicToCheck:
            AuditString += dicToCheck['@name'] +'/'
            if 'Guardsman' in dicToCheck['@name']:
                print(AuditString)
        for value in dicToCheck.values():
                findFusionGun(value, AuditString)
    elif type(dicToCheck) == list:
        for i in dicToCheck:
            findFusionGun(i, AuditString)

def getSelections(diht):
    return diht['selectionEntries']['selectionEntry']
    
def checkDictForModel(dicToCheck, resultDict):
    """
    Recursively interates through a dictionary's value to find and dictionarys
    where the type is model
    """
    def getMinMax(dicToCheck):
        #check the constraints to see how many of each model is allowed
        maxModels = 1
        minModels = 1
        #if there are no constraints, assume only 1 can be selected
        if 'constraints' in dicToCheck:
            constraints = dicToCheck['constraints']['constraint']
            if type(constraints) == list:
                for constraint in constraints:
                    #constraints with scope of parent refer to the number of 
                    #of the unit in question can be selected 
                    if constraint['@scope'] == 'parent':
                        if constraint['@type'] == 'max':
                            maxModels = constraint['@value']
                        elif constraint['@type'] == 'min':
                            minModels = constraint['@value']
            #if the constraints aren't a list, then there is only one constraint
            #we need to check if it is a max, if so then min can be assumed
            #to be zero
            elif type(constraints) == dict:
                if constraints['@scope'] == 'parent':
                    if constraints['@type'] == 'max':
                        maxModels = constraints['@value']
                        minModels = 0 
        return maxModels, minModels
    
    def getWeapons(dicToCheck):
        """
        arg: dicToCheck - the top level dictionary of a unit
        
        functionaity - creates a dictionary of dictionaries, where each index 
        value corresponds to a wargear option. dictionary shows min and max 
        values of the 
        """
        def getWeaponData(allWeaponDict, weapon):
            
            options = {}
            optionDict = {}
            optionDict['@max'], optionDict['@min'] = getMinMax(weapon)
            if 'profiles' in weapon.keys():
                weaponProfiles = weapon['profiles']['profile']
                weaponProfiles = weaponProfiles['characteristics']['characteristic']
            elif '@characteristics' in weapon.keys(): 
                weaponProfiles = weapon['@characteristics']['characteristic']
            else:
                #profile is not a weapon as we cant find characteristics for it
                return
            weaponDict = {}
            weaponDict['@data'] = weapon
            weaponDict['@name'] = weapon['@name']
            weaponDict['@id'] = weapon['@id']
            weaponDict['characteristic'] = weaponProfiles
            options[0] = weaponDict
            optionDict[0] = options
            weaponID = 0
            while weaponID in allWeaponDict.keys():
                weaponID += 1
            allWeaponDict[weaponID] = optionDict
        
        def getWeaponOptions(allWeaponDict, weapon):
            #gets the weapon options from a dictionary
            optionDict = {}
            selections = weapon['selectionEntries']['selectionEntry']
            optionDict['@max'], optionDict['@min'] = getMinMax(weapon)
            optionID = 0 
            #we iterate over the list of possible choices for this slot,
            #extracting all the porfiles for each potential selection
            if type(selections) != list:
                selections = [selections]
            for choice in selections:
                if 'selectionEntries' in choice:
                    profiles = choice['selectionEntries']['selectionEntry']
                else: 
                    profiles = [choice]
                for profile in profiles:
                    weaponDict = {'@data': profile,
                                  '@name': profile['@name'],
                                  '@id': profile['@id']}
                    weaponProfiles = profile['profiles']['profile']
                    #get the charactersitics of the weapon
                    if type(weaponProfiles) == list:
                        #if the profiles is a list, the weapon has multiple 
                        #options to chose from 
                        for profile in weaponProfiles:
                            if 'characteristics' in profile:
                                weaponProfiles = profile['characteristics']['characteristic']
                        weaponDict['characteristic'] = weaponProfiles
                    else:
                        #if its not a list, it must be a dictionary with 
                        #one characteristic option
                        weaponProfiles = weaponProfiles['characteristics']['characteristic']
                        weaponDict['characteristic'] = weaponProfiles
                #increase the optionID by 1 so that all choice slots have a 
                #unique key
                while optionID in optionDict:
                    optionID += 1
                optionDict[optionID] = weaponDict  
             
            #check if there are any generic options that can be taken
            if 'entryLinks' in weapon:
                commonWeapons = weapon['entryLinks']['entryLink']
                if type(commonWeapons) != list:
                    commonWeapons = [commonWeapons]
                for weapon in commonWeapons:
                    for entry in allUnits:
                        if entry['@id'] == weapon['@targetId']:
                            while optionID in optionDict:
                                optionID += 1
                            optionDict[optionID] = entry   
            
            z = 0 
            while z in optionDict:
                optionDict[z]['@selected'] = 0
                z += 1
            
            weaponID = 0
            while weaponID in allWeaponDict.keys():
                weaponID += 1
            allWeaponDict[weaponID] = optionDict
            

        def checkForGenericOptions(dicToCheck, allWeaponDict):
            commonWeapons = dicToCheck['entryLinks']['entryLink']
            #if it is not a list, there is only one item, convert it to a one 
            #item list for readability
            if type(commonWeapons) != list:
                commonWeapons = [commonWeapons]
            for weapon in commonWeapons:
                for entry in allUnits:
                    if entry['@id'] == weapon['@targetId']:
                        getWeaponData(allWeaponDict, entry)
            
        #initialise dictionary to store the all the weapon data nd options
        allWeaponDict = {}
        #weapons that share profiles across multiple units and models are
        #stored at the top level of the catalogue
        if 'entryLinks' in dicToCheck:
            checkForGenericOptions(dicToCheck, allWeaponDict)

        #if the model has weapons or upgrades that are not on the top level, 
        #we check for those as well
        if 'selectionEntries' in dicToCheck:
            selectionEntries = dicToCheck['selectionEntries']['selectionEntry']
            #if the item is not a list, that means there is only one weapon
            #we convert it to a list with one item for readability
            if type(selectionEntries) != list:
                selectionEntries = [selectionEntries]
            for weapon in selectionEntries:
                getWeaponData(allWeaponDict, weapon)  
        elif 'selectionEntryGroups' in dicToCheck: 
            selectionEntries = dicToCheck['selectionEntryGroups']['selectionEntryGroup']
            print('selectionEntryGroups in model profile')     
            print(selectionEntries['@name'], type(selectionEntries))
            if 'entryLinks' in selectionEntries:
                checkForGenericOptions(selectionEntries, allWeaponDict)
            if 'selectionEntries' in selectionEntries:
                #model has options that it can take, but only one slot for them
                getWeaponOptions(allWeaponDict, selectionEntries)
            if 'selectionEntryGroups' in selectionEntries:
                #model has multiple slots with multiple options
                testProfiles = selectionEntries['selectionEntryGroups']['selectionEntryGroup']
                if type(testProfiles) != list:
                    testProfiles = [testProfiles]
                for profile in testProfiles:
                    getWeaponOptions(allWeaponDict, profile)
                
        return allWeaponDict
     
    def getModelData(Dict):
        print('Getting data for Model: {}'.format(Dict['@name']))
        modelDict = {}
        modelDict['@name'] = Dict['@name']
        #retain the unmodified data for debugging purposes
        modelDict['@data'] = Dict
        #get max and min available models
        modelDict['@max'], modelDict['@min'] = getMinMax(Dict)
        modelDict['selected'] = modelDict['@min']
        #get the updgrades and weapons data for each model
        modelDict['Weapons'] = getWeapons(Dict)
        return modelDict
    
    """
    code starts here
    """
    
    if type(dicToCheck) == dict:
        #check to see if the dictionary relates to a model
        allModels = {}
        modelsForSlot = {}
        if '@type' in dicToCheck:
            if dicToCheck['@type'] == 'model':
                #top level dictionary is model, the unit is a character with 1
                #possible selection
                print(dicToCheck['@name'])
                #initialise new dictionary to store the model data
                modelDict = getModelData(dicToCheck)
                allModels = {0: modelsForSlot}
                modelsForSlot['@max'], modelsForSlot['@min'] = getMinMax(dicToCheck)
                modelsForSlot[0] = modelDict
            elif dicToCheck['@type'] == 'unit':
                if 'selectionEntryGroups' in dicToCheck:
                    #selection entry groups group together selectable units
                    selections = dicToCheck['selectionEntryGroups']['selectionEntryGroup']
                    if type(selections) != list:
                        #if it is not a list, make it one so that the below code works
                        onlyChoice = selections['selectionEntries']['selectionEntry']
                        modelsForSlot['@max'], modelsForSlot['@min'] = getMinMax(onlyChoice)
                        selections = [selections]
                    for slot in selections:
                        #choices will be the 'slots' we can take models in,
                        #each of them containing data for the models
                        modelsForSlot = {}
                        if 'constraints' in slot:
                            #check whether the slot has constraints at the top
                            #level, as this will act a a limiter for all
                            #the child choices
                            modelsForSlot['@max'], modelsForSlot['@min'] = getMinMax(slot)
                        #selectionentries contains the possible choices for the 
                        #slot
                        choices = slot['selectionEntries']['selectionEntry']
                        if type(choices) != list:
                            modelsForSlot['@max'], modelsForSlot['@min'] = getMinMax(choices)
                            choices = [choices]
                        for choice in choices:
                            #slots with single models have to be stored in a 
                            #dictionary to ensure symmetry in cases where there
                            #are sub choices
                            modelData = getModelData(choice)
                            choiceDict = {'@name': modelData['@name'],
                                          '@max': modelData['@max'],
                                          '@min': modelData['@min'],
                                          0: modelData}
                            choiceID = 0
                            while choiceID in modelsForSlot:
                                choiceID += 1           
                            modelsForSlot[choiceID] = choiceDict
                        if 'selectionEntryGroups' in slot:
                            #check if there are any subgroups that need to be 
                            #pulled out
                            subSlot = slot['selectionEntryGroups']['selectionEntryGroup']
                            subChoices = subSlot['selectionEntries']['selectionEntry']
                            allSubChoices = {}
                            subChoice = {'@name': subSlot['@name']} 
                            for choice in subChoices:
                                subChoice['@max'], subChoice['@min'] = getMinMax(choice)
                                subChoiceID = 0
                                while subChoiceID in subChoice:
                                    subChoiceID += 1
                                subChoice[subChoiceID] = getModelData(choice)
                            allSubChoices[0] = subChoice
                            choiceID = 0
                            while choiceID in modelsForSlot:
                                choiceID += 1
                            modelsForSlot[choiceID] = subChoice
                        
                        #finally, take the collected model data and put it in 
                        #the appropriate spot
                        slotID = 0
                        while slotID in allModels:
                            slotID += 1
                        allModels[slotID] = modelsForSlot
            
                if 'selectionEntries' in dicToCheck:
                    entry = dicToCheck['selectionEntries']['selectionEntry']
                    entryData = getModelData(entry)
                    entryDict = {'@max': entryData['@max'],
                                 '@min': entryData['@min'],
                                  0: entryData}
                    choiceID = 0
                    while choiceID in allModels:
                        choiceID += 1           
                    allModels[choiceID] = entryDict
                    
                                                  
            resultDict['modelSelections'] = allModels
                            
        elif 'selectionEntryGroups' in dicToCheck:
            comps = dicToCheck['selectionEntryGroups']['selectionEntryGroup']
            if type(comps) == dict and comps['@name'] == 'Unit Composition':
                #TODO set up code to work when unit has multiple selections
                #for models
                print("Attacked by a penugs fish?")
        """                        
        for value in dicToCheck.values():
            #Check the vlues of the dictionary for any further models
                checkDictForModel(value, resultDict)
        """
    #if its a list, we need to iterate through the values to make sure we have 
    #missed any models
    elif type(dicToCheck) == list:
        for i in dicToCheck:
            checkDictForModel(i, resultDict)

def checkUnitEligable(unitID):
    #TODO write process to check unit can be added
    return True

def addUnit(unitID):
    unit = selectableUnits[unitID]
    print('-----')
    print("Attempting to add {}".format(unit['@name']))
    if checkUnitEligable(unit):
        #once we chack the unit can be added, we assign a key based on the 
        #lowest available number
        currIDs = selectedUnits.keys()
        assignedID = 0
        while assignedID in currIDs:
            assignedID += 1
        #create dictionary object to store the data
        unitDict = {'@name': unit['@name'],
                    '@id': unit['@id']}
        checkDictForModel(unit, unitDict)
        selectedUnits[assignedID] = unitDict
   
def getRules(detachmentID):
    global selectableUnits
    selectableUnits = {}
    global a
    a = 123
    rules = CacheBSData.getMusteringRules(detachmentID)  
    unitList = list(rules['Unit'])
    for unit in allUnits:
        if unit['@id'] in unitList:
            selectableUnits[unit['@id']] = unit

def testDetachment(detachmentID):
    gotRules = False
    addedUnits = False
    try:
        getRules(detachmentID)
        gotRules = True
        print('Got Detachment Rules')
    except: 
        print('Could not get detachment rules')
    if gotRules:
        for unit in selectableUnits.values():
            try: 
                addUnit(unit['@id'])
                addedUnits = True
                print('   Got Data for {}'.format(unit['@name']))
            except:
                print('   Could not select {}'.format(unit['@name']))    
    if addedUnits:
        print('-------')        
        print('Checking Data')
        for selectedUnit in selectedUnits.values():
            try:
                print('------')
                print(selectedUnit['@name'])
            except:
                print('cant print name')
                continue
            try:
                models = selectedUnit['modelSelections']
                i = 0 
                while i in models:
                    print('   Checking model slot {}'.format(i))
                    slot = models[i]
                    y = 0 
                    while y in slot:
                        print('      Model: {}'.format(slot[y]['@name']))
                        if 'Weapons' in slot[y]:
                            modelWeaponsSlots = slot[y]['Weapons']
                            z = 0
                            while z in modelWeaponsSlots:
                                print('         Checking Weapon Slot {}'.format(z))
                                weapons = modelWeaponsSlots[z]
                                q = 0
                                while q in weapons:
                                    for value in weapons[q].values():
                                        print('            {}'.format(value['@name']))
                                    q += 1
                                z += 1
                        else:
                            print("         Can't find weapons")
                        y += 1
                    i +=1
            except:
                print("Issue with data structure for {}".format(selectedUnit['@name']))
                    

                    
                    
            
def adHocGetUnits():           
    for unit in allUnits:
        if unit['@id'] in unitsToSelect:
            selectableUnits[unit['@id']] = unit 

testDetachment(919)
 

"""   
lines = []
for unit in allUnits:
    if unit['@type'] == 'model' or unit['@type'] == 'unit':
        lines.append([unit['@id'], unit['@name']])
    
import pandas as pd

unitData = pd.DataFrame(lines, columns = ['id', 'name'])
unitData.to_csv('modelData.csv')
"""

#testUnitWargear = testUnit['selectionEntryGroups']['selectionEntryGroup']['selectionEntryGroups']['selectionEntryGroup']