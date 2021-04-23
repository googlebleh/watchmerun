#!/usr/bin/env python3

import csv
import re

import chart_studio.plotly as py
import plotly.graph_objects as go

log = {}

regex = re.compile(r'\|? #(\d+) "(.+?) @ \w+" \((\d+)\)')

with open("poker_now_log_vpWH6-qgxi4ajqq6p7ftY7GgE.csv") as f:
    csv_lines = list(csv.DictReader(f))
    for row in reversed(csv_lines):
        entry = row["entry"]
        if entry.startswith("Player stacks:"):
            for m in regex.finditer(entry):
                seat_num, player_name, stack = m.groups()

                if player_name not in log:
                    log[player_name] = []

                log[player_name].append(int(stack))

# chart_studio.tools.set_credentials_file(username="googlebleh", api_key="https://youtu.be/oHg5SJYRHA0")

# fig = go.Figure()
graphs = []
for player_name, stacklog in log.items():
    graph_obj = go.Scatter(y=stacklog, mode="lines+markers", name=player_name)
    graphs.append(graph_obj)
#     fig.add_trace(graph_obj)
# fig.show()

py.plot(graphs, sharing="public")
