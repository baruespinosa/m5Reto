import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
from Homepage import filter_by_texboxes
from Homepage import load_data


# This method will work as a dynamic funcion, it depends of the filter
# the used makes, it will give the answer of the Analysis
def getMaxAttritionRateHometown(employees_by_hometown):
    max_rate_value = employees_by_hometown['Attrition_rate'].max()
    max_rate_df = employees_by_hometown.loc[employees_by_hometown['Attrition_rate'] == max_rate_value]

    for i in max_rate_df.index:
        st.text(f"Ciudad con mayor índice de deserción:{i}")
        st.text(f"Valor de tasa de deserción: {max_rate_value}")

st.title("Gráficas")
st.markdown('Desmarca la gráfica y marca la gráfica deseada.')

data = load_data(2)

# Using session state, so that we can get the value of the filters

if 'employeeIdFilter' not in st.session_state:
    st.session_state.employeeIdFilter = ''
    st.session_state.homeTownFilter = ''
    st.session_state.unitFilter = ''
    st.session_state.sel_educational_levl = 0


dataFiltered = filter_by_texboxes(data, st.session_state.employeeIdFilter.upper(), st.session_state.homeTownFilter.upper(), st.session_state.unitFilter.upper(), int(st.session_state.sel_educational_levl))

sidebar_obj = st.sidebar
chkBox0 = sidebar_obj.checkbox('Histograma de empleados por edad', value=True)
chkBox1 = sidebar_obj.checkbox('Mostrar frencuencia por unidad')
chkBox2 = sidebar_obj.checkbox('Mostrar deserción por ciudad')
chkBox3 = sidebar_obj.checkbox('Mostrar deserción por edad')
chkBox4 = sidebar_obj.checkbox('Mostrar tiempo de servicio y deserción')

fig = plt.figure()

if chkBox0:
    st.header("Histograma del empleados por edad")
    st.markdown(f"Total empleados encontrados: {dataFiltered.shape[0]} ")
    
    plt.hist(x=dataFiltered['Age'], rwidth=.98, bins=[10, 20, 30, 40, 50, 60, 70])
    plt.title('Hostograma por Edad')
    plt.xlabel('Edades')
    plt.ylabel('Frecuencia')
    st.pyplot(fig)

if chkBox1:
    
    st.header("Gráfica de frecuencia por Unidad")
    st.subheader("No. Empleados por Unidad")
    st.markdown(f"Total empleados encontrados: {dataFiltered.shape[0]} ")

    employees_clean_df = dataFiltered['Unit'].value_counts()
    employees_clean_df.plot(kind = 'bar')

    for i in range(employees_clean_df.shape[0]):
        plt.text(i, employees_clean_df[i], employees_clean_df[i], fontsize=8)
    
    st.pyplot(fig)

if chkBox2:
    st.header("Mayor índice de deserción por ciudad")
    st.markdown(f"Total empleados encontrados: {dataFiltered.shape[0]} ")

    employees_by_hometown = dataFiltered[dataFiltered.columns].groupby(['Hometown']).mean()
    getMaxAttritionRateHometown(employees_by_hometown)
    
    st.write(employees_by_hometown[['Attrition_rate']])
    st.bar_chart(employees_by_hometown['Attrition_rate'])

if chkBox3:
    st.header("Análisis deserción por edad")
    st.markdown(f"Total empleados encontrados: {dataFiltered.shape[0]} ")

    #dataFiltered = dataFiltered.dropna()
    st.markdown("No existe correlación entre edad y tasa de deserción")
    
    plt.scatter(x=dataFiltered['Age'], y=dataFiltered['Attrition_rate'])
    plt.title('Gráfico de deserción y edad')
    plt.xlabel('Edad')
    plt.ylabel('Tasa de deserción')
    st.pyplot(fig)

if chkBox4:
    st.header("Análisis de deserción por tiempo de servicio")
    st.markdown(f"Total empleados encontrados: {dataFiltered.shape[0]} ")

    st.markdown("No existe correlación entre tiempo de servicio y tasa de deserción")
    plt.scatter(x=dataFiltered['Time_of_service'], y=dataFiltered['Attrition_rate'],  alpha=0.5)
    
    plt.xlabel('Tiempo de servicio')
    plt.ylabel('Tasa de deserción')
    st.pyplot(fig)