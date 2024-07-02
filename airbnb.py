import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from streamlit_option_menu import option_menu

#reading the csv file
df1=pd.read_csv("C:/Users/surya/OneDrive/Desktop/suryavs/airbnb.csv")
def sun(a):
    if(a=="All"):
        df=df1
    else:
        country=a
        df=df1[df1["Country"]==country]
    fig_2 = px.sunburst(df, 
                    path=['Country','Street','Property_type','Room_type','Name'], 
                    values='Review_scores',
                    color_discrete_sequence=px.colors.qualitative.Prism,  # Example color palette
                    maxdepth=3,  # Limit the depth of the sunburst to make it clearer
                    # labels={amount},  # Update labels for clarity
                    title="Sunburst Chart for Transactions",  # Add a title
                    height=850,  # Set the height of the chart
                    width=850,  # Set the width of the chart
                    )
    fig_2.update_traces(textfont=dict(size=12), insidetextorientation='radial')  # Adjust font size and text orientation
    fig_2.update_layout(margin=dict(t=0, l=0, r=0, b=0),  # Remove unnecessary margins
                        plot_bgcolor='rgba(0,0,0,0)')  # Set transparent background
    return fig_2
def map():
    fig = px.choropleth(
                df1,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='Country',
                color="Street",
                #title=f"year {i} Quarter {j}",
                color_continuous_scale='Blue',
                #range_color=(0,b[count].max()),  # Define the range of colors
                height=700,
                width=700
            )
    fig.update_geos(fitbounds="locations", visible=False)
    fig = px.choropleth(df1, locations='Country', locationmode='country names',
                    color_discrete_sequence=['#636EFA'],  # Color for the highlighted countries
                    title='Highlighted Countries Map')
# Update layout for better visualization
    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        title_x=0.5
    )
    return fig
import plotly.express as px
def glo():
    fig = px.scatter_mapbox(df1, 
                            lat="Latitude", 
                            lon="Longitude", 
                            color="availability_365",
                            size="availability_365",  # Adjust marker size based on availability
                            hover_name="Country",
                            hover_data={"suburb": True, "market": True, "Country": True, "availability_365": True},
                            color_continuous_scale=px.colors.sequential.Viridis,
                            zoom=1,
                            width=1300,
                            height=700)
    
    fig.update_layout(mapbox_style="open-street-map", 
                    title="Listing Availability by Location",
                    title_font=dict(size=24, family='Arial', color='red'),  # Enhance title
                    margin={"r":0,"t":50,"l":0,"b":0},  # Adjust margins for better layout
                    coloraxis_colorbar=dict(
                        title="Availability (days)",
                        ticks="outside",
                        tickvals=[0, 100, 200, 300, 365],
                        ticktext=["0", "100", "200", "300", "365"],
                        lenmode="fraction", len=0.5,
                    )) 
    
    fig.update_traces(marker=dict(opacity=0.7, sizemode='area', sizemin=4))  # Make markers semi-transparent and minimum size
    
    return fig
def bar_chart():
    df=df1.groupby("Country")["availability_365"].mean()
    d=pd.DataFrame(df)
    d.reset_index(inplace=True)
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=d['Country'], 
        y=d['availability_365'], 
        marker_color='indianred',  # Set bar color
        text=d['Country'],  # Display value on bars
        textposition='auto'
    ))

    fig.update_layout(
        title="Bar Chart Example",
        title_font=dict(size=24, family='Arial', color='green'),
        xaxis_title="Country",
        yaxis_title="Average Availability in a year",
        margin=dict(l=20, r=20, t=50, b=50),  # Adjust margins
        xaxis=dict(tickangle=-45),  # Rotate x-axis labels if necessary
    )
    return fig
def pie_line(a):
    if(a=="All"):
        d=df1
    else:
        country=a
        d=df1[df1["Country"]==country]
    f=[]
    df=d.groupby("Property_type")['Review_scores'].count()
    k=pd.DataFrame(df)
    k.reset_index(inplace=True)
    k.columns = ["Property_type","count"]
    fig = px.pie(k,values="count",names="Property_type", title=f'User Count Distribution by Region')
    # Update traces to show labels
    fig.update_traces(textinfo='label+percent')

    # Optionally, you can customize the position of the labels
    fig.update_traces(textposition='inside')
    f.append(fig)
    r=[True,False]
    for i in r:
        z=k.sort_values(by="count",ascending=i)
        b=z.head()
        fig_1 = go.Figure()

        fig_1.add_trace(go.Bar(
            x=b['Property_type'], 
            y=b['count'], 
            marker_color='orange',  # Set bar color
            text=b['Property_type'],  # Display value on bars
            textposition='auto'
        ))

        fig_1.update_layout(
            title="Bar Chart Example",
            title_font=dict(size=24, family='Arial', color='darkblue'),
            xaxis_title="Category",
            yaxis_title="Value",
            margin=dict(l=20, r=20, t=50, b=50),  # Adjust margins
            xaxis=dict(tickangle=-45),  # Rotate x-axis labels if necessary
        )
        f.append(fig_1)
    return f
def box(a):
    if(a=="All"):
        d=df1
    else:
        country=a
        d=df1[df1["Country"]==country]
    fig = px.box(d, x="Room_type", y="availability_365", title="Box plot of Room types by Availability")
    fig2 = px.box(d, x="Room_type", y="Review_scores", title="Box plot of Room types by Review Score")
    f=[fig,fig2]
    return f
def sc(a):
    if(a=="All"):
        d=df1
    else:
        country=a
        d=df1[df1["Country"]==country]
    fig = px.scatter(d, x="Bed_type", y="Review_scores", title="Scatter plot of Bed type vs Review score")
    return fig
def card(a):
    if(a=="All"):
        d=df1
    else:
        country=a
        d=df1[df1["Country"]==country]
    list=["Min_nights","Max_nights","Cleaning_fee","Review_scores_accuracy","Review_scores_cleanliness","Review_scores_checkin","Review_scores_communication","Review_scores_location","Review_scores_value","Review_scores_rating"]
    color=["sandybrown","seagreen","blue","sienna","red","skyblue","slateblue","slategray","slategrey","orange"]
    f=[]
    for i,j in zip(list,color):
        # Create a blank figure
        fig = px.scatter()
        a=i
        b=d[i].mean()
        # Update layout to add a card-like annotation
        fig.update_layout(
            annotations=[
                dict(
                    text=f"{a}<br><b>{b}",
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=20),
                    align="center",
                    bordercolor="black",
                    borderwidth=2,
                    borderpad=10,
                    bgcolor=j,
                    opacity=0.8
                )
            ],
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            width=300,
            height=200,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        f.append(fig)
    return f
def heat(a):
    if(a=="All"):
        d=df1
    else:
        country=a
        d=df1[df1["Country"]==country]
    x=d[["Review_scores","Review_scores_communication","Review_scores_checkin","Review_scores_location","Review_scores_value","Review_scores_rating"]]
    # Compute the correlation matrix
    corr_matrix = x.corr()

    # Create a heatmap using Plotly
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='tempo',
        zmin=0, zmax=1
    ))
    # tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid','turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr','ylorrd'
    # Add annotations
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix.columns)):
            fig.add_annotation(
                x=corr_matrix.columns[j],
                y=corr_matrix.columns[i],
                text=str(round(corr_matrix.iloc[i, j], 2)),
                showarrow=False,
                font=dict(color="black" if abs(corr_matrix.iloc[i, j]) < 0.5 else "white")
            )

    # Update layout for better appearance
    fig.update_layout(
        title='Correlation Matrix Heatmap',
        xaxis_nticks=25,
        yaxis_nticks=25,
        width=1200,  # Increase width
        height=600 
    )

    return fig
def fun(z):
        st.plotly_chart(sun(z))
        col1, col2 = st.columns(2)
        a=pie_line(z)
        with col2:
            t1,t2=st.tabs(["top 5","bottom 5"])
            # Chart 1: Bar chart
            with t2:
                    st.plotly_chart(a[1])

            # Chart 2: Pie chart
            with t1:
                    st.plotly_chart(a[2])
        with col1:
            st.plotly_chart(a[0])
        st.plotly_chart(heat(z))
        c=card(z)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.plotly_chart(c[0])
        with col2:
            st.plotly_chart(c[1])
        with col3:
            st.plotly_chart(c[2])
        with col4:
            st.plotly_chart(c[3])
        b=box(z)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(b[0])
        with col2:
            st.plotly_chart(b[1])
        st.plotly_chart(sc(z))
        col1,col2,col3,col4= st.columns(4)
        with col1:
            st.plotly_chart(c[4])
        with col2:
            st.plotly_chart(c[5])
        with col3:
            st.plotly_chart(c[6])
        with col4:
            st.plotly_chart(c[7])
        col5,col6= st.columns(2)
        with col5:
            st.plotly_chart(c[8])
        with col6:
            st.plotly_chart(c[9])
        return(0)






























#streamli page
st.set_page_config(layout="wide")

with st.sidebar:
    select_option=option_menu("Menu",["About","Map","Insights"])
if select_option=="About":

# Set the page configuration
    # st.set_page_config(page_title="Explore Airbnb", layout="wide")

    # CSS for background image
    page_bg_img = '''
    <style>
    body {
        background-image: url("https://www.freepik.com/premium-photo/view-wall-through-window_101459348.htm#fromView=search&page=1&position=39&uuid=0450eb17-50ab-4207-8fb1-d517c62cde2c");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .main-content {
        background-color: rgba(255, 255, 255, 0.8); /* White background with some transparency */
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    '''

    # Inject CSS with HTML
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Title and Introduction
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.title("Explore Airbnb")
    st.write("""
    Airbnb revolutionizes the way we travel by offering a diverse array of unique and personalized accommodations around the globe. 
    From enchanting treehouses and luxurious villas to eco-friendly tiny homes and rustic cabins, Airbnb provides a home away from home 
    for every type of traveler.
    """)

    # Unique Stays Section
    st.header("Unique Stays")
    st.write("""
    - Enchanting treehouses
    - Whimsical yurts
    - Eco-friendly tiny homes
    - Floating houseboats
    - Glamping tents
    - Off-grid retreats
    - Artistic lofts
    """)

    # Unique Experiences Section
    st.header("Unique Experiences")
    st.write("""
    - Immersive local culture
    - Unforgettable adventures
    - Hidden gems
    - Secret spots
    - Local insider tips
    - One-of-a-kind activities
    - Personalized itineraries
    """)

    # Unique Features Section
    st.header("Unique Features")
    st.write("""
    - Spectacular views
    - Historical landmarks
    - Architectural marvels
    - Themed interiors
    - Artisanal touches
    - Quirky decor
    - Bespoke amenities
    """)

    # Benefits for Guests Section
    st.header("Benefits for Guests")
    st.write("""
    - Home away from home
    - Authentic experiences
    - Convenient locations
    - Customized stays
    - Cost-effective
    - 24/7 support
    """)

    # Benefits for Hosts Section
    st.header("Benefits for Hosts")
    st.write("""
    - Extra income
    - Flexible hosting
    - Global community
    - Hosting resources
    - Secure payments
    - Insurance coverage
    """)

    # Footer
    st.write("""
    Whether seeking adventure, comfort, or a touch of whimsy, Airbnb opens the door to a world of possibilities.
    """)
    st.markdown('</div>', unsafe_allow_html=True)


elif select_option=="Map":
    st.plotly_chart(glo())
elif select_option=="Insights":
    st.plotly_chart(bar_chart())
    country=st.selectbox("Country:",['All countries','United States', 'Turkey', 'Hong Kong', 'Australia', 'Portugal','Brazil', 'Canada', 'Spain', 'China'])
    if country=="All countries":
        fun("All")
    elif country=="United States":
        fun("United States")
    elif country=="Turkey":
        fun("Turkey")        
    elif country=="Hong Kong":
        fun("Hong Kong")        
        
    elif country=="Australia":
        fun("Australia")
    elif country=="Portugal":
        fun("Portugal")
        
    elif country=="Brazil":
        fun("Brazil")
        
    elif country=="Canada":
        fun("Canada")
        
    elif country=="Spain":
        fun("Spain")
        
    elif country=="China":
        fun("China")
        