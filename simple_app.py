from dash import Dash, dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.express as px

# Instantiate our App and incorporate BOOTSTRAP theme stylesheet
app = Dash(__name__)

# Incorporate data into App
df = px.data.gapminder()


# Build the layout to define what will be displayed on the page
app.layout = html.Div(className='container', children=[
   
    html.H1("Life Expectancy vs. GDP"),
        

    #### SCATTER PLOT WITH SLIDER INTERACTION ####
    dcc.Graph(id='fig-slider-output', className='plot'),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='fig-year-slider'
    ),


    #### LINE PLOT WITH DROPDOWN INTERACTION ####
    html.Div(className='two-columns', children=[
        html.Div(className='left-column', children=[
            dcc.Graph(id='my-output2', className='plot'),
        ]),

       html.Div(className='right-column', children=[
           "Country: ",
            #dcc.Input(id='my-input2', value='United States', type='text')
            dcc.Dropdown(
                id='my-input2',
                options=df['country'].unique(),
                value='United States'  # Default value
            ),
       ]),
       
    ]),

])


# callback is used to create app interactivity
@callback(
    Output(component_id='fig-slider-output', component_property='figure'),
    Input(component_id='fig-year-slider', component_property='value')
)
def update_output_div(input_value):
    fig = px.scatter(data_frame=df[df['year'] == input_value], x="gdpPercap", y="lifeExp", 
                 size="pop",
                 color="continent", 
                 hover_name="country", 
                 log_x=True,
                 size_max=60, 
                 range_y=[30, 90], 
                 animation_frame='year')
    fig.update_layout(transition_duration=500)

    return fig




@callback(
    Output(component_id='my-output2', component_property='figure'),
    Input(component_id='my-input2', component_property='value')
)
def update_output_div(input_value):
    fig2 = px.line(data_frame=df[df['country'] == input_value].sort_values(by='year'), 
              x="year", y="gdpPercap", 
                 hover_name="gdpPercap",
                 title=input_value
                 )
    fig2.update_layout()

    return fig2
  

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)