import streamlit as st
import pandas as pd
import openpyxl
import seaborn as sns
import pygwalker as pyg
import sys

st.set_page_config(page_title='EDA', page_icon='D:\coding\Streamlite\download.png', layout="wide")
st.sidebar.write("****A) File upload****")
ft=st.sidebar.selectbox("File Type",["csv","Excel"])
upload_file=st.sidebar.file_uploader("upload file here")

if upload_file is not None:
    file_path = upload_file

    if ft == 'Excel':
        try:
            sheet_names = pd.ExcelFile(file_path,sheet_names=None,engine=openpyxl).keys()
            ss=None
            s=None
        except ValueError as ve:
            st.error(f"Error: {ve}")
            st.info("File is not recognized as an Excel file. Please upload a valid Excel file.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.info("Please check the file and try again.")
    elif ft =='csv':
        try:
            ss=None
            s=None
        except:
            st.info("File is not recoginsed")
            sys.exit()
    @st.cache_data
    def load_data(file_path,ft,ss,s):
        if ft == 'Excel':
            try:
                data=pd.read_excel(file_path,sheet_names=ss,header=s,engine="openpyxl")
            except:
                st.info("file is not recognised as an excel file.")
                sys.exit()
        elif ft == 'csv':
            try:
                data =pd.read_csv(file_path)
            except:
                st.info("file is not recoginsed on csv file")
                sys.exit()

            return data
        
    data=load_data(file_path,ft,ss,s)
    st.write("Data Preview")


    try:
        st.dataframe(data,use_container_width=True)
    except:
        st.info("the file wasn't read properly .please ensure input parameter are crrecty defined")
        sys.exit()
    selected =st.sidebar.radio("what would you like to know about data",
                               ["Data Dimensions",
                               "Summary Statistics",
                               "value Counts of Fileds"])
    if selected == 'Summary Statistics':
        sh = pd.DataFrame(data.describe(include='all').round(2).fillna(''))
        st.dataframe(sh,use_container_width=True)
    elif selected == 'value Counts of Fileds':
        sub_selected = st.sidebar.radio("which best train",data.select_dtypes('object').columns)   
        vc = data[sub_selected].value_counts().reset_index().rename(columns={'count':'Count'}).reset_index().rename(columns={'count':'Count'}).reset_index(drop=True)
        st.dataframe(vc,use_container_width=True)
    else:
        st.write('The data has the dimenison:',data.shape)

    eda_select =st.sidebar.checkbox("EDA")

    if eda_select:
        walker =pyg.walk(data,return_html=True)
        html_content = walker.to_html()
        st.components.v1.html(html_content,width=1000,height=900)

        
    
   