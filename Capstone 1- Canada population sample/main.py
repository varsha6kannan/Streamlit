import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

@st.cache_data
def read_data():
    df=pd.read_csv("quarterly_canada_population.csv", dtype={"Quarter":str, "Canada":np.int32, "Newfoundland and labrador":np.int32,"Prince Edward Island":np.int32,
                "Nova Scotia":np.int32,"New Brunswick":np.int32,"Quebec":np.int32,"Ontario":np.int32,"Manitoba":np.int32, "Saskatchewan":np.int32,
                "Alberta":np.int32, "British Columbia":np.int32,"Yukon":np.int32, "Northwest Territories":np.int32,"Nunavut":np.int32
    })
    return df

@st.cache_data
def quarter_info(date):
    if date[1]==2:
        return float(date[2:])+0.25
    elif date[1]==3:
        return float(date[2:])+0.5
    elif date[1]==4:
        return float(date[2:])+0.75
    else:
        return float(date[2:])
    
@st.cache_data   
def compare_dates(start,end):
    new_start_date=quarter_info(start)
    new_end_date=quarter_info(end)

    if new_start_date>new_end_date:
        return True
    else:
        return False

# python logic to display the dashboard based on the selected options:
def display_dashboard(start_date,end_date,target):
    tab1, tab2= st.tabs(["Population change", "Compare"])

    with tab1:
        st.subheader(f"Population change from {start_date} to {end_date}")
        col1, col2=st.columns(2)

        with col1:
            initial_population=df.loc[df["Quarter"]==start_date,target].item()
            final_population=df.loc[df["Quarter"]==end_date, target].item()

            percentage=round(((final_population-initial_population)/final_population)*100,2)
            delta=f"{percentage}%"

            st.metric(label=start_date,value=initial_population)
            st.metric(label=end_date, value=final_population, delta=delta, delta_color="normal")

        with col2:
            start_idx=df.loc[df["Quarter"]==start_date].index.item()
            end_idx=df.loc[df["Quarter"]==end_date].index.item()
            filtered_df=df.loc[start_idx:end_idx+1]

            fig,ax = plt.subplots()
            ax.plot(filtered_df["Quarter"],filtered_df[target])
            ax.set_xlabel("Time")
            ax.set_ylabel("Population")
            ax.set_xticks([filtered_df["Quarter"].iloc[0],filtered_df["Quarter"].iloc[-1]])
            fig.autofmt_xdate()

            st.pyplot(fig)

        with tab2:
            st.subheader("Compare with other regions")
            multiselect=st.multiselect("Select the locations to compare", options= filtered_df.columns[1:], default=[target])

            fig,ax= plt.subplots()
            for each in multiselect:
                ax.plot(filtered_df["Quarter"],filtered_df[each])
            ax.set_xlabel("Time")
            ax.set_ylabel("Population")
            ax.set_xticks([filtered_df["Quarter"].iloc[0],filtered_df["Quarter"].iloc[-1]])
            fig.autofmt_xdate()

            st.pyplot(fig)


if __name__=="__main__":
    df=read_data()

    st.title("Population of Canada")
    st.markdown("Source table can be found at this website [here](https://www150.statcan.gc.ca/n1/pub/71-607-x/71-607-x2018005-eng.htm)")

    with st.expander("Select to view the full table"):
        st.dataframe(df)

    with st.form(key="my_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### Choose a starting date")
            st.write("Quarter")
            start_date_select=st.selectbox("Select a quarter", options=["Q1","Q2","Q3","Q4"], key="quarter_select_1", index=2)
            start_date_slider=st.slider("Year",min_value=1991, max_value=2023,key="first_slider")

        with col2:
            st.markdown("### Choose a ending date")
            st.write("Quarter")
            end_date_select=st.selectbox("Select a quarter", options=["Q1","Q2","Q3","Q4"], key="quarter_select_2", index=3)
            end_date_slider=st.slider("Year",min_value=1991, max_value=2023,key="second_slider")

        with col3:
            st.markdown("### Choose a Location")
            st.write("Location")
            location_select=st.selectbox("Select a location", options=df.columns[1:], key="location_select")

        submit_btn=st.form_submit_button("Analyze",type="primary")

    #python logic to get the quarter of the year- 1991.25 like that
    start_date= f"{start_date_select} {start_date_slider}"
    end_date=f"{end_date_select} {end_date_slider}" 

    if start_date not in df["Quarter"].to_list() or end_date not in df["Quarter"].to_list():
        st.error("Please re-check your date")
    elif compare_dates(start_date,end_date):
        st.error("End date should be lesser than start date")
    else:
        display_dashboard(start_date,end_date,location_select)


