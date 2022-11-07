import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
from Homepage import filter_by_texboxes
from Homepage import load_data


st.title("Gráficas")


data = load_data(500)
if 'employeeIdFilter' not in st.session_state:
    st.session_state.employeeIdFilter = ''
    st.session_state.homeTownFilter = ''
    st.session_state.unitFilter = ''
    st.session_state.sel_educational_levl = 0
print(st.session_state.homeTownFilter.upper())
dataFiltered = filter_by_texboxes(data, st.session_state.employeeIdFilter.upper(), st.session_state.homeTownFilter.upper(), st.session_state.unitFilter.upper(), int(st.session_state.sel_educational_levl))




sidebar_obj = st.sidebar
chkBox0 = sidebar_obj.checkbox('Histograma de empleados por edad')
chkBox1 = sidebar_obj.checkbox('Grafica Frencuencia por Unidad')
chkBox2 = sidebar_obj.checkbox('Mostrar Deserción por ciudad')
chkBox3 = sidebar_obj.checkbox('Mostrar Deserción por edad')
chkBox4 = sidebar_obj.checkbox('Mostrar Tiempo de servicio y Deserción')

fig, ax = plt.subplots()
if chkBox0:
    st.header("Histograma del empleados por edad")
    fig = plt.figure()

    plt.hist(x=dataFiltered['Age'], rwidth=.98, bins=[10, 20, 30, 40, 50, 60, 70])
    plt.title('Hostograma por Edad')
    plt.xlabel('Edades')
    plt.ylabel('Frecuencia')
    st.pyplot(fig)


if chkBox1:
    fig = plt.figure()

    employees_clean_df = dataFiltered['Unit'].value_counts()
    employees_clean_df.plot(kind = 'bar')

    for i in range(employees_clean_df.shape[0]):
        plt.text(i, employees_clean_df[i], employees_clean_df[i], fontsize=8)
    
    st.pyplot(fig)

if chkBox2:
    st.write(f"Total Empleados : {dataFiltered.shape[0]}")

    dataFiltered = dataFiltered.dropna()
    st.write(f"Total Empleados : {dataFiltered.shape[0]}")

    employees_by_hometown = dataFiltered[dataFiltered.columns].groupby(['Hometown']).mean()
    st.write(employees_by_hometown)
    st.bar_chart(employees_by_hometown['Attrition_rate'])


if chkBox3:
    st.write(f"Total Empleados : {dataFiltered.shape[0]}")
    dataFiltered = dataFiltered.dropna()

    plt.scatter(x=dataFiltered['Age'], y=dataFiltered['Attrition_rate'])
    plt.title('Gráfico Relación de deserción y edad')
    plt.xlabel('Edad')
    plt.ylabel('Tasa de deserción')
    st.pyplot(fig)

if chkBox4:
    plt.scatter(x=dataFiltered['Time_of_service'], y=dataFiltered['Attrition_rate'],  alpha=0.5)
    plt.title('Gráfico feo')
    plt.xlabel('x')
    plt.ylabel('y')
    st.pyplot(fig)
