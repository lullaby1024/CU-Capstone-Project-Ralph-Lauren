import pandas as pd
import sys
import numpy as np
# from math import pi
from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import Select, \
    ColumnDataSource, TableColumn, \
    DataTable, RangeSlider, CheckboxGroup, CheckboxButtonGroup, \
    Panel, Tabs, Div, Paragraph, TextInput, FactorRange, \
    ColorBar, LinearColorMapper, BasicTicker, DatetimeTickFormatter, HoverTool
from bokeh.layouts import row, column
from bokeh.tile_providers import get_provider, Vendors
from bokeh.palettes import d3, brewer, Viridis256
import math

# ----------------------------  Constants ----------------------------

try:
    STORE = sys.argv[1].replace('_', ' ')  #TODO: make this selectable on UI
except:
    print('Store name should be specified using "--args STORE".')
    print('Defaulted to "ORLANDO FOA".')
    STORE = 'ORLANDO FOA'

CITY_MAP = {'ORLANDO FOA': 'ORLANDO',
            'LANCASTER FSC': 'LANCASTER',
            'LAS VEGAS SOUTH': 'LAS VEGAS',
            'LAS VEGAS NORTH': 'LAS VEGAS'}

CITY = CITY_MAP[STORE]

# Constant location for stores
LAT_STORE, LON_STORE = {}, {}

LAT_STORE['ORLANDO FOA'] = 28.473595
LAT_STORE['LAKE BUENA VISTA FOA'] = 28.387852
LAT_STORE['LANCASTER FSC'] = 40.025636
LAT_STORE['LAS VEGAS NORTH'] = 36.170727
LAT_STORE['LAS VEGAS SOUTH'] = 36.056725

LON_STORE['ORLANDO FOA'] = -81.451615
LON_STORE['LAKE BUENA VISTA FOA'] = -81.493674
LON_STORE['LANCASTER FSC'] = -76.217167
LON_STORE['LAS VEGAS NORTH'] = -115.157651
LON_STORE['LAS VEGAS SOUTH'] = -115.170121

# Constants in the data set
RANKS = ['minor', 'moderate', 'important', 'significant', 'major']
RANKS_INT = ['(0, 20]', '(20, 40]', '(40, 60]', '(60, 80]', '(80, 100]']
YEARS = ['2017', '2018', '2019']
COLS = ['title', 'description', 'labels', 'category', \
        'year', 'is_annual', 'date', 'start_time', 'duration', \
        'venue_name', 'scope', 'venue_type', 'est_capacity', 'distance', 'longitude', 'latitude', \
        'rank', 'impact_linear']

# -------------------------- Static Divs --------------------------
DIV_FILTER = Div(text="""<b>Filters</b>""", style={'font-size': '200%'})

DIV_YEAR = Div(text="""<b>Year</b>""")
DIV_IS_ANNUAL = Div(text="""<b>Is Annual</b>""")
DIV_START_TIME = Div(text="""<b>Start Time</b>""")

DIV_RANK = Div(text="""<b>Rank</b>""")
ANNT_RANK = Paragraph(text="""Minor: 0-20, Moderate: 21-40, Important: 41-60, 
Significant: 61-80, Major: 81-100""")

DIV_SCOPE = Div(text="""<b>Scope</b>""")
DIV_VENUE_TYPE = Div(text="""<b>Venue Type</b>""")
DIV_DISTANCE = Div(text="""<b>Distance</b>""")

DIV_CATEGORY = Div(text="""<b>Category</b>""")

# ----------------------------  Tab 1 ----------------------------
DIV_TABLE = Div(text="""<b>Data Table</b>""", style={'font-size': '200%'}, height=20)
ANNT_TABLE = Div(text="""
<ul>
    <li>Use filters on the left to filter the table.</li>
    <li>Click on the column name to sort the table by a specific column.</li>
    <li>Click on the cells to reveal values. </li>
    <li>Explanations for columns:
        <ul>
            <li>
                <i>is_annual.</i> An event is determined to be annual if it occurred across the three years.
            </li>
            <li>
                <i>venue_type.</i> Classification is based on 
                <a href="http://places2.csail.mit.edu/index.html">Places365-CNN</a> combined with NLP for <i>venue_name</i>.
            </li>
            <li>
                <i>est_capacity.</i> This is the estimated capacity of the venue using reversed engineering of <i>rank</i>.
            </li>
            <li>
                <i>impact_linear.</i> This is a derived metric for event impact, caculated by <i>rank</i>/<i>distance</i>.
            </li>
            <li>Units: <i>duration (days), distance (miles).</i></li>
        </ul>
    </li>
</ul>""")

# ----------------------------  Tab 2 ----------------------------
DIV_MAP = Div(text="""<b>Events Filtered for Distance <= 50 miles</b>""", style={'font-size': '200%'}, height=20)
ANNT_MAP = Div(text="""
<ul>
    <li>Store is marked by <b>asterisk</b>.</li>
    <li>Ranks are reflected by <b>sizes</b> of the circles so that points with larger ranks are larger on the graph.</li>
    <li>Use filters on the left to filter the map.</li>
    <li>Hover over the points to reveal <i>title, labels, venue, date and duration.</i></li>
    <li>Use the tool bar on the side to zoom-in/out and save the plot.</li>
</ul>""")
DIV_TOP_VENUES = Div(text="""<b>Top Venues by Rank</b>""", style={'font-size': '200%'}, height=20)

VENUES_MAP = {'ORLANDO': """<ul> \
<li>Universal Orlando</li> <li>Universal Orlando Resort</li> \
<li>Winter Park</li> <li>Lake Eola Park</li> <li>EDC Orlando</li> </ul>""",
              'LANCASTER': """<ul> \
              <li>Lancaster County Convention Center</li> <li>Clipper Magazine Stadium</li> \
<li>Eden Resort & Suites</li> <li>Lancaster Host Resort</li></ul>""",
              'LAS VEGAS': """<li>World Market Center Las Vegas</li> \
<li>Las Vegas Motor Speedway</li> <li>EDC</li> <li>Sam's Town Hotel & Gambling Hall</li> \
<li>Caesars Palace</li></ul>"""}

ANNT_TOP_VENUES = Div(text=VENUES_MAP[CITY])

# ----------------------------  Tab 3 ----------------------------
DIV_COUNT = Div(text="""<b>Count of Events by Category and Rank</b>""", style={'font-size': '200%'}, height=20)
ANNT_COUNT = Div(text="""
<ul>
    <li>Hover over the bars to reveal the exact count for each rank category.</li>
    <li>Use the tool bar on the side to zoom-in/out and save the plot.</li>
</ul>
""")
DIV_CAT_COUNT = Div(text="""<b>Count of Events by Category Over Time</b>""", style={'font-size': '200%'}, height=20)
ANNT_CAT_COUNT = Div(text="""
<ul>
    <li>Use filter on the left to filter the category.</li>
    <li>Hover over the points to reveal the exact date, count and category.</li>
    <li>Use the tool bar on the side to zoom-in/out and save the plot.</li>
</ul>
""")

# ----------------------------  Tab 4 ----------------------------
DIV_WORDCLOUD = Div(text="""<b>Word Cloud for Event Labels</b>""", style={'font-size': '200%'}, height=20)
ANNT_WORDCLOUD = Div(text="""
<ul>
    <li>The more a specific word appears in <i>labels</i>, the <b>bigger and bolder</b> it appears in the cloud.</li>
    <li>Use the tool bar on the side to zoom-in/out and save the plot.</li>
</ul>
""")

# ----------------------------  Tab 5 ----------------------------
DIV_PAIR = Div(text="""<b>Correlation Heatmap for Sales vs. Category Impacts</b>""",
               style={'font-size': '200%'}, height=20)
ANNT_PAIR = Div(text="""
<ul>
    <li>A lighter yellowish color implies a greater positive correlation, 
    while a darker blueish one implies a greater negative correlation.</li>
    <li>Use the tool bar on the side to zoom-in/out and save the plot.</li>
    <li>Hover over the tiles to reveal the exact correlation.</li>
</ul>
""")


# ----------------------------  Preprocessing ----------------------------

def read_events_data():
    events_raw = pd.read_csv(join(dirname(__file__), 'data', 'events_' + STORE + '.csv'))
    events_raw = events_raw[COLS]
    events_raw['is_annual'] = events_raw['is_annual'].replace({0: 'no', 1: 'yes'})
    events_raw['year'] = events_raw['year'].astype(str)
    # Round digits for visualization
    events_raw['distance'] = round(events_raw['distance'], 2)
    events_raw['duration'] = round(events_raw['duration'] / 86400, 1)  # Turn seconds into days
    events_raw['est_capacity'] = round(events_raw['est_capacity'])
    events_raw['impact_linear'] = round(events_raw['impact_linear'], 2)
    # events_raw['impact_exp'] = events_raw.apply(lambda x: '{:.5E}'.format(x['impact_exp']), axis=1)

    return events_raw


def set_default_category(df):
    # For filters on category, get indexes for ['concerts', 'conferences', 'festivals']
    target = ['concerts', 'conferences', 'festivals']
    all_cat = sorted(df['category'].unique())
    return [all_cat.index(t) for t in target]


events_raw = read_events_data()

# ----------------------------  The First Tab: Data Table ----------------------------


def filter_events():
    selected = events[
        (events['rank'].between(rank1.value[0], rank1.value[1], inclusive=True)) &
        (events['distance'].between(distance1.value[0], distance1.value[1], inclusive=True)) &
        (events['scope'].isin([scope1.labels[i] for i in scope1.active])) &
        (events['category'].isin([category1.labels[i] for i in category1.active])) &
        (events['year'].isin([year1.labels[i] for i in year1.active])) &
        (events['is_annual'].isin([is_annual1.labels[i] for i in is_annual1.active])) &
        (events['start_time'].isin([start_time1.labels[i] for i in start_time1.active])) &
        (events['venue_type'].isin([venue_type1.labels[i] for i in venue_type1.active]))
    ]

    return selected.sort_values(['rank'], ascending=False)


def update_table():
    df = filter_events()
    new_src = ColumnDataSource(df)
    # Update data table
    src_tbl.data.update(new_src.data)

    # Update output cells
    try:
        selected_index = src_tbl.selected.indices[0]
        src_tbl_title.value = str(src_tbl.data["title"][selected_index])
        src_tbl_descript.value = str(src_tbl.data["description"][selected_index])
        src_tbl_label.value = str(src_tbl.data["labels"][selected_index])
        src_tbl_venue.value = str(src_tbl.data["venue_name"][selected_index])
    except IndexError:
        pass


events = events_raw.drop(['longitude', 'latitude'], axis=1)
col_tbl = [TableColumn(field=i, title=i) for i in events.columns]
src_tbl = ColumnDataSource(events)
data_table = DataTable(source=src_tbl, columns=col_tbl, width=1300)

# Input controls
rank1 = RangeSlider(title="Range of ranks", value=(61, 100), start=0, end=100, step=5)
distance1 = RangeSlider(title="Range of distances (miles)", value=(0, 30), start=0, end=max(events['distance']), step=5)
scope1 = CheckboxGroup(labels=list(events['scope'].unique()), active=[0, 1])
venue_type1 = CheckboxGroup(labels=['indoor', 'outdoor'], active=[0, 1])
category1 = CheckboxGroup(labels=list(sorted(events['category'].unique())), active=set_default_category(events))
year1 = CheckboxButtonGroup(labels=list(events['year'].unique()), active=[0, 1, 2])
start_time1 = CheckboxGroup(labels=list(sorted(events['start_time'].unique())), active=[0, 1])
is_annual1 = CheckboxGroup(labels=list(events['is_annual'].unique()), active=[0, 1])

update_table()  # initial load of the data

# Output controls
src_tbl_title = TextInput(value="", title="Title:")
src_tbl_descript = TextInput(value="", title="Description:")
src_tbl_label = TextInput(value="", title="Labels:")
src_tbl_venue = TextInput(value="", title="Venue:")

controls1 = [rank1, distance1, scope1, venue_type1, category1, year1, start_time1, is_annual1]
for control in controls1:
    if control in [rank1, distance1]:
        control.on_change('value', lambda attr, old, new: update_table())
    else:
        control.on_change('active', lambda attr, old, new: update_table())

src_tbl.selected.on_change('indices', lambda attr, old, new: update_table())

inputs = column(DIV_FILTER,
                DIV_YEAR, year1,
                row(column(DIV_IS_ANNUAL, is_annual1, width=100), column(DIV_START_TIME, start_time1, width=100)),
                DIV_RANK, rank1, ANNT_RANK,
                row(column(DIV_SCOPE, scope1, width=100), column(DIV_VENUE_TYPE, venue_type1, width=100)),
                DIV_DISTANCE, distance1,
                DIV_CATEGORY, category1,
                width=250)
outputs = column(DIV_TABLE, ANNT_TABLE, data_table,
                 src_tbl_title, src_tbl_descript, src_tbl_label, src_tbl_venue)
l1 = row(inputs, outputs)
tab1 = Panel(child=l1, title='Event Data Table')

# ----------------------------  The Second Tab: Map ----------------------------

def merc(lat, lon):
    # Converts (lat, lon) into (x, y) for plots
    r_major = 6378137.000
    x = r_major * math.radians(lon)
    scale = x / lon
    y = 180.0 / math.pi * math.log(math.tan(math.pi / 4.0 +
                                            lat * (math.pi / 180.0) / 2.0)) * scale
    return (x, y)


def filter_map():
    selected = events_map[
        (events_map['year'].isin([year2.labels[i] for i in year2.active])) &
        (events_map['is_annual'].isin([is_annual2.labels[i] for i in is_annual2.active])) &
        (events_map['start_time'].isin([start_time2.labels[i] for i in start_time2.active])) &
        (events_map['rank'].between(rank2.value[0], rank2.value[1], inclusive=True)) &
        (events_map['venue_type'].isin([venue_type2.labels[i] for i in venue_type2.active])) &
        (events_map['category'].isin([category2.labels[i] for i in category2.active]))
    ]

    return selected


def plot(tile_source, coords_store):

    # create plot and add tools
    p = figure(tools='hover,wheel_zoom,box_zoom,save,pan,reset,help',
               title="",
               tooltips=[("Title", "@title"),
                         ("Labels", "@labels"),
                         ("Venue Name", "@venue_name"),
                         ("Venue Type", "@venue_type"),
                         ("Estimated Capacity", "@est_capacity"),
                         ("Date", "@date"),
                         ("Duration", "@duration"),
                         ("Is Annual", "@is_annual"),
                         ("Start Time", "@start_time"),
                         ("Rank", "@rank"),
                         ("Linear Impact", "@impact_linear")],
               plot_width=700,
               plot_height=700)
    p.axis.visible = False
    p.add_tile(tile_source)

    # create point glyphs
    p.circle(x='coords_x',
             y='coords_y',
             source=src_map,
             size='size_by_rank',
             color='color_by_cat',
             legend_field='category',
             fill_alpha=0.3)

    p.legend.location = "top_right"

    p.asterisk(x=coords_store[0],
               y=coords_store[1],
               size=70,
               line_color="#f0027f",
               fill_color=None,
               line_width=3)

    return p


def plot_venues(src_url):
    p = figure(x_range=(0, 500), y_range=(0, 500),
               plot_width=500,
               plot_height=500)
    p.image_url(x=10, y=490, w=480, h=480,
                url='url',
                source=src_url)
    p.axis.visible = False
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    return p


def update_map():
    df = filter_map()
    new_src = ColumnDataSource(df)
    src_map.data.update(new_src.data)


events_map = events_raw.drop(['description'], axis=1)
# Keep one record for each event in each year
events_map = events_map.drop_duplicates(subset=['title', 'year'], keep='first')
events_map['month'] = pd.to_datetime(events_map['date'], format='%Y-%m-%d').dt.month
events_map = events_map[events_map['distance'] <= 50]  # Subset for a smaller distance
# Scope now only has locality.

# Aggregate some features for plotting
events_map['coords_x'] = events_map.apply(lambda x: merc(x['latitude'], x['longitude'])[0], axis=1)
events_map['coords_y'] = events_map.apply(lambda x: merc(x['latitude'], x['longitude'])[1], axis=1)
events_map['size_by_rank'] = events_map['rank'] / 2
# Create a colormap for category
cat_to_map = sorted(events_map['category'].unique())
colors = d3['Category20'][len(cat_to_map)]
cmp = dict(zip(cat_to_map, colors))
events_map['color_by_cat'] = events_map['category'].map(cmp)

COORDS_STORE = merc(LAT_STORE[STORE], LON_STORE[STORE])

src_map = ColumnDataSource(events_map)
tile_source = get_provider(Vendors.CARTODBPOSITRON)
p1 = plot(tile_source, COORDS_STORE)

# Input controls
year2 = CheckboxButtonGroup(labels=list(events_map['year'].unique()), active=[0, 1, 2])
rank2 = RangeSlider(title="Range of ranks", value=(61, 100), start=0, end=100, step=5)
category2 = CheckboxGroup(labels=list(cat_to_map), active=set_default_category(events_map))
venue_type2 = CheckboxGroup(labels=['indoor', 'outdoor'], active=[0, 1])
start_time2 = CheckboxGroup(labels=list(sorted(events_map['start_time'].unique())), active=[0, 1])
is_annual2 = CheckboxGroup(labels=list(events['is_annual'].unique()), active=[0, 1])

update_map()  # initial load of the data

controls2 = [year2, is_annual2, start_time2, rank2, venue_type2, category2]
for control in controls2:
    if control == rank2:
        control.on_change('value', lambda attr, old, new: update_map())
    else:
        control.on_change('active', lambda attr, old, new: update_map())

inputs = column(DIV_FILTER,
                DIV_YEAR, year2,
                row(column(DIV_IS_ANNUAL, is_annual2, width=100), column(DIV_START_TIME, start_time2, width=100)),
                DIV_RANK, rank2, ANNT_RANK,
                DIV_VENUE_TYPE, venue_type2,
                DIV_CATEGORY, category2,
                width=300)

src_url = ColumnDataSource({'url': ['bokeh_app/static/top_venues_' + CITY + '.png']})
p2 = plot_venues(src_url)

outputs = row(
    column(DIV_MAP, ANNT_MAP, p1),
    column(DIV_TOP_VENUES, ANNT_TOP_VENUES, p2)
)
l2 = row(inputs, outputs)
tab2 = Panel(child=l2, title='Event Map')

# ----------------------------  The Third Tab: (stacked + grouped) Bar plot ----------------------------


def plot_bar(factors, src_bar):

    # create plot and add tools
    p = figure(x_range=FactorRange(*factors),
               tools='hover,box_zoom,save,pan,reset,help',
               tooltips=[("Minor", "@minor"),
                         ("Moderate", "@moderate"),
                         ("Important", "@important"),
                         ("Significant", "@significant"),
                         ("Major", "@major")],
               title="",
               y_axis_label='Count',
               plot_width=1000,
               plot_height=400)

    # create a quad glyph for stacked histogram
    p.vbar_stack(
        RANKS,
        x='x',
        width=0.8,
        color=brewer['YlGnBu'][len(RANKS)][::-1],
        source=src_bar,
        legend_label=[i + ': ' + j for i, j in zip(RANKS, RANKS_INT)])

    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_right"
    # p.legend.orientation = "horizontal"

    return p


def plot_scatter(src_scatter):
    # create plot and add tools

    hover = HoverTool(tooltips=[('Date', '@date{%F}'),
                                ("Category", "@category"),
                                ("Counts", "@counts")],
                      formatters={'date': 'datetime'})

    p = figure(tools=[hover, 'box_zoom,save,pan,reset,help'],
               x_axis_type="datetime",
               x_axis_label='Date',
               y_axis_label='Counts',
               plot_width=800,
               plot_height=350)

    p.scatter(x='date',
              y='counts',
              color='color_by_cat',
              legend_field='category',
              source=src_scatter,
              alpha=0.8,
              size=5)

    p.legend.location = "top_right"
    p.xaxis.formatter = DatetimeTickFormatter(
        months=['%Y-%m'],
    )

    return p


def update_scatter():
    selected = category_counts[category_counts['category'].isin([category3.labels[i] for i in category3.active])]
    new_src = ColumnDataSource(selected)
    src_scatter.data.update(new_src.data)


events_counts = events_raw[['year', 'category', 'rank']]
# Cut rank into five groups
events_counts['rank'] = pd.cut(events_counts['rank'],
                               bins=[0, 20, 40, 60, 80, 100],
                               labels=RANKS)

factors = [(str(i), j) for i in YEARS for j in sorted(events_raw['category'].unique())]
new_idx = pd.MultiIndex.from_tuples(factors, names=('year', 'category'))
# Shape = (n_year * n_category, n_rank)
counts = events_counts.pivot_table(index=['year', 'category'],
                                   columns=['rank'],
                                   aggfunc=len,
                                   fill_value=0)  # Missing categories for zero counts
counts = counts.reindex(new_idx, fill_value=0)
# Sanity check
for i in RANKS:
    if i not in counts.columns:  # If we miss rank category
        counts[i] = [0] * len(counts)  # Append a column of 0's
counts = counts[RANKS]  # Reorder columns

src_bar = ColumnDataSource(data=dict(
    x=factors,
    minor=list(counts['minor']),
    moderate=list(counts['moderate']),
    important=list(counts['important']),
    significant=list(counts['significant']),
    major=list(counts['major'])
))

p3 = plot_bar(factors, src_bar)

category_counts = events_raw.groupby(['date', 'category']).size().reset_index(name='counts')
category_counts['date'] = pd.to_datetime(category_counts['date'], format='%Y-%m-%d')
# Create a colormap for category
cat_scatter = sorted(category_counts['category'].unique())
colors_scatter = d3['Category20'][len(cat_scatter)]
cmp_scatter = dict(zip(cat_scatter, colors_scatter))
category_counts['color_by_cat'] = category_counts['category'].map(cmp_scatter)
src_scatter = ColumnDataSource(category_counts)

p4 = plot_scatter(src_scatter)

category3 = CheckboxGroup(labels=list(cat_scatter), active=set_default_category(category_counts))

update_scatter()

category3.on_change('active', lambda attr, old, new: update_scatter())

l3 = column(
    column(DIV_COUNT, ANNT_COUNT, p3),
    row(column(DIV_FILTER, DIV_CATEGORY, category3, width=200),
        column(DIV_CAT_COUNT, ANNT_CAT_COUNT, p4))
)

tab3 = Panel(child=l3, title='Event Count')

# ----------------------------  Fourth Tab: Word Cloud ----------------------------


def plot_wordcloud():
    p = figure(x_range=(0, 1200), y_range=(0, 500),
               plot_width=1000,
               plot_height=450)
    p.image_url(x=10, y=490, w=1180, h=480,
                url='url',
                source=src_url)
    p.axis.visible = False
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    return p


src_url = ColumnDataSource({'url': ['bokeh_app/static/wordcloud_' + STORE + '.png']})

wordcloud = plot_wordcloud()

l4 = column(DIV_WORDCLOUD, ANNT_WORDCLOUD, wordcloud)

tab4 = Panel(child=l4, title='Event Word Cloud')

# ----------------------------  The Fifth Tab: Scatterplot Matrix ----------------------------
# sales_raw = pd.read_csv(join(dirname(__file__), 'data', 'sales_traffic_' + store_choice.value + '.csv'))
# def plot_pair():
#
#     mapper = LinearColorMapper(
#         palette=Viridis256, low=src_pair.data['value'].min(), high=src_pair.data['value'].max())
#
#     x_ran = list(np.unique(src_pair.data['all_columns_1']))
#     x_ran.remove('sales_cleaned')
#     x_range = sorted(x_ran) + ['sales_cleaned']
#
#     y_ran = list(np.unique(src_pair.data['all_columns_2']))
#     y_ran.remove('sales_cleaned')
#     y_range = sorted(y_ran) + ['sales_cleaned']
#
#     # Define a figure and tools
#     p = figure(
#         tools="hover,box_select,pan,wheel_zoom,box_zoom,reset,help",
#         tooltips=[("Correlation", "@value")],
#         plot_width=700,
#         plot_height=700,
#         title="",
#         x_range=x_range,
#         y_range=y_range,
#         toolbar_location="right",
#         x_axis_location="below")
#
#     p.xgrid.grid_line_color = None
#     p.ygrid.grid_line_color = None
#     p.xaxis.major_label_orientation = pi / 4
#     p.yaxis.major_label_orientation = pi / 4
#
#     # Create rectangle for heatmap
#     p.rect(
#         x="all_columns_1",
#         y="all_columns_2",
#         width=1,
#         height=1,
#         source=src_pair,
#         line_color=None,
#         fill_color=transform('value', mapper))
#
#     # Add legend
#     color_bar = ColorBar(
#         color_mapper=mapper,
#         location=(0, 0),
#         ticker=BasicTicker(desired_num_ticks=10))
#
#     p.add_layout(color_bar, 'right')
#
#     return p
#
#
# def filter_pair():
#     selected = sales_raw[['sales_cleaned'] + [category4.labels[i] + '_impact_linear' for i in category4.active]]
#     selected = selected.corr()
#     selected.index.name = 'all_columns_1'
#     selected.columns.name = 'all_columns_2'
#     selected = selected.stack().rename("value").reset_index()
#
#     return selected
#
#
# def update_pair():
#     df = filter_pair()
#     new_src = ColumnDataSource(df)
#     src_pair.data.update(new_src.data)
#
#
# corr = sales_raw.corr()
# corr.index.name = 'all_columns_1'
# corr.columns.name = 'all_columns_2'
# # Prepare data.frame in the right format
# corr = corr.stack().rename("value").reset_index()
#
# src_pair = ColumnDataSource(corr)
# p4 = plot_pair()
#
# # Input controls
# category4 = CheckboxGroup(labels=list(events_raw['category'].unique()), active=list(range(N_CATEGORIES)))
#
# update_pair()  # initial load of the data
#
# category4.on_change('active', lambda attr, old, new: update_pair())
#
# inputs = column(DIV_FILTER,
#                 DIV_CATEGORY, category4,
#                 width=200)
# outputs = column(DIV_PAIR, ANNT_PAIR, p4)
#
# l4 = row(inputs, outputs)
#
# tab4 = Panel(child=l4, title='Event Impact Correlation Heatmap')


# ----------------------------  Integrate The Tabs ----------------------------

# curdoc().add_root(Tabs(tabs=[index_tab, tab1, tab2, tab3, tab4]))
curdoc().add_root(Tabs(tabs=[tab1, tab2, tab3, tab4]))
# curdoc().add_root(p)