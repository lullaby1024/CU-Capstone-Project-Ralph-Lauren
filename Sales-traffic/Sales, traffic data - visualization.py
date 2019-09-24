# # Data Visualization

# ## Sales vs. date, grouped by group divisions
sales_by_group = df.groupby(['group name', 'date']).sum().reset_index()[['group name', 'date', 'sales unit', 'sales retail']]
sales_by_group.head(5)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ax = sales_by_group.pivot(index="date", 
                          columns="group name", 
                          values="sales unit").plot(x_compat=True, figsize=(15, 8))
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.set_ylabel('sales unit')
plt.show()

ax = sales_by_group.pivot(index="date", 
                          columns="group name", 
                          values="sales retail").plot(x_compat=True, figsize=(15, 8))
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.set_ylabel('Sales Retail', fontsize=15)
ax.set_xlabel('Date', fontsize=15)
ax.set_title('Sales Retail by Group vs. Date', fontsize=20)
# ax.set_ylim(5000, 30000)
plt.show()


# ## Sales vs. date, grouped by stores and group divisions
fig = plt.figure()
cnt = 0
    
for store, grp in df.groupby('store name'):
    cnt += 1
    ax = fig.add_subplot(3, 2, cnt)
    grp.pivot(index="date", 
              columns="group name",
              values="sales retail").plot(x_compat=True, figsize=(20, 15), 
                                          title=store, ax=ax)
    plt.legend(loc=1, fontsize=8)
    plt.ylabel('Sales Retail', fontsize=15)
    plt.xlabel('Date', fontsize=15)

plt.subplots_adjust(hspace = .4)
_ = plt.suptitle('Sales Retail by Stores and Group Divisions vs. Date',
                 fontsize=40)

plt.show()


# **Observation**
# - Similar pattern for `sales unit` and `sales retail` across stores/group divisions
#     - Two peaks at Nov-Dec, 2017 and Nov-Dec, 2018.
#         - Sales season (Thanksgiving, Christmas)
#     - Nearly stationary time series.
#         - Mean/variance does not seem to be dependant of time.
#     - Seasonality, but no obvious trends
# - Overall revenue ranking
#     - *By store*: LAKE BUENA VISTA FOA >= LAS VEGAS NORTH > ORLANDO FOA > LANCASTER FSC > LAS VEGAS SOUTH > TANNERSVILLE FOC
#     - *By group division*: **Men's apparel** > women's apparel > accessories and fragrance > children's >  others
# - Traffic has a very similar pattern as sales, shown by the previous graphs. Interestingly, **women's apparel** seems overwhelming among all divisions.
# - Remarks
#     - Unlike other stores, *LANCASTER FSC* and *TANNERSVILLE FOC* do not sell accessories and fragrance.
#         - Special note for *TANNERSVILLE FOC* where children's is the top division (out of the two divisions on record).

# **Caveats and additional remarks**
# - Because of the two extreme peak values, data at the bottom are hard to see.
#     - Possible remedy: zoom-in
# - Note that some (portions of) divisions appear to be flat in some plots.
#     - Zero sales across time?
#     - Might be related to the time when the store was first opened.
# - Multicollinearity between `sales unit`, `sales retail` and `traffic out`.
#     - Need to be treated in model fitting.

import plotly.graph_objs as go

fig = go.Figure()

for i in sales_by_group['group name'].unique():
    fig.add_trace(go.Scatter(x = sales_by_group.date, 
                             y = sales_by_group[sales_by_group['group name'] == i]['sales retail'],
                             name = i))

fig.update_layout(
    width = 800,
    height = 500,
    paper_bgcolor = 'white',
    title_text = 'Sales Retail with Range Slider and Selectors',
    xaxis=go.layout.XAxis(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1 Month",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6 Month",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="1 Year",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ),
    legend = go.layout.Legend(font = dict(size = 8))
)

fig.show()

cmp = plt.cm.get_cmap('viridis')
sales_by_store = df.groupby(['store name', 'group name']).sum().reset_index()[['store name', 'group name', 'sales retail']]
_ = sales_by_store.pivot(index='store name',
                         columns='group name', 
                         values='sales retail').plot.bar(stacked=True, 
                                                         figsize=(15, 8), 
                                                         cmap=cmp)
_ = plt.xticks(rotation='horizontal')
_ = plt.ylabel('Sales Retail', fontsize=15)
_ = plt.xlabel('Store Name', fontsize=15)
_ = plt.legend(loc='best')
_ = plt.title('Sales Retail by Group Division vs. Store', fontsize=25)


# ## Scatterplot Matrix for Correlation

import seaborn as sns
_ = sns.pairplot(df[['sales retail', 'sales unit', 'traffic out', 'group name']],
                 hue='group name', plot_kws = {'alpha': 0.6})
_ = plt.suptitle('Scatterplot Matrix for Correlation')

