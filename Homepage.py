import streamlit as st  
import pandas as pd
import numpy as np
import math as math


DATA_URL = ('Employees.csv')

st.set_page_config(
    page_title="Multipage App"  
)

st.title("Filtros")
st.sidebar.success("Select a page above")





@st.cache
def load_data(nrows):
    #data = pd.read_csv(DATA_URL, nrows=nrows)
    data = pd.read_csv(DATA_URL)
    return data



@st.cache
def filter_by_texboxes(data, employeeIdFilter, homeTownFilter, unitFilter, educationalLevlFilter):
    dyn_query = '1==1'
    
    if len(employeeIdFilter) > 0:
        dyn_query = '(Employee_ID.str.upper().str.contains(@employeeIdFilter))'
    if len(homeTownFilter) > 0:
        if len(dyn_query)>4:
            dyn_query = dyn_query + ' and (Hometown.str.upper().str.contains(@homeTownFilter))'
            print(dyn_query)
        else:    
            dyn_query = '(Hometown.str.upper().str.contains(@homeTownFilter))'
            print(dyn_query)
    if len(unitFilter) > 0:
        if len(dyn_query)>4:
            dyn_query = dyn_query + ' and (Unit.str.upper()==@unitFilter)'
            print(dyn_query)
        else:    
            dyn_query = '(Unit.str.upper()==@unitFilter)'
            print(dyn_query)
    if educationalLevlFilter > 0:
        if len(dyn_query)>4:
            dyn_query = dyn_query + ' and (Education_Level==@educationalLevlFilter)'
            print(dyn_query)
        else:    
            dyn_query = '(Education_Level==@educationalLevlFilter)'
            print(dyn_query)            
    print(dyn_query)
    if dyn_query == '1==1':
        return data
    return  data.query(dyn_query)

def createSelectBox(data, column):
    df = np.append(data[column].unique(), [' Todos..'])
    df.sort()
    return df


#Starting main program
data = load_data(500)
dataFiltered = ''

# Creating a side bar
sidebar_obj = st.sidebar

if sidebar_obj.checkbox('Mostrar tabla original'):
    st.subheader('Mostrando datos')
    st.write(data)

employeeIdFilter = sidebar_obj.text_input("Buscar por EmployeeID")
homeTownFilter = sidebar_obj.text_input("Buscar por HomeTown")
unitFilter = sidebar_obj.text_input("Buscar por Unidad")


edu_levl_df = createSelectBox(data, 'Education_Level')
sel_cities_df = createSelectBox(data, 'Hometown')
sel_unit_df = createSelectBox(data, 'Unit')


sel_educational_levl = sidebar_obj.selectbox("Seleccionar nivel educativo", edu_levl_df)
sel_cities = sidebar_obj.selectbox("Seleccionar ciudades", sel_cities_df)
sel_unit = sidebar_obj.selectbox("Seleccionar Unidades", sel_unit_df)


btnBuscar = st.sidebar.button('Buscar...')
if(btnBuscar):
    if(sel_educational_levl == ' Todos..'):
        sel_educational_levl = '0'

    if(sel_cities == ' Todos..'):
        sel_cities = '' 
    else:
        homeTownFilter = sel_cities

    if(sel_unit == ' Todos..'):
        sel_unit = '' 
    else:
        unitFilter = sel_unit

    if 'employeeIdFilter' not in st.session_state:
        st.session_state.employeeIdFilter = '.'
        st.session_state.homeTownFilter = '.'
        st.session_state.unitFilter = '.'
        st.session_state.sel_educational_levl = 0
        print('No los encuentra(1)..')
    print('Si los encontró(1)..')
   

    st.session_state.employeeIdFilter = employeeIdFilter
    st.session_state.homeTownFilter = homeTownFilter
    st.session_state.unitFilter = unitFilter
    st.session_state.sel_educational_levl = int(sel_educational_levl)
    

    dataFiltered = filter_by_texboxes(data, employeeIdFilter.upper(), homeTownFilter.upper(), unitFilter.upper(), int(sel_educational_levl))
    st.write(f"Total Empleados : {dataFiltered.shape[0]}")
    st.write(dataFiltered)