# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
launch_sites = [{'label': 'All Sites', 'value': 'All Sites'}] + [{'label': item, 'value': item} for item in spacex_df["Launch Site"].value_counts().index]

app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
        ),
        dcc.Dropdown(
            id='site-dropdown',
            options=launch_sites,
            value='All Sites',
            placeholder="Select a Launch Site here",
            searchable=True
        ),
        html.Br(),

        html.Div(
            dcc.Graph(id='success-pie-chart')
        ),
        html.Br(),

        html.P("Payload range (Kg):"),
        dcc.RangeSlider(
            id='payload-slider',
            min=min_payload,
            max=max_payload,
            step=1000,
            value=[min_payload, max_payload],
            marks={2500: {'label': '2500 (Kg)'}, 5000: {'label': '5000 (Kg)'}, 7500: {'label': '7500 (Kg)'}}
        ),

        html.Div(
            dcc.Graph(id='success-payload-scatter-chart')
        ),
    ]
)

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'All Sites':
        site_df = spacex_df.groupby(['Launch Site'])['class'].sum().reset_index()
        fig = px.pie(site_df, values='class', names='Launch Site', title='Total Success Launches by Site')
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site]['class'].value_counts().reset_index()
        site_df.columns = ['class', 'count']
        fig = px.pie(site_df, values='count', names='class', title=f'Total Success Launches for {selected_site}')
    return fig

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'All Sites':
        site_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    else:
        site_df = spacex_df[(spacex_df['Launch Site'] == selected_site) & (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df



# Run the app
if __name__ == '__main__':
    app.run_server()
