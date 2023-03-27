import streamlit as sl
import os
import joblib
import numpy as np
import pandas as pd
from loan_prediction_and_analysis import scaler

#Load Model
classifier = joblib.load('randomforestmodel.pkl')

sl.title(':red[LOAN] Validation App')
sl.header('Kindly Fill the form below......')

import requests

#Collecting user details 
with sl.form('loan_form',clear_on_submit=True):
    loan_amount_term = sl.number_input('Input Loan Term')
    credit_history = sl.radio('Input Credit History 1 or 0',[0,1])

    property_area = sl.radio('Input Property Area',{'Rural':0,'Semiurban':1,'Urban':2})
    property_dict = {'Rural':0,'Semiurban':1, 'Urban':2}
    property_area = property_dict[property_area]

    gender = sl.radio('Sex',['Male','Female'])
    gender_dict = {'Male':1,'Female':0}
    gender = gender_dict[gender]

    married = sl.radio('Are You Married',['Yes','No'])
    married_dict = {'Yes':1,'No':0}
    married =  married_dict[married]

    graduate = sl.radio('Are You a Graduate',['Yes','No'])
    graduate_dict = {'Yes':0,'No':1}
    graduate =  graduate_dict[graduate]

    employed = sl.radio('Are You Self Employed',['Yes','No'])
    employed_dict = {'Yes':1,'No':0}
    employed =  employed_dict[employed]

    dependents = sl.number_input('Input number of Dependents')
    applicantincome =  sl.number_input('Input Your Income')
    coapplicantincome =  sl.number_input('Input spouse income else input 0')
    loanamount = sl.number_input('Input Loan Amount')
    totalhouseincome = applicantincome + coapplicantincome

    scalable_data = [dependents,applicantincome,coapplicantincome,loanamount,totalhouseincome]
    scalable_data = np.reshape(scalable_data,(1,-1))
    transformed = scaler.transform(scalable_data)[0]

    user_data = [loan_amount_term,
                credit_history,
                property_area,
                gender,
                married,
                graduate,
                employed,
                transformed[0],
                transformed[1],
                transformed[2],
                transformed[3],
                transformed[4]
                ]
    bank = sl.selectbox('Bank',['First Bank of Nigeria','First City Monument Bank','Access Bank'])
    bank_dict = {'First Bank of Nigeria':'011','First City Monument Bank':'214','Access Bank':'044'}
    bank = bank_dict[bank]
    account_number=sl.text_input('Input Guarantor Account Number')
    phone = sl.text_input('Input Phone Number')

    
    submitted = sl.form_submit_button("Submit")
    if submitted:
        user_data = np.reshape(user_data,(1,-1))
        result = classifier.predict(user_data)
        if result == 1:
            sl.balloons()
            sl.markdown('You Successfully Qualify for A :blue[Loan] :heart_eyes:')
            resp = requests.get('https://maylancer.org/api/nuban/api.php', {
            'account_number':account_number,
            'bank_code': bank,
            }).json()
            if resp['status'] == 'Account number resolved':
                guarantor_name = resp['account_name']
                sl.markdown(f'Please wait while we contact {guarantor_name} to verify your details \
                    and upon approval the loan will be paid into the\
                        guarantor account :heart_eyes:')

            else:
                sl.markdown('Kindly verify the account details :disappointed:')
           
        else:
            sl.snow()
            sl.markdown('Your Loan Application :red[Failed] :disappointed:')
