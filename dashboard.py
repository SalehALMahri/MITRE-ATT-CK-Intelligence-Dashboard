import dash
from dash import dcc, html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input
import random

# Load the scored dataset from your local system
file_path = r'C:/Users/saleh/Downloads/saleh/Swinburne University/3rd Semester/Technology Innovation Project/TIP Project/FV2.csv'
scored_data = pd.read_csv(file_path)

# Load the FV4 dataset specifically for the bar chart
fv4_file_path = r'C:/Users/saleh/Downloads/saleh/Swinburne University/3rd Semester/Technology Innovation Project/TIP Project/FV2.csv'
fv4_data = pd.read_csv(fv4_file_path)

# Clean the dataset
scored_data = scored_data[scored_data['tactics'].notnull()]
scored_data_expanded = scored_data[scored_data['defenses bypassed'].notnull()].copy()
scored_data_expanded['defenses bypassed'] = scored_data_expanded['defenses bypassed'].str.split(',')
scored_data_expanded = scored_data_expanded.explode('defenses bypassed')
grouped_data = scored_data_expanded.groupby(['defenses bypassed', 'tactics']).size().reset_index(name='technique_count')
grouped_data_filtered = grouped_data[(grouped_data['technique_count'] > 0)]

# Convert 'created_x' to datetime and group data
scored_data['created_x'] = pd.to_datetime(scored_data['created_x'], errors='coerce', format='%d-%b-%y')
scored_data['Year'] = scored_data['created_x'].dt.year
scored_data['Prevalence Score'] = pd.to_numeric(scored_data['Prevalence Score'], errors='coerce')

# Clip Prevalence Score to remove extreme values and rescale to 0-500
scored_data['Prevalence Score'] = scored_data['Prevalence Score'].clip(upper=1000)
scored_data['Prevalence Score'] = (scored_data['Prevalence Score'] - scored_data['Prevalence Score'].min()) / (scored_data['Prevalence Score'].max() - scored_data['Prevalence Score'].min()) * 500

# Group by region and year, calculate cumulative score
region_year_cumulative = scored_data.groupby(['Region', 'Year'], as_index=False)['Prevalence Score'].sum()
region_year_cumulative['Cumulative Score'] = region_year_cumulative.groupby('Region')['Prevalence Score'].cumsum()

# Group data for the stacked bar chart
scored_data_filtered = scored_data[scored_data['source name'].notnull() & scored_data['tactics'].notnull()]
threat_actor_techniques_grouped = scored_data_filtered.groupby(['source name', 'tactics']).size().reset_index(name='technique_count')

country_coordinates = {
    'Russia': {'lat': 61.5240, 'lon': 105.3188},
    'North Korea': {'lat': 40.3399, 'lon': 127.5101},
    'Japan': {'lat': 36.2048, 'lon': 138.2529},
    'China': {'lat': 35.8617, 'lon': 104.1954},
    'Iran': {'lat': 32.4279, 'lon': 53.6880},
    'Germany': {'lat': 51.1657, 'lon': 10.4515},
    'UAE': {'lat': 23.4241, 'lon': 53.8478}
}

file_path = r'C:/Users/saleh/Downloads/saleh/Swinburne University/3rd Semester/Technology Innovation Project/TIP Project/FV2.csv'  # Update this path
df = pd.read_csv(file_path)
df_filtered = df[df['Region'] != 'Unknown']

def randomize_coordinates(lat, lon, country):
    """Randomize lat/lon with different deviation for specific countries."""
    if country in ['North Korea', 'Japan']:
        max_deviation = 5  # Smaller deviation for these countries
    elif country in ['Russia']:
        max_deviation = 15  
    elif country in ['China']:
        max_deviation = 12
    elif country in ['UAE']:
        max_deviation = 6
    else:
        max_deviation = 9  # Larger deviation for all other countries
        
    lat_variation = random.uniform(-max_deviation, max_deviation)
    lon_variation = random.uniform(-max_deviation, max_deviation)
    return lat + lat_variation, lon + lon_variation


# Map latitudes and longitudes using the country_coordinates with more variation
latitudes = []
longitudes = []

for index, row in df_filtered.iterrows():
    country = row['Region']
    if country in country_coordinates:
        base_lat = country_coordinates[country]['lat']
        base_lon = country_coordinates[country]['lon']
        # Apply larger randomization to get more separation between cities
        new_lat, new_lon = randomize_coordinates(base_lat, base_lon, country)
        latitudes.append(new_lat)
        longitudes.append(new_lon)
    else:
        latitudes.append(None)
        longitudes.append(None)

# Add the new latitudes and longitudes to the dataframe
df_filtered['Latitude'] = latitudes
df_filtered['Longitude'] = longitudes

# Remove entries where lat/lon are still None (countries without coordinates)
df_filtered = df_filtered.dropna(subset=['Latitude', 'Longitude'])

# Assign a unique color to each tactic
unique_tactics = df_filtered['tactics'].unique()
color_map = {tactic: f'rgb({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)})' for tactic in unique_tactics}
df_filtered['color'] = df_filtered['tactics'].map(color_map)
def randomize_coordinates(lat, lon, country):
    """Randomize lat/lon with different deviation for specific countries."""
    if country in ['North Korea', 'Japan']:
        max_deviation = 5  # Smaller deviation for these countries
    elif country in ['Russia']:
        max_deviation = 15  
    elif country in ['China']:
        max_deviation = 12
    elif country in ['UAE']:
        max_deviation = 6
    else:
        max_deviation = 9  # Larger deviation for all other countries
        
    lat_variation = random.uniform(-max_deviation, max_deviation)
    lon_variation = random.uniform(-max_deviation, max_deviation)
    return lat + lat_variation, lon + lon_variation


# Map latitudes and longitudes using the country_coordinates with more variation
latitudes = []
longitudes = []

for index, row in df_filtered.iterrows():
    country = row['Region']
    if country in country_coordinates:
        base_lat = country_coordinates[country]['lat']
        base_lon = country_coordinates[country]['lon']
        # Apply larger randomization to get more separation between cities
        new_lat, new_lon = randomize_coordinates(base_lat, base_lon, country)
        latitudes.append(new_lat)
        longitudes.append(new_lon)
    else:
        latitudes.append(None)
        longitudes.append(None)

# Add the new latitudes and longitudes to the dataframe
df_filtered['Latitude'] = latitudes
df_filtered['Longitude'] = longitudes

# Remove entries where lat/lon are still None (countries without coordinates)
df_filtered = df_filtered.dropna(subset=['Latitude', 'Longitude'])

# Assign a unique color to each tactic
unique_tactics = df_filtered['tactics'].unique()
color_map = {tactic: f'rgb({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)})' for tactic in unique_tactics}
df_filtered['color'] = df_filtered['tactics'].map(color_map)

# Create the 3D globe plot with unique colors for each tactic
fig = go.Figure(go.Scattergeo(
    lon=df_filtered['Longitude'],
    lat=df_filtered['Latitude'],
    text=df_filtered['Region'] + ': ' + df_filtered['tactics'],
    mode='markers',
    marker=dict(
        size=8,
        color=df_filtered['color'],
        symbol='circle',
        line=dict(width=1, color='rgb(40,40,40)')
    )
))

# Globe settings to make it more prominent
fig.update_layout(
    #title='Tactics Used by Country (Increased Distance Between Tactics)',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='orthographic',
        projection_rotation=dict(lon=105, lat=61),  # Coordinates of Russia
        bgcolor='white',  # Set background to black to make the globe more prominent
        visible=True,
        showland=True,
        landcolor='forestgreen',
        showcountries=True,
        countrycolor='gray',
    )
)



# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard with a professional format
app.layout = html.Div([

    # Dashboard Title
    html.Div([
    html.H1("MITRE ATT&CK Intelligence Dashboard", style={
        'text-align': 'center',
        'font-family': 'Arial, sans-serif',
        'color': 'black',
        'font-size': '36px',
        'margin-bottom': '20px',
        'text-shadow': '2px 2px 4px rgba(0, 0, 0, 0.4)',  # Add a shadow to give a 3D effect
        'font-weight': 'bold'  # Optional: makes the font stand out more
    }),
    html.P("Visualizing techniques, defenses, and prevalence across regions and time.",
           style={'text-align': 'center', 'color': 'black', 'font-size': '16px'}),
], style={'padding': '20px', 'background-color': 'lightgrey', 'box-shadow': '0px 4px 6px rgba(0, 0, 0, 0.1)', 'border': '2px solid black'}),

    # Bar chart with filters
    html.Div([
        html.H3("Bar Chart: Top 10 Threat Actors by Threat Actor Score", style={
            'text-align': 'center',
            'color': 'grey',
            'font-size': '24px',
            'margin-bottom': '10px',
            'border': '2px solid black'
        }),
        html.Div([
            # Filter for Technique Dropdown
            html.Div([
                html.H4("Select a Threat Actor", style={'font-family': 'Arial'}),
                dcc.Dropdown(
                id='actor-dropdown',  # Updated the ID to reflect the change
                options=[{'label': 'Top 10 Threat Actors', 'value': 'Top 10'}] +
                        [{'label': actor, 'value': actor} for actor in scored_data['source name'].unique()],
                value='Top 10',
                clearable=False,
                style={'border': '1px solid #00008B', 'border-radius': '5px'}
            ),

            ], style={'width': '30%', 'padding': '10px'}),
            
            # Bar chart for Techniques
            html.Div([dcc.Graph(id='dynamic-bar-chart')],
                     style={'width': '65%', 'padding': '20px', 'background-color': '#FBFCFC', 'border-radius': '5px'})
        ], style={'display': 'flex', 'justify-content': 'center'}),
    ]),

    # Pie chart with filters for Tactics and Regions
    html.Div([
        html.H3("Pie Chart: Distribution of Tactics by Region", style={
            'text-align': 'center',
            'color': 'grey',
            'font-size': '24px',
            'margin-bottom': '10px',
            'border': '2px solid black'
        }),
        html.Div([
            # Filter for Tactic Dropdown
            html.Div([
                html.H4("Select a Tactic", style={'font-family': 'Arial'}),
                dcc.Dropdown(
                    id='tactic-dropdown',
                    options=[{'label': tactic, 'value': tactic} for tactic in scored_data['tactics'].unique()],
                    value=scored_data['tactics'].unique()[0],
                    clearable=False,
                    style={'border': '1px solid #000080', 'border-radius': '5px'}
                ),
            ], style={'width': '30%', 'padding': '10px'}),
            
            # Filter for Region Dropdown
            html.Div([
                html.H4("Select Region(s)", style={'font-family': 'Arial'}),
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[{'label': region, 'value': region} for region in scored_data['Region'].unique()],
                    value=list(scored_data['Region'].unique()),
                    multi=True,
                    clearable=False,
                    style={'border': '1px solid grey', 'border-radius': '5px'}
                ),
            ], style={'width': '30%', 'padding': '10px'}),

            # Pie Chart
            html.Div([dcc.Graph(id='dynamic-pie-chart')],
                     style={'width': '65%', 'padding': '20px', 'background-color': '#FBFCFC', 'border-radius': '5px'})
        ], style={'display': 'flex', 'justify-content': 'center'}),
    ]),

    # Scatter plot for Complexity vs Prevalence
    html.Div([
        html.H3("Scatter Plot Chart: Complexity vs Prevalence of Techniques", style={
            'text-align': 'center',
            'color': 'grey',
            'font-size': '24px',
            'margin-bottom': '10px',
            'border': '2px solid black'
        }),
        html.Div([
            dcc.Graph(
                    figure=px.scatter(scored_data, x='Complexity Score', y='Prevalence Score', hover_data=['name'],
                      color='name',  # This line assigns different colors to each technique
                      labels={"Complexity Score": "Complexity", "Prevalence Score": "Prevalence"}))

        ], style={'padding': '20px', 'background-color': '#FBFCFC', 'border-radius': '5px'})
    ]),

    # Heatmap with filters
    html.Div([
        html.H3("Heat Map: Defenses Bypassed vs Tactics Heatmap", style={
            'text-align': 'center',
            'color': 'grey',
            'font-size': '24px',
            'margin-bottom': '10px',
            'border': '2px solid black'
        }),
        html.Div([
            # Filter for Heatmap Region
            html.Div([
                html.H4("Select a Region", style={'font-family': 'Arial'}),
                dcc.Dropdown(
                    id='region-heatmap-dropdown',
                    options=[{'label': region, 'value': region} for region in scored_data['Region'].unique()],
                    value=scored_data['Region'].unique()[0],
                    clearable=False,
                    style={'border': '1px solid grey', 'border-radius': '5px'}
                ),
            ], style={'width': '30%', 'padding': '10px'}),
            
            # Heatmap
            html.Div([dcc.Graph(id='dynamic-heatmap')],
                     style={'width': '65%', 'padding': '20px', 'background-color': '#FBFCFC', 'border-radius': '5px'})
        ], style={'display': 'flex', 'justify-content': 'center'}),
    ]),

    # Line chart with filters for regions
    html.Div([
        html.H3("Line Graph: Cumulative Prevalence Score Over Time", style={
            'text-align': 'center',
            'color': 'grey',
            'font-size': '24px',
            'margin-bottom': '10px',
            'border': '2px solid black'
        }),
        html.Div([
            # Filter for Region Dropdown
            html.Div([
                html.H4("Select Region(s)", style={'font-family': 'Arial'}),
                dcc.Dropdown(
                    id='region-dropdown_LC',
                    options=[{'label': region, 'value': region} for region in region_year_cumulative['Region'].unique()],
                    value=list(region_year_cumulative['Region'].unique()),
                    multi=True,
                    clearable=False,
                    style={'border': '1px solid grey', 'border-radius': '5px'}
                ),
            ], style={'width': '30%', 'padding': '10px'}),
            
            # Line Chart
            html.Div([dcc.Graph(id='line-chart-cumulative')],
                     style={'width': '65%', 'padding': '20px', 'background-color': '#FBFCFC', 'border-radius': '5px'})
        ], style={'display': 'flex', 'justify-content': 'center'}),
    
    # 3D Globe for Tactics by Country
    html.Div([
        html.H3("3D Globe: Tactics by Country", style={
            'text-align': 'center',
            'color': 'grey',
            'font-size': '24px',
            'margin-bottom': '10px',
            'border': '2px solid black'
        }),
        dcc.Graph(figure=fig)  # This embeds the globe figure directly into the layout
    ], style={'width': '90%', 'padding': '20px', 'background-color': '#FBFCFC', 'border-radius': '5px'}),
    
    ]),

    # Stacked bar chart for techniques used by threat actors
    html.Div([
        html.H3("Stacked Bar Chart: Techniques Used by Threat Actors", style={
            'text-align': 'center',
            'color': 'grey',
            'font-size': '24px',
            'margin-bottom': '10px',
            'border': '2px solid black'
        }),
        html.Div([
            # Stacked Bar Chart
            html.Div([dcc.Graph(figure=px.bar(
                threat_actor_techniques_grouped,
                x='source name',
                y='technique_count',
                color='tactics',
                #title="Stacked Bar Chart: Techniques Used by Threat Actors",
                labels={'source name': 'Threat Actor', 'technique_count': 'Number of Techniques', 'tactics': 'Tactic'},
                barmode='stack'
            ))],
                style={'width': '100%', 'padding': '20px', 'background-color': '#FBFCFC', 'border-radius': '5px'})
        ], style={'display': 'flex', 'justify-content': 'center'}),
    ], style={'padding': '20px'})


])


# Callback for updating the bar chart based on dropdown selection
@app.callback(
    Output('dynamic-bar-chart', 'figure'),
    [Input('actor-dropdown', 'value')]  # Updated to actor-dropdown
)
def update_bar_chart(selected_technique):
    unique_techniques = fv4_data.groupby('source name', as_index=False)['Threat Actor Score'].mean()

    if selected_technique == 'Top 10':
        filtered_data = unique_techniques.nlargest(10, 'Threat Actor Score')
    else:
        filtered_data = unique_techniques[unique_techniques['source name'] == selected_technique]
    
    filtered_data['Threat Actor Score'] = filtered_data['Threat Actor Score'].round(0)


    if filtered_data.empty:
        return go.Figure(go.Bar(x=[], y=[], text="No data available"))

    fig = go.Figure([go.Bar(y=filtered_data['source name'], x=filtered_data['Threat Actor Score'],
                            orientation='h', marker_color='#FF0000', width=0.4)])

    fig.update_traces(text=filtered_data['Threat Actor Score'], textposition='auto', textfont_size=14)

    fig.update_layout(
        #title="Top 10 Techniques by Threat Actor Score" if selected_technique == 'Top 10' else f"Selected Technique: {selected_technique}",
        xaxis_title="Threat Actor Score",
        yaxis_title="Threat Actor",
        plot_bgcolor='#FBFCFC',
        paper_bgcolor='#FBFCFC',
        bargap=0.2,
        height=600
    )

    return fig

# Callback for updating the pie chart based on tactic and region selection
@app.callback(
    Output('dynamic-pie-chart', 'figure'),
    [Input('tactic-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_pie_chart(selected_tactic, selected_regions):
    if not selected_regions:
        selected_regions = scored_data['Region'].unique()

    filtered_data = scored_data[(scored_data['tactics'] == selected_tactic) & (scored_data['Region'].isin(selected_regions))]
    region_counts = filtered_data['Region'].value_counts()

    fig = px.pie(values=region_counts.values, names=region_counts.index, 
                 #title=f"Distribution of Techniques by Region for {selected_tactic}",
                 labels={'value': 'Count'})

    fig.update_traces(textinfo='percent+label')

    fig.update_layout(
        plot_bgcolor='#FBFCFC',
        paper_bgcolor='#FBFCFC',
    )

    return fig

# Callback for updating the heatmap based on region selection
@app.callback(
    Output('dynamic-heatmap', 'figure'),
    [Input('region-heatmap-dropdown', 'value')]
)
def update_heatmap(selected_region):
    filtered_data = scored_data_expanded[scored_data_expanded['Region'] == selected_region]
    grouped_data = filtered_data.groupby(['defenses bypassed', 'tactics']).size().reset_index(name='technique_count')
    grouped_data_filtered = grouped_data[(grouped_data['technique_count'] > 0) & (pd.notna(grouped_data['technique_count']))]

    heatmap_fig = go.Figure(data=go.Heatmap(
        z=grouped_data_filtered['technique_count'],
        x=grouped_data_filtered['defenses bypassed'],
        y=grouped_data_filtered['tactics'],
        colorscale='Plasma',
        colorbar=dict(title="Technique Count")
    ))

    heatmap_fig.update_layout(
        #title=f"Defenses Bypassed vs. Tactics in {selected_region}",
        xaxis_title="Defenses Bypassed",
        yaxis_title="Tactics",
        font=dict(family="Arial", size=12, color="black"),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return heatmap_fig

# Callback for updating the line chart based on selected regions
@app.callback(
    Output('line-chart-cumulative', 'figure'),
    [Input('region-dropdown_LC', 'value')]
)
def update_line_chart(selected_regions):
    fig = go.Figure()

    if not selected_regions:
        selected_regions = region_year_cumulative['Region'].unique()

    for region in selected_regions:
        region_data = region_year_cumulative[region_year_cumulative['Region'] == region]
        
        fig.add_trace(go.Scatter(
            x=region_data['Year'], 
            y=region_data['Cumulative Score'], 
            mode='lines+markers',
            name=region
        ))

    fig.update_layout(
        #title="Cumulative Prevalence Score Over Time by Region",
        xaxis_title="Year",
        yaxis_title="Cumulative Prevalence Score",
        legend_title="Region",
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified'
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
