# watchmerun
fill in the one feature pokernow doesn't have: seeing each players' stack over time

just graphs data for now. prob add more stats later

### setup
```bash
# to plot
pip install plotly

# to share with the world
pip install chart_studio
```
if you want to share with the world, do this too:
https://plotly.com/python/getting-started-with-chart-studio/#initialization-for-online-plotting

### todo
some events are a lil off. e.g.:
- when a player busts, they're out the next hand, so their stack size is not reported. then when they buy in, it can look like their stack size didn't change
- when someone loses a bunch, then sits out the next hand, their stack size might not decrease until they join the table again. haven't verified this bug exists tho
