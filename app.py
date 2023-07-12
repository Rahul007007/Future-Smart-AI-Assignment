import streamlit as st
from streamlit_chat import message
from model import *
st.title("Report Chatbot")

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I help you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

# container for response
response_container = st.container()
# container for user input
textcontainer = st.container()


with textcontainer:
    query = st.text_area("Report: ", key="input")
    if st.button("Submit"):
        with st.spinner("typing..."):
            pred_label = predict(query)

        st.session_state.requests.append(query)
        st.session_state.responses.append(pred_label)


with response_container:
    if st.session_state['responses']:

        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')