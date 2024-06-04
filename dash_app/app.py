import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import sqlalchemy
from dash_bootstrap_templates import load_figure_template
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_password: str
    database_name: str
    database_username: str

    class Config:
        env_file = ".env_config"

settings = Settings()

# Load the dark theme for the entire app
load_figure_template("DARKLY")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div(
    [
        dbc.NavbarSimple(
            brand="Real-time Sensor Data Analysis",
            brand_href="#",
            color="dark",
            dark=True,
        ),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(id="accelerometer-metrics"), width=6),
                        dbc.Col(dcc.Graph(id="gyroscope-metrics"), width=6),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(id="gravity-metrics"), width=6),
                        dbc.Col(dcc.Graph(id="orientation-metrics"), width=6),
                    ]
                ),
                dbc.Row([dbc.Col(dcc.Graph(id="magnetometer-metrics"), width=12)]),
                dcc.Interval(
                    id="interval-component", interval=10 * 1000, n_intervals=0
                ),
            ],
            fluid=True,
        ),
    ]
)

@app.callback(
    [
        Output("accelerometer-metrics", "figure"),
        Output("gyroscope-metrics", "figure"),
        Output("gravity-metrics", "figure"),
        Output("orientation-metrics", "figure"),
        Output("magnetometer-metrics", "figure"),
    ],
    Input("interval-component", "n_intervals"),
)
def update_metrics(n):
    # Create database connection
    engine = sqlalchemy.create_engine(f"postgresql://{settings.database_username}:{settings.database_password}@postgres:5432/{settings.database_name}")

    # Fetch data for each sensor type
    with engine.connect() as conn:
        accelerometer_df = pd.read_sql(
            "SELECT * FROM sensor_metrics WHERE sensor_name='accelerometer' ORDER BY enddate DESC LIMIT 10", conn
        )
        gyroscope_df = pd.read_sql(
            "SELECT * FROM sensor_metrics WHERE sensor_name='gyroscope' ORDER BY enddate DESC LIMIT 10", conn
        )
        gravity_df = pd.read_sql(
            "SELECT * FROM sensor_metrics WHERE sensor_name='gravity' ORDER BY enddate DESC LIMIT 10", conn
        )
        orientation_df = pd.read_sql(
            "SELECT * FROM sensor_metrics WHERE sensor_name='orientation' ORDER BY enddate DESC LIMIT 10", conn
        )
        magnetometer_df = pd.read_sql(
            "SELECT * FROM sensor_metrics WHERE sensor_name='magnetometer' ORDER BY enddate DESC LIMIT 10", conn
        )

    # Accelerometer Metrics Plot
    accelerometer_metrics = go.Figure()
    if not accelerometer_df.empty:
        accelerometer_metrics.add_trace(
            go.Scatter(
                x=accelerometer_df["startdate"],
                y=accelerometer_df["avg_x_value"],
                mode='lines',
                name="X"
            )
        )
        accelerometer_metrics.add_trace(
            go.Scatter(
                x=accelerometer_df["startdate"],
                y=accelerometer_df["avg_y_value"],
                mode='lines',
                name="Y"
            )
        )
        accelerometer_metrics.add_trace(
            go.Scatter(
                x=accelerometer_df["startdate"],
                y=accelerometer_df["avg_z_value"],
                mode='lines',
                name="Z"
            )
        )
        accelerometer_metrics.update_layout(
            title="Average Accelerometer Metrics",
            xaxis_title="Time",
            yaxis_title="Average Value",
            template="plotly_dark",
        )

    # Gyroscope Metrics Plot
    gyroscope_metrics = go.Figure()
    if not gyroscope_df.empty:
        gyroscope_metrics.add_trace(
            go.Scatter(
                x=gyroscope_df["startdate"],
                y=gyroscope_df["avg_x_value"],
                mode='lines',
                name="X"
            )
        )
        gyroscope_metrics.add_trace(
            go.Scatter(
                x=gyroscope_df["startdate"],
                y=gyroscope_df["avg_y_value"],
                mode='lines',
                name="Y"
            )
        )
        gyroscope_metrics.add_trace(
            go.Scatter(
                x=gyroscope_df["startdate"],
                y=gyroscope_df["avg_z_value"],
                mode='lines',
                name="Z"
            )
        )
        gyroscope_metrics.update_layout(
            title="Average Gyroscope Metrics",
            xaxis_title="Time",
            yaxis_title="Average Value",
            template="plotly_dark",
        )

    # Gravity Metrics Plot
    gravity_metrics = go.Figure()
    if not gravity_df.empty:
        gravity_metrics.add_trace(
            go.Scatter(
                x=gravity_df["startdate"],
                y=gravity_df["avg_x_value"],
                mode='lines',
                name="X"
            )
        )
        gravity_metrics.add_trace(
            go.Scatter(
                x=gravity_df["startdate"],
                y=gravity_df["avg_y_value"],
                mode='lines',
                name="Y"
            )
        )
        gravity_metrics.add_trace(
            go.Scatter(
                x=gravity_df["startdate"],
                y=gravity_df["avg_z_value"],
                mode='lines',
                name="Z"
            )
        )
        gravity_metrics.update_layout(
            title="Average Gravity Metrics",
            xaxis_title="Time",
            yaxis_title="Average Value",
            template="plotly_dark",
        )

    # Orientation Metrics Plot
    orientation_metrics = go.Figure()
    if not orientation_df.empty:
        orientation_metrics.add_trace(
            go.Scatter(
                x=orientation_df["startdate"],
                y=orientation_df["avg_yaw"],
                mode='lines',
                name="Yaw"
            )
        )
        orientation_metrics.add_trace(
            go.Scatter(
                x=orientation_df["startdate"],
                y=orientation_df["avg_pitch"],
                mode='lines',
                name="Pitch"
            )
        )
        orientation_metrics.add_trace(
            go.Scatter(
                x=orientation_df["startdate"],
                y=orientation_df["avg_roll"],
                mode='lines',
                name="Roll"
            )
        )
        orientation_metrics.add_trace(
            go.Scatter(
                x=orientation_df["startdate"],
                y=orientation_df["avg_qw"],
                mode='lines',
                name="QW"
            )
        )
        orientation_metrics.add_trace(
            go.Scatter(
                x=orientation_df["startdate"],
                y=orientation_df["avg_qx"],
                mode='lines',
                name="QX"
            )
        )
        orientation_metrics.add_trace(
            go.Scatter(
                x=orientation_df["startdate"],
                y=orientation_df["avg_qy"],
                mode='lines',
                name="QY"
            )
        )
        orientation_metrics.add_trace(
            go.Scatter(
                x=orientation_df["startdate"],
                y=orientation_df["avg_qz"],
                mode='lines',
                name="QZ"
            )
        )
        orientation_metrics.update_layout(
            title="Average Orientation Metrics",
            xaxis_title="Time",
            yaxis_title="Average Value",
            template="plotly_dark",
        )

    # Magnetometer Metrics Plot
    magnetometer_metrics = go.Figure()
    if not magnetometer_df.empty:
        magnetometer_metrics.add_trace(
            go.Scatter(
                x=magnetometer_df["startdate"],
                y=magnetometer_df["avg_x_value"],
                mode='lines',
                name="X"
            )
        )
        magnetometer_metrics.add_trace(
            go.Scatter(
                x=magnetometer_df["startdate"],
                y=magnetometer_df["avg_y_value"],
                mode='lines',
                name="Y"
            )
        )
        magnetometer_metrics.add_trace(
            go.Scatter(
                x=magnetometer_df["startdate"],
                y=magnetometer_df["avg_z_value"],
                mode='lines',
                name="Z"
            )
        )
        magnetometer_metrics.update_layout(
            title="Average Magnetometer Metrics",
            xaxis_title="Time",
            yaxis_title="Average Value",
            template="plotly_dark",
        )

    return (
        accelerometer_metrics,
        gyroscope_metrics,
        gravity_metrics,
        orientation_metrics,
        magnetometer_metrics,
    )


if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0")
