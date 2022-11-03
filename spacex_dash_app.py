import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout

sites = spacex_df['Launch Site'].unique().tolist()
sites.insert(0, 'All Sites')

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                        # Task 1:Add a Launch Site Drop-down Input Component
                                dcc.Dropdown(id='site_dropdown',
                                options=[{'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True
                                ),
                                html.Br(),
                # TASK: Add a pie chart to show the total successful launches count for all sites
                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                html.Div(dcc.Graph(id='success-pie-chart')),
                 html.Br(),

                html.P("Payload range (Kg):"),
                # TASK: Add a slider to select payload range
                dcc.RangeSlider(id='payload_slider',
                                 min=0, max=10000, step=1000, marks={0: '0', 1000: '1000', 2000: '2000',
                                                                                   3000: '3000', 4000: '4000', 5000: '5000',
                                                                                   6000: '6000', 7000: '7000', 8000: '8000',
                                                                                   9000: '9000', 10000: '10000'},
                                value=[min_payload, max_payload]),

                # TASK: Add a scatter chart to show the correlation between payload and launch success
                 html.Div(dcc.Graph(id='success_payload_scatter_chart')),
                                ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site_dropdown', component_property='value')
            )
def get_pie_chart(site_dropdown):
    if site_dropdown == 'ALL':
        fig = px.pie(spacex_df, values='class',
        names='Launch Site', title='Success Launch All sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_dropdown].groupby(['Launch Site', 'class']). \
            size().reset_index(name='class count')
        title = f"Total Success Launches for site {site_dropdown}"
        filtered_df = filtered_df
        fig = px.pie(filtered_df, values='class count', names='class', title=title)
        return fig


# Task 3: Add a Range Slider to Select Payload
dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0 kg',
                       100: '100'},
                value=[min_payload, max_payload])
# TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot


@app.callback(Output(component_id='success_payload_scatter_chart', component_property='figure'),
        [Input(component_id='site_dropdown', component_property='value'),
        Input(component_id='payload_slider', component_property='value')])

def get_scatter_plot(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        low_value, high_value=payload_slider
        range_df=spacex_df[(spacex_df['Payload Mass (kg)'] >= low_value) & (
            spacex_df['Payload Mass (kg)'] <= high_value)]
        fig=px.scatter(range_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                hover_data=['Booster Version'],
                  title='Success Launch for All Boosters with Respect to Payload Mass (kg)')
        return fig
    else:
        Site_df2=range_df[range_df['Launch Site'] == site_dropdown]
        fig=px.scatter(Site_df2, x='Payload Mass (kg)', y='class',
                        color='Booster Version Category', hover_data=['Booster Version'],
                        title='Success Launch for' + site_dropdown + 'Site With Respect to Payload Mass (kg)')
        return fig



# Run the app
if __name__ == '__main__':
    # REVIEW8: Adding dev_tools_ui=False, dev_tools_props_check=False can prevent error appearing before calling callback function
      app.run_server()