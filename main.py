import streamlit as st
import pandas as pd
import requests

# SMS API credentials and settings
username = 'CILANTRO'
password = 'bJdY6HzXA9'
sms_lang = 'E'  # 'E' for English, 'A' for Arabic
sms_sender = 'CILANTRO'  # Should be less than 12 characters
api_endpoint = 'https://smsvas.vlserv.com/KannelSending/service.asmx/SendSMSWithDLR'

# Function to send the SMS
def send_sms(api_endpoint, username, password, sms_text, sms_lang, sms_sender, sms_receiver):
    payload = {
        'Username': username,
        'Password': password,
        'SMSText': sms_text,
        'SMSLang': sms_lang,
        'SMSSender': sms_sender,
        'SMSReceiver': sms_receiver
    }

    try:
        response = requests.post(api_endpoint, data=payload)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return str(e)

# Streamlit app
st.title('SMS Sending Tool')

uploaded_file = st.file_uploader("Upload Excel File", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Preview of uploaded file:")
    st.dataframe(df)

    sms_template = st.text_area("Enter SMS template", "Hello [first_name], your promo code is [promocode].")

    if st.button('Send SMS'):
        results = []
        for index, row in df.iterrows():
            sms_text = sms_template.replace('[first_name]', str(row['first_name'])).replace('[promocode]', str(row['promocode']))
            sms_receiver = str(row['phone_number'])
            result = send_sms(api_endpoint, username, password, sms_text, sms_lang, sms_sender, sms_receiver)
            results.append({'phone_number': sms_receiver, 'message': sms_text, 'status': result})

        results_df = pd.DataFrame(results)
        st.write("SMS Sending Results:")
        st.dataframe(results_df)

# To run the app, save this file and run the following command in your terminal:
# streamlit run app.py