import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


# Data for application

dublin_constits = ["Dublin Bay South", "Dublin Central", "Dublin South Central", "Dublin North West", "Dublin Mid West",
                  "Dublin South West", "Dublin West", "Dublin Fingal", "Dublin Rathdown", "Dún Laoghaire", "Dublin Bay North"]
    


cons_location = "https://raw.githubusercontent.com/LiamConnors/elections_ireland/main/constituencies.csv"
cons_data = pd.read_csv(cons_location, encoding="latin_1")
cons_data["Turnout"] =  cons_data["Total Poll"]/ cons_data["Total Electorate"]
cons_data["Spoiled_votes_percent"] =  cons_data["Spoiled"]/ cons_data["Total Poll"]
cons_data["In_Dublin"] = cons_data["Constituency Name"].apply(lambda x : "Dublin" if x in dublin_constits else "Outside Dublin")

cons_data.sort_values(by="Turnout", inplace=True)


# Refined data for graph 2
seat_numbers_in_constit = cons_data["SeatsinConstit"]
seat_numbers_in_constit = pd.DataFrame(seat_numbers_in_constit.value_counts())
seat_numbers_in_constit["number_of_seats"] = seat_numbers_in_constit.index



# Graphs

fig = px.bar(
             cons_data, x="Constituency Name", y="Turnout",
             hover_data=["Total Electorate", "Total Poll"],
             labels = {"Turnout":"Turnout %", "Constituency Name": "Constituency"},
             color="In_Dublin",
            
             title="Turnout % by constituency",
             height=700,
             width=1200)




fig.update_xaxes(categoryorder='total ascending')

fig2= px.pie(pd.DataFrame(seat_numbers_in_constit), values="SeatsinConstit", names="number_of_seats", labels = {"SeatsinConstit":"Number of constituencies", "number_of_seats": "Seats"},
            title="Breakdown by 3, 4 and 5 seat constituencies")


# App layout


app.layout = html.Div(children=[
    html.H1(children='Irish elections dash'),

    html.Div(children='''
        Charts, graphs and other stuff related to the 2020 general election
    '''),
             
#    html.Div(["Input: ",
#              dcc.Input(id='my-input', value='initial value', type='text')]),

#    html.Br(),
#   html.Div(id='my-output'),
    html.Br(),
    
    
    html.Div([
  
    
    
    dcc.Dropdown(
        id='seat-dropdown',
        options=[
            {'label': 'Count number', 'value': 3},
            {'label': 'Number of candidates', 'value': 2},
            {'label': 'Turnout %', 'value': 1},
            {'label': 'Spoilt votes %', 'value': 0}
        ],
        value=0
    ),
    
      dcc.Graph(id='graph-with-slider'),
    
    

]),
             
#html.P(children="Turnout % is the number of people who voted divided by the total registered electorate"),  

    #dcc.Graph(
    #    id='example-graph',
    #    figure=fig
    #   ),
            

            
])
    
## app callback functionality

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('seat-dropdown', 'value'))
def update_figure(selected_seat):
    if selected_seat == 0:
        filtered_df = cons_data
        y_value = "Spoiled_votes_percent"
        current_title = "Spoilt votes % by constituency"
    
    elif selected_seat == 1:
        filtered_df = cons_data
        y_value = "Turnout"
        current_title = "Turnout % by constituency"
        
    elif selected_seat == 2:
        filtered_df = cons_data
        y_value = "Number Of Candidates"
        current_title = "No. of candidates"
    elif selected_seat == 3:
        filtered_df = cons_data
        y_value = "Count Number"
        current_title = "Count number"       


    
    
    
    fig = px.bar(
             filtered_df, x="Constituency Name", y=y_value,
             hover_data=["Total Electorate", "Total Poll"],
             labels = {"Turnout":"Turnout %", "Constituency Name": "Constituency"},
             color="In_Dublin",
            
             title=current_title,
             height=700,
             width=1200)
    fig.update_xaxes(categoryorder='total ascending')
    fig.update_layout(transition_duration=0)

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
    
