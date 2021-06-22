import requests
import json 
import pandas as pd
import matplotlib.pyplot as plt

def covidcasesdata():
    data = ((requests.get("https://api.covid19india.org/state_district_wise.json")).json())
    states = []

    for key in data.items():
        states.append(key[0])

    for state in states:
        # try this before you go through the code 
        #print(state)
        #print("\n")
        #print(data[state]["districtData"])
        #print("\n")
        #print("\n")

        subdata = data[state]["districtData"]
        complete_data = []
        all_district_in_state = []
        total_active , total_confirmed , total_death  , total_recovered = 0 , 0 , 0 , 0

        for  key in (data[state]["districtData"]).items():
            district = key[0]
            all_district_in_state.append(district)
            active = subdata[district]["active"]
            confirmed = subdata[district]["confirmed"]
            deaths = subdata[district]["deceased"]
            recovered = subdata[district]["recovered"]
            if district == "Unknown":
                active , confirmed , deaths , recovered = 0,0,0,0
            complete_data.append([active , deaths , confirmed , recovered])
            total_active = total_active +active
            total_confirmed = total_confirmed + confirmed
            total_death = total_death + deaths
            total_recovered = total_recovered + recovered
        
        complete_data.append([total_active,total_death,total_confirmed,total_recovered])
        all_district_in_state.append("Total")
        parameters = ["Active Cases","Deaths Comfirmed","Comfirmed Cases","Recovered Cases"]

        dataframe = pd.DataFrame(complete_data,all_district_in_state,parameters)
        print("*"*100)
        print("COVID-19 ",state," district wise data")
        print(dataframe)
        print("*"*100)
        print("\n")

        plt.bar(all_district_in_state,dataframe['Active Cases'],width=1.0,align='center')
        plt.xlabel("States")
        plt.ylabel("Active Cases")
        plt.title(f"{state} covid cases")
        fig = plt.gcf()
        fig.set_size_inches(10.5 , 5.5)
        plt.xticks(rotation = 75)
        plt.show()

        

        
if __name__ == "__main__":
    covidcasesdata()
