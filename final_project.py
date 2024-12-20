"""
Lilly Steffen
CS-230-05
Boston Airbnb Dataset
URL: [ https://boston-airbnb-data-analysis-fh38jj7bepnpswchwrfhrn.streamlit.app ]
Description:
This program creates an interactive site for exploring Boston Airbnb data concerning
price analysis, neighbourhood mapping, and property type comparisons.
The program allows users to filter by price range, neighbourhood, and property
type while providing visualizations such as maps and charts.

* There will be an accompanying AI use document. At the end of that document it will
contain a list of websites and YouTube videos I used as support to create this assignment

"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk

# create a dataframe for the listings csv file and remove the empty column of neighbourhood_group
dflistings = pd.read_csv("listings.csv")
dflistings = dflistings.drop('neighbourhood_group', axis=1)


st.title("Boston Airbnb Data Analysis")
st.text("An interactive site for exploring Boston Airbnb data concerning price analysis, neighbourhood mapping, "
        "and property type comparisons. This site allows users to filter by price range, neighbourhood, "
        "and property type while providing visualizations such as maps and charts.")

# I found this trick in a YouTube Video on tricks you can do with streamlit. "st.tabs" is what creates the tabs at the
# top of the website so the user can navigate between subjects rather than scrolling down a long page
tab1, tab2, tab3 = st.tabs(["Price Analysis", "Neighbourhood Explorer", "Property Analysis"])




with tab1: # then under that first tab, Price Analysis, we can put this portion of information

    st.title("Price Analysis")

    st.subheader(":red[Property Listings Available Based on their Price]", divider="gray")
    #Since the majority of the listings are under 600 dollars I added a checkbox where users could choose if they
            # wanted to include the higher values. I found this way of using a checkbox from a streamlit help video.
    st.text("Due to the fact that majority of the listings in the Boston area are under 600 dollars, "
            "The default ranges are capped at 600 dollars.")
    st.text("Would you like to see listings above a value of 600 dollars? "
            "If checked the ranges will be updated to values that reflect all listing amounts.")
    yes = st.checkbox("Yes")
    if yes:

        # AI Assisted *Documented as AI Use 1       LEARN WHAT LINE 48/51 DOES

        # labels for the ranges onf prices and their respective buckets that they would be categorized into
        labels = ['0-100', '100-200', '200-300', '300-400','400-500', '500-600', '600-1000', '1000-2000', '2000-3000', '3000-4000', '4000-5000']
        bins = [0, 100, 200, 300, 400, 500, 600, 1000, 2000, 3000, 4000, 5000]

        # user chooses their price range
        selected_range = st.selectbox("What price range would you like to see? (In USD Currency):" , labels)

        #creates a new column in the data frame to sort listings by their price brackets and assign the listing to a bracket
        dflistings['Price Bracket'] = pd.cut(dflistings['price'], bins=bins, labels=labels, right=False)

        # stores the filtered data so when the user selects a range the df will print out only the data in that range
        range = dflistings[dflistings['Price Bracket'] == selected_range]
        # cut out all unnecessary columns
        dflistings_shortened = range.drop(columns=['id', 'host_id', 'latitude', 'longitude', 'minimum_nights',
                                                        'number_of_reviews', 'last_review', 'reviews_per_month',
                                                        'calculated_host_listings_count', 'availability_365',
                                                        'number_of_reviews_ltm', 'license'])

                # check that there are values in that price range
                # if range:
                #     st.write("These are the listings available in your selected price range:")
                #     st.dataframe(range)
                # else:
                #     st.write("There are no listings available in the selected price range.")


        # Originally tried the other way around but streamlit was unable to process it
        if dflistings_shortened.empty:   #The error of the earlier way to present the data was because you cant directly state that there is a value in the data frame. so this checks if the data frame is empty rather than containing something.
            st.write("There are no listings available in the selected price range.")
        else:
            st.write("These are the listings available in your selected price range:")
            st.dataframe(dflistings_shortened)


    else:
        # Same as above but with different bins to choose from for the under $500 listings
        labels = ['0-50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350', '350-400', '400-450', '450-500', '500-550', '550-600']
        bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]

        selected_range = st.selectbox("What price range would you like to see? (In USD Currency):" , labels)

        dflistings['Price Bracket'] = pd.cut(dflistings['price'], bins=bins, labels=labels, right=False)
        # sort listings by their price and then by their price bracket
        sorted_df_by_price = dflistings.sort_values(by="price", ascending=True)
        range = dflistings[dflistings['Price Bracket'] == selected_range]
        dflistings_shortened = range.drop(columns=['id', 'host_id', 'latitude', 'longitude', 'minimum_nights',
                                                        'number_of_reviews', 'last_review', 'reviews_per_month',
                                                        'calculated_host_listings_count', 'availability_365',
                                                        'number_of_reviews_ltm', 'license'])


        if dflistings_shortened.empty:   #The error of the earlier way to present the data was because you cant directly state that there is a value in the data frame. so this checks if the data frame is empty rather than containing something.
            st.write("There are no listings available in the selected price range.")
        else:
            st.write("These are the listings available in your selected price range:")
            st.dataframe(dflistings_shortened)



    st.subheader(":red[Top 5 Most and Least Expensive Listings]", divider = 'grey')
    dflistings_revised = dflistings.drop(columns=['id', 'host_id', 'latitude', 'longitude', 'minimum_nights',
                                                        'number_of_reviews', 'last_review', 'reviews_per_month',
                                                        'calculated_host_listings_count', 'availability_365',
                                                        'number_of_reviews_ltm', 'license', 'Price Bracket'])

    # printing the top 5 most expensive listings
    st.text("The 5 Most Expensive Listings:")
    top_5 = dflistings_revised.nlargest(5, 'price')
    st.write(top_5)
    # printing the lowest 5 listings
    st.text("The 5 Cheapest Listings:")
    bottom_5 = dflistings_revised.nsmallest(5, 'price')
    st.write(bottom_5)




    st.subheader(":red[Average Price of Listings by their Neighbourhood]", divider = 'grey')
    # markdown allows for more customization in the text than just using text. "_" makes the text italicised and "**" bolds text.
    st.markdown("_Keep in mind **several** listings do not have a price available_")
    # Create the chart
    avg_price_neighbourhood = dflistings.groupby('neighbourhood')['price'].mean()
    # print the chart
    st.bar_chart(avg_price_neighbourhood, color = '#a0db8e')





    st.subheader(":red[Analysis of the Effect of the Price of the Listing and the Amount of Reviews Given per Month]", divider = 'grey')
    st.markdown("There **does not** appear to be a clear **relationship** between the price of a listing and the number of reviews it receives.")

    # creating the chart
    fig, ax = plt.subplots()
    ax.scatter(x=dflistings['reviews_per_month'], y=dflistings['price'], s = 2, c = '#915F6D', marker = '^')   # s=1 controls the size of the dots

    # Setting axis limits so we can zoom into the scatterplot and not have to include the outliers
    ax.set_xlim(0, 10)                  # The x-axis range is now from 0 to 15
    ax.set_ylim(0, 1000)                # The y-axis range is now from 0 to 1500

    # Chart information
    ax.set_xlabel('Reviews per Month')
    ax.set_ylabel('Price ($)')
    ax.set_title('Price vs Reviews')

    # show the plot in streamlit site
    st.pyplot(fig)




with tab2:
    st.title("Neighbourhood Explorer")
    st.subheader(":red[Map of all Listings Available in Boston, MA on Airbnb]", divider = 'grey')

    # Bulleted list explaining the colored dots on the map
    st.markdown(
        """
        **Listings on the map are color categorized in the following way:**
        - Green dots indicate listings with a price price less than 150 dollars
        - Yellow dots indicate listings with a price between 150 and 500 dollars
        - Red dots indicate listings with a price above 500 dollars
        - Grey dots indicate listings without an available price
        """
    )

    st.text("What neighbourhood would you like to view?")
            # sliders for users to change the zoom and pinpoint levels on the map. Value is the initial point it will be set to
            # the min and max values do just as they say creating a minimum and maximum for the slider and the step is how
            # much the slider moves when shifting up or down
    zoom_value = st.slider("How zoomed in would you like the map to be?", value = 12.5, min_value=10.0, max_value=15.0, step = 0.5)
    dot_size = st.slider("Would you like to change the size of the pinpoints on the map?", value = 40.0, min_value=15.0, max_value=65.0, step = 5.0)


    # AI Assisted  *Documented as AI Use 2
    # This function creates price brackets for the listings and assigns them their own colors
    def price_bracket(price):
        if price < 150:
            return 'Low', [0, 255, 0]                       # Green dots for low prices
        elif price < 500:
            return 'Medium', [255, 255, 0]                  # Yellow dots for medium price
        elif price >500:
            return 'High', [255, 0, 0]                      # Red dots for high price
        else:
            return 'Price N/A', [169, 169, 169]             # Grey dots for listings w/o a price

    #assigns the price bracket and coordinating color to the listing
    dflistings[['price_bracket', 'color']] = dflistings['price'].apply(lambda x: pd.Series(price_bracket(x)))


    # Select box to choose the neighbourhood
    neighbourhood_dropdown = st.selectbox(
        'Select Neighbourhood:', dflistings['neighbourhood'].unique()
    )

    # Filter DataFrame based on selected neighborhood
    neighbourhood_df = dflistings[dflistings['neighbourhood'] == neighbourhood_dropdown]

    # Create the PyDeck scatterplot layer
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        neighbourhood_df,
        get_position=["longitude", "latitude"],
        get_radius=dot_size,                                  # Adjust the sizes of the circles on the map
        get_color="color",                              # assign the colors based on the listing's price bracket
        pickable=True,                                  # Enable hover functionality to see key details
        auto_highlight=True,                            # highlight the dots when hovered on
        opacity=1                                       # how opaque are the dots
    )

    # Tooltip for displaying listing details when hovered.
    tooltip = {
                #This will show the name of the listing, the room type and the price
        "html": "<b>Listing:</b> {name}<br><b>Room Type:</b> {room_type}<br><b>Price:</b> ${price}",
                # this creates the box that the key details will be inside. the font color will be black and size 14
                # with a white background and a 1 point solid gray border. The padding is what creates distance between
                # the words in the box and the border.
        "style": {"color": "black", "fontSize": "14px", "backgroundColor": "white", "border": "1px solid gray",
                  "padding": "10px"}
    }

    # Set up the view of the map based on filtered data
    view_state = pdk.ViewState(
        latitude=neighbourhood_df['latitude'].mean(),    # Centers the map based on the average latitude of the listings for the selected neighbourhood
        longitude=neighbourhood_df['longitude'].mean(),  # Centers the map based on average longitude of the listings for the selected neighbourhood
        zoom=zoom_value,                                 # affects how zoomed in we are to the map
        pitch = 0                                        # affects the tilt of the map
    )

    # Creating the map
    map = pdk.Deck(
        layers=[scatter_layer],                         # all the dot points that will be printed on the map
        initial_view_state=view_state,                  # where is the map is initially centered based on the mean lat and lon of each neighbourhood
        tooltip=tooltip,                                # the map will have hover functionality
        map_style= "mapbox://styles/mapbox/light-v9"    # the map will be in the light style
        #'mapbox://styles/mapbox/outdoors-v11' - outdoors map style
        #'mapbox://styles/mapbox/satellite-v9' - satellite map style
    )

    # print the map in Streamlit
    st.pydeck_chart(map)



with tab3:
    st.title("Property Analysis")
    st.subheader(":red[Property listings by their Housing Type]", divider="grey")

    # Table for the selected listings type (Private Room Entire home/apt, etc.)
    selected_housing = st.selectbox("Select a Housing Type", options = ["Private room", "Entire home/apt",
                                                                              "Shared room", "Hotel room"])
    housing = dflistings[dflistings["room_type"] == selected_housing]
    st.write(f"{selected_housing} listings available in the Boston, MA area:")
    dflistings_cutdown = housing.drop(columns=['id', 'host_id', 'latitude', 'longitude', 'minimum_nights',
                                                  'number_of_reviews', 'last_review', 'reviews_per_month',
                                                  'calculated_host_listings_count', 'availability_365',
                                                  'number_of_reviews_ltm', 'license', 'Price Bracket',
                                                  'price_bracket', 'color'])
    st.dataframe(dflistings_cutdown)

    # Pie Chart to compare listing by their room type
    st.subheader(":red[Property Listings Pie Chart]", divider="grey")
    st.text("The majority of Airbnb listings in Boston, MA are Entire homes/appartments and Private rooms.")

    explode = [0.025,0.025,0.35,0.35]                          # splits the slices out this many points
    colors = ['#D8BFD8','#89CFF0', '#953553', '#51414F' ]      # assigns a color to each slice
    room_types = dflistings['room_type'].value_counts()        # counts each room type in the listings to figure out the slice size

    #Making the pie chart
    fig, ax = plt.subplots()
                # the pie chart is for room  types, it will show the percentage of the pie and that label will be 1.15 points away from the center
                # the colors and explode values are assigned as well. The start angle shifts the chart by 180 degrees.
    ax.pie(room_types, autopct="%.1f%%", explode=explode, colors=colors, pctdistance=1.15, startangle=180)

    # pie chart legend
        # the legend will be based on the room types variable. It will have a tittle and will be placed in the upper
        # right of the image by using bbox_to_anchor to place the legend outside the chart to the upper right 
    ax.legend(room_types.index, title="Room Types:", bbox_to_anchor=(1.25,1.15))

    # Display the plot in Streamlit
    st.pyplot(fig)






