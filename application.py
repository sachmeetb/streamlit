import streamlit as st
import pandas as pd
import numpy as np
import pickle
from google.cloud import aiplatform as aip

aip.init(project="aesthetic-rush-352008", location="us-central1",staging_bucket="cloud-ai-platform-9ce4bf1d-d8b8-41cf-92cb-1732efff16a0")


def predict_function(distance_from_home, distance_from_last_transaction, ratio_to_median_purchase_price, repeat_retailer, used_chip, used_pin_number, online_order):
    #prediction = model.predict([[distance_from_home, distance_from_last_transaction, ratio_to_median_purchase_price, int(repeat_retailer), int(used_chip), int(used_pin_number), int(online_order)]])
    prediction = dict(predict_tabular_classification_sample(
        project="1048826067215",
        endpoint_id="8272153741340180480",
        location="us-central1",
        instance_dict={ "distance_from_home":distance_from_home, 
            "distance_from_last_transaction": distance_from_last_transaction, 
            "ratio_to_median_purchase_price": ratio_to_median_purchase_price, 
            "repeat_retailer": int(repeat_retailer),
            "used_chip": int(used_chip),
            "used_pin_number": int(used_pin_number),
            "online_order": int(online_order) }
)[0])
    if prediction['scores'].index(max(prediction['scores'])) == 0:
        return "Not Fraud"
    else:
        return "Fraud"

from typing import Dict

from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value


def predict_tabular_classification_sample(
    project: str,
    endpoint_id: str,
    instance_dict: Dict,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aip.gapic.PredictionServiceClient(client_options=client_options)
    # for more info on the instance schema, please use get_model_sample.py
    # and look at the yaml found in instance_schema_uri
    instance = json_format.ParseDict(instance_dict, Value())
    instances = [instance]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/tabular_classification_1.0.0.yaml for the format of the predictions.
    predictions = response.predictions
    for prediction in predictions:
        print(" prediction:", dict(prediction))
    return predictions


def main():
    st.title("Credit Card Fraud Detection")

    with st.sidebar:
        st.image("https://m.foolcdn.com/media/affiliates/images/research-artdebit-and-credit-card-market-shar.width-1200_oL4ST5A.jpg")
        st.write("Welcome to Credit Card Fraud Validation, please use the fields provided, then click on Predict to check if the Credit Transaction was a fraud or not")
    dfh = st.number_input("Distance from Home")
    dflt = st.number_input("Distance from Last Transaction")
    rmp = st.number_input("Ratio to Median Purchase Price")
    rr = st.checkbox("Repeat Retailer?")
    uc = st.checkbox("Use of Chip?")
    up = st.checkbox("Use of PIN?")
    oo = st.checkbox("Online Transaction?")
    if st.button("Predict"):
        result = predict_function(dfh,dflt,rmp,rr,uc,up,oo)
        st.text(result)
if __name__=='__main__': 
        main()