#!/usr/bin/env python3

import csv
import datetime
import re
import sys

import chart_studio.plotly as py
import inotify.adapters
import plotly.graph_objects as go


def main():
    log = {}

    hands_re = re.compile(r"-- starting hand #(\d+)")
    stacks_re = re.compile(r'\|? #(\d+) "(.+?) @ [^\s]+?" \((\d+)\)')

    with open(sys.argv[1]) as f:
        # CSV is in reverse chronological order because reasons
        csv_lines = list(csv.DictReader(f))
        for row in reversed(csv_lines):
            entry = row["entry"]

            # keep track of what number hand we're on
            hands_m = hands_re.match(entry)
            if hands_m:
                current_hand = int(hands_m.group(1))

            # log stacks for those who played
            elif entry.startswith("Player stacks:"):
                for m in stacks_re.finditer(entry):
                    seat_num, player_name, stack = m.groups()

                    if player_name not in log:
                        log[player_name] = []

                    data_point = (current_hand, int(stack))
                    log[player_name].append(data_point)

    # chart_studio.tools.set_credentials_file(username="googlebleh", api_key="https://youtu.be/oHg5SJYRHA0")

    # fig = go.Figure()
    graphs = []
    for player_name, stacklog in log.items():
        hands, stack_values = zip(*stacklog)
        graph_obj = go.Scatter(x=hands, y=stack_values, mode="lines+markers", name=player_name)
        graphs.append(graph_obj)
    #     fig.add_trace(graph_obj)
    # fig.show()

    plot_name = "pokernow-{}".format(datetime.date.today().strftime("%Y%m%d"))
    py.plot(graphs, auto_open=False, filename=plot_name, sharing="public")


if __name__ == "__main__":
    main()

    i = inotify.adapters.Inotify()
    i.add_watch(sys.argv[1])
    print("listening")
    for event in i.event_gen(yield_nones=False):
        _, type_names, path, filename = event
        print(event)
        main()
