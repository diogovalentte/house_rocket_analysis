import os
import folium
import pathlib
import geopandas
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from pandas.io.formats.format import DataFrameFormatter


st.set_page_config(layout="wide")


@st.cache_data(show_spinner=False)
def load_parquet_dataset(path: str):
    return pd.read_parquet(path)


@st.cache_resource(show_spinner=False)
def get_houses_map(_data: pd.DataFrame, only_to_puchase: bool):
    map_density = folium.Map(
        location=[_data["Latitude"].mean(), _data["Longitude"].mean()],
        default_zoom_start=20,
    )
    marker_cluster = MarkerCluster().add_to(map_density)
    for name, row in _data.iterrows():
        folium.Marker(
            [row["Latitude"], row["Longitude"]],
            popup="ID: {}, Price: {}, Year Built: {}, ZipCode: {}".format(
                row["ID"], row["Price"], row["Year Built"], row["ZipCode"]
            ),
        ).add_to(marker_cluster)
    return map_density


@st.cache_resource(show_spinner=False)
def get_price_per_region_map(_data: pd.DataFrame, only_to_puchase: bool):
    url = "https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson"
    geojson = geopandas.read_file(url)
    price_per_zipcode = (
        _data[["Price", "ZipCode"]].groupby("ZipCode").mean().reset_index()
    )
    geojson = geojson[geojson["ZIP"].isin(price_per_zipcode["ZipCode"].tolist())]
    map_price_zipcode = folium.Map(
        location=[_data["Latitude"].mean(), _data["Longitude"].mean()],
        default_zoom_start=20,
    )
    folium.Choropleth(
        data=price_per_zipcode,
        geo_data=geojson,
        columns=["ZipCode", "Price"],
        key_on="feature.properties.ZIP",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=-0.2,
        legend_name="Region Avarage Price",
    ).add_to(map_price_zipcode)
    return map_price_zipcode


class Dashboard:
    def __init__(self):
        self.ABS_PATH_TO_FOLDER = pathlib.Path(__file__).parent.resolve()
        self.renamed_houses = load_parquet_dataset(
            os.path.join(self.ABS_PATH_TO_FOLDER, "data/cleaned/houses_data.parquet")
        )
        self.recommended_houses = load_parquet_dataset(
            os.path.join(
                self.ABS_PATH_TO_FOLDER, "reports/data/final_houses_sale.parquet"
            )
        )

    def side_bar(self):
        st.sidebar.title("Select Page:")
        page_options = ["Final Reports", "Maps"]
        page_select = st.sidebar.selectbox(
            label="select_page", label_visibility="collapsed", options=page_options
        )
        if page_select == "Final Reports":
            st.sidebar.title("Filter the table with recommended houses to purchase:")
            id_input = str(
                st.sidebar.text_input(label="Enter the house ID:")
            ).strip()  # Input ID to search house
            self.page_final_reports(id_input)
        else:
            st.sidebar.title("Filter map:")
            filter_map = st.sidebar.radio(
                label="Filter map",
                label_visibility="collapsed",
                options=["All houses", "Recommended houses to buy"],
            )
            self.page_maps(filter_map)

    def page_final_reports(self, id_input):
        st.title("House Rocket Analysis")
        st.header(
            f"There are {self.renamed_houses.shape[0]} properties available for purchase today. Bellow is a table of the raw data:"
        )
        st.dataframe(self.renamed_houses)

        # Insights
        st.header("Main insights from the analysis:")
        st.markdown(
            """
            * The variables with the highest positive correlation with the price of the houses are:
                * Grade: indicates the quality of the building mateirais of the house.
                * Sqft living: the living square foot of the house.
                * The number of bathrooms in the house.
            * Houses with "Grade" 8 or higher have the best average price per building materials quality and number of homes.
            * The average price of renovated homes is 22% higher than unrenovated homes.
            * The best decision to renovate the houses would be to build a new bathroom as a new addition to the house, increasing the number of bathrooms in the house and the Square Foot of the House itself.
            * The best season of the year for re-selling homes is the Spring.
        """
        )

        # Main questions
        st.header("Which houses should the House Rocket buy?")
        st.markdown(
            """
            * Houses with Grade equal or greater than 8.
            * Houses with condition equal to or greater than 3.
            * Houses priced below the median price of their region (ZipCode).
        """
        )
        st.header("For which price the houses unrenovated should be sold?")
        st.markdown(
            """
            To find the price to sell a specific house, we need to define the Total Avarage Price. The Total Avarage Price is the mean of:

            1. The median price of houses with same ZipCode that this house.
            2. Avarage price of the houses that became avaiable on the same season of the year that this house.

            If the purchase price of the house is less than the "Total Avarage Price", the suggested selling price will be the purchase price + 30%. \n 
            If the purchase price of the house is higher than the "Total Avarage Price", the suggested selling price will be the purchase price + 10%.
        """
        )
        st.header("For which price the houses renovated should be sold?")
        st.write(
            """
            If the house is renovated, for example with a new bathroom, the re-sale price should be:

            If the purchase price of the house is less than the "Total Avarage Price", the suggested selling price will be the purchase price + 50%.\n
            If the purchase price of the house is higher than the "Total Avarage Price", the suggested selling price will be the purchase price + 30%.
        """
        )
        st.title(
            f"After analysis, {self.recommended_houses.shape[0]} properties are recommended for purchase and re-sale."
        )
        st.write("The following new columns were added to the dataset:")
        st.markdown(
            """
            * **Status**: if it's recommended to buy the house or not.
            * **Season**: the season of the year that the house become avaiable for purchase.
            * **Median Price Season**: the median price of the houses that become avaibale in that season of the year.
            * **Total Avarage Price**: the mean between the median price of the houses with same ZipCode and the avarage price of the houses of the same season of the year.
            * **Sale Price**: recommended price to sell the house if not renovated.
            * **Profit**: the possible profit if selling the unrenovated house by the recommended sale price.
            * **Renovated Sale Price**: recommended price to sell the house if renovated.
            * **Profit Renovation**: the possible profit if selling the renovated house by the recommended sale price.
        """
        )
        st.subheader(
            "The bellow table shows the final dataset with only the houses recommended for purchase and re-sale:"
        )
        try:
            if not id_input:
                st.dataframe(self.recommended_houses)
            else:
                if int(id_input) in self.recommended_houses["ID"].values:
                    st.dataframe(
                        self.recommended_houses.loc[
                            self.recommended_houses["ID"] == int(id_input)
                        ]
                    )
                else:
                    st.warning(
                        "The house with this ID is not recommended for purchase or there is no house with this ID."
                    )
        except:
            st.error("Input value is not a valid ID.")

        return None

    def page_maps(self, filter_map):
        if filter_map == "Recommended houses to buy":
            st.title("Map of all recommended houses for purchase:")
            st.header("")
            map_args = (self.recommended_houses, True)
        else:
            st.title("Map of all available houses:")
            st.header("")
            map_args = (self.recommended_houses, False)

        # Density map of the houses
        houses_map = get_houses_map(*map_args)
        folium_static(houses_map, width=1200, height=700)

        # Map with the avarage price per region (ZipCode)
        st.title("Avarage Price per Region (ZipCode)")
        avg_region = get_price_per_region_map(*map_args)
        folium_static(avg_region, width=1200, height=700)


if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.side_bar()
