import streamlit as st  # pyright: ignore[reportMissingImports]
import random
from datetime import datetime

st.title("Sensor Monitor")

if "sensor_history" not in st.session_state:
	st.session_state.sensor_history = []


@st.fragment(run_every="1.5s")
def show_sensor_reading():
	reading = random.uniform(0, 100)
	if reading < 40:
		status = "Low"
	elif reading <= 70:
		status = "Moderate"
	else:
		status = "High"

	status_level = {"Low": 1, "Moderate": 2, "High": 3}[status]
	st.session_state.sensor_history.append(
		{"time": datetime.now(), "status": status, "level": status_level}
	)
	st.session_state.sensor_history = st.session_state.sensor_history[-60:]

	st.metric("Sensor value", f"{reading:.2f}")
	st.write(f"Flag: **{status}**")
	st.vega_lite_chart(
		st.session_state.sensor_history,
		{
			"mark": {"type": "line", "point": True},
			"encoding": {
				"x": {"field": "time", "type": "temporal", "title": "Time"},
				"y": {
					"field": "level",
					"type": "quantitative",
					"scale": {"domain": [1, 3], "nice": False},
					"axis": {
						"title": "Flag",
						"values": [1, 2, 3],
						"labelExpr": "datum.value === 1 ? 'Low' : datum.value === 2 ? 'Moderate' : 'High'",
					},
				},
			},
		},
	)


show_sensor_reading()
