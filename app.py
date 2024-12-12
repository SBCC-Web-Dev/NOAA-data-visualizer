from dash import Dash, dcc, html
from figure import getFigure

app = Dash(__name__)

app.layout = html.Div([
        html.H1("NOAA Data Visualizer"),
        dcc.Graph(
            figure=getFigure(),
            style=dict(height="calc(100vh - 12rem)", aspectRatio="7 / 4")
        ),
    ], 
    style=dict(
        display="flex",
        flexDirection="column",
        alignItems="center",
        justifyItems="center",
    )
)

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, port=8050, dev_tools_silence_routes_logging=True)