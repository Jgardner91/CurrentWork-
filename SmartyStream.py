import ast
import pandas as pd
import urllib.request
import requests
import json
from tabulate import tabulate
import requests
import streamlit as st


class SMARTY:
    def __init__(self):
        self.url = 'https://us-street.api.smartystreets.com/street-address?auth-id=8272ff28-79f0-3d14-d632-802a39a77bd5&auth-token=CV3uRryC5axrROq1vbXZ&license=us-core-cloud'

    def bulk_address(self,file_name):
        df = pd.read_csv(file_name)
        return_address = []

        for i, row in df.iterrows():
            street = row['street']
            city = row['city']
            state = row['state']

            skeleton_dict = {"street":street,"city":city,"state":state}
            return_address.append(skeleton_dict)

        OBJ = json.dumps(return_address,default=str)

        try:
            req = requests.post(self.url,data=OBJ)
            print(req)
        except Exception as E:
            print("Error: ",E)

        req_json = req.json()

        
        return req_json 

    def single_address(self,street,city,state):

            
        
        skeleton_dict = [{"street":street,"city":city,"state":state}]
        OBJ = json.dumps(skeleton_dict,default=str)
        req = requests.post(self.url,data=OBJ)
        req_json = req.json()
        df = pd.DataFrame(req_json[0])
        st.table(df[['components','input_index','candidate_index']])
        return None 









if __name__ == '__main__':

    smart = SMARTY()
    table = smart.bulk_address("SampleDataX.csv")
    st.title("Smarty Streets Helper")
    

    OPT_1 = st.selectbox(
     '---Search Options---',
     ('Search', 'BULK ADDRESS', 'SINGLE ADDRESS'))

    if OPT_1 == 'BULK ADDRESS':
        table = smart.bulk_address("SampleDataX.csv")
        returned = len(table)
        temp_list = [i for i in range(returned)]
        opts = tuple(temp_list)
        OPT_2 = st.selectbox('---Chose Frome List---',opts)
        df = pd.DataFrame(table[int(OPT_2)])
        st.table(df[['components','input_index','candidate_index']])

    if OPT_1 == 'SINGLE ADDRESS':

        col1, col2, col3 = st.columns(3)
        with col1:
            street = st.text_input("--Street--","1410 Spring Hill Rd")
        with col2:
            city = st.text_input("--City--", "McLean")
        with col3: 
            state = st.text_input("--State--","Virginia")
        smart.single_address(street,city,state)



        




 