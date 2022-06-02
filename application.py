import streamlit as st
import pandas as pd
import numpy as np
import pickle

pickle_in = open('model.pkl', 'rb') 
model = pickle.load(pickle_in)



@st.cache()
def predict_function(distance_from_home, distance_from_last_transaction, ratio_to_median_purchase_price, repeat_retailer, used_chip, used_pin_number, online_order):
    prediction = model.predict([[distance_from_home, distance_from_last_transaction, ratio_to_median_purchase_price, repeat_retailer, used_chip, used_pin_number, online_order]])
    if prediction == 0:
        return "Not Fraud"
    else:
        return "Fraud"

def main():
    st.title("Credit Card Fraud Detection")
    dfh = st.number_input("Distance from Home")
    dflt = st.number_input("Distance from Last Transaction")
    rmp = st.number_input("Ratio to Median Purchase Price")
    rr = st.checkbox("reapet reatailer?")
    uc = st.checkbox("chip")
    up = st.checkbox("pin")

if __name__=='__main__': 
        main()