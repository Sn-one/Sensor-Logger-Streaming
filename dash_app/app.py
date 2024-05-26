import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import sqlalchemy
from dash_bootstrap_templates import load_figure_template

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
    engine = sqlalchemy.create_engine("postgresql://admin:admin@postgres:5432/logs")

    # Using context managers for handling database connections
    with engine.connect() as conn:
        df = pd.read_sql(
            "SELECT * FROM sensor_metrics ORDER BY enddate DESC LIMIT 10", conn
        )

    # Accelerometer Metrics Plot
    accelerometer_metrics = go.Figure()
    accelerometer_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_accel_x"],
            name="X"
        )
    )
    accelerometer_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_accel_y"],
            name="Y"
        )
    )
    accelerometer_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_accel_z"],
            name="Z"
        )
    )
    accelerometer_metrics.update_layout(
        barmode="group",
        title="Average Accelerometer Metrics",
        xaxis_title="Time",
        yaxis_title="Average Value",
        template="plotly_dark",
    )

    # Gyroscope Metrics Plot
    gyroscope_metrics = go.Figure()
    gyroscope_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_gyro_x"],
            name="X"
        )
    )
    gyroscope_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_gyro_y"],
            name="Y"
        )
    )
    gyroscope_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_gyro_z"],
            name="Z"
        )
    )
    gyroscope_metrics.update_layout(
        barmode="group",
        title="Average Gyroscope Metrics",
        xaxis_title="Time",
        yaxis_title="Average Value",
        template="plotly_dark",
    )

    # Gravity Metrics Plot
    gravity_metrics = go.Figure()
    gravity_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_gravity_x"],
            name="X"
        )
    )
    gravity_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_gravity_y"],
            name="Y"
        )
    )
    gravity_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_gravity_z"],
            name="Z"
        )
    )
    gravity_metrics.update_layout(
        barmode="group",
        title="Average Gravity Metrics",
        xaxis_title="Time",
        yaxis_title="Average Value",
        template="plotly_dark",
    )

    # Orientation Metrics Plot
    orientation_metrics = go.Figure()
    orientation_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_orientation_pitch"],
            name="Pitch"
        )
    )
    orientation_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_orientation_roll"],
            name="Roll"
        )
    )
    orientation_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_orientation_yaw"],
            name="Yaw"
        )
    )
    orientation_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_orientation_qw"],
            name="QW"
        )
    )
    orientation_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_orientation_qx"],
            name="QX"
        )
    )
    orientation_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_orientation_qy"],
            name="QY"
        )
    )
    orientation_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_orientation_qz"],
            name="QZ"
        )
    )
    orientation_metrics.update_layout(
        barmode="group",
        title="Average Orientation Metrics",
        xaxis_title="Time",
        yaxis_title="Average Value",
        template="plotly_dark",
    )

    # Magnetometer Metrics Plot
    magnetometer_metrics = go.Figure()
    magnetometer_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_magnetometer_x"],
            name="X"
        )
    )
    magnetometer_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_magnetometer_y"],
            name="Y"
        )
    )
    magnetometer_metrics.add_trace(
        go.Bar(
            x=df["startdate"],
            y=df["avg_magnetometer_z"],
            name="Z"
        )
    )
    magnetometer_metrics.update_layout(
        barmode="group",
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
