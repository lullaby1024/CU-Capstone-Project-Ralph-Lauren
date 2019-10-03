

# # Data Visualization

# ## Sales vs. date, grouped by group divisions

sales_by_group = df.groupby(['group_name', 'date']).sum().reset_index()[['group_name', 'date', 'sales_unit', 'sales_retail']]
sales_by_group.head(5)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ax = sales_by_group.pivot(index="date",
                          columns="group_name",
                          values="sales_unit").plot(x_compat=True, figsize=(15, 8))
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.set_ylabel('Sales unit')
plt.show()

ax = sales_by_group.pivot(index="date",
                          columns="group_name",
                          values="sales_retail").plot(x_compat=True, figsize=(15, 8))
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.set_ylabel('Sales Retail', fontsize=15)
ax.set_xlabel('Date', fontsize=15)
ax.set_title('Sales Retail by Group vs. Date', fontsize=20)
# ax.set_ylim(5000, 30000)
plt.savefig('./img/Sales Retail by Group vs. Date.png')
plt.show()


# ## Sales vs. date, grouped by stores and group divisions
fig = plt.figure()
cnt = 0

for store, grp in df.groupby('store_name'):
    cnt += 1
    ax = fig.add_subplot(3, 2, cnt)
    grp.pivot(index="date",
              columns="group_name",
              values="sales_retail").plot(x_compat=True, figsize=(20, 15),
                                          title=store, ax=ax)
        
                                          plt.legend(loc=1, fontsize=8)
                                          plt.ylabel('Sales Retail', fontsize=15)
                                          plt.xlabel('Date', fontsize=15)

plt.subplots_adjust(hspace = .4)
_ = plt.suptitle('Sales Retail by Stores and Group Divisions vs. Date',
                 fontsize=40)
plt.savefig('./img/Sales Retail by Stores and Group Divisions vs. Date.png')
plt.show()


# **Observation**
# - Similar pattern for `sales unit` and `sales retail` across stores/group divisions
#     - Two peaks at Nov-Dec, 2017 and Nov-Dec, 2018.
#         - Sales season (Thanksgiving, Christmas)
#     - Nearly stationary time series.
#         - Mean/variance does not seem to be dependant of time.
#     - Seasonality, but no obvious trends
# - Overall revenue ranking
#     - *By store*: LAKE BUENA VISTA FOA >= LAS VEGAS NORTH > ORLANDO FOA > TANNERSVILLE FOC > LANCASTER FSC > LAS VEGAS SOUTH
#     - *By group division*: **Men's apparel** > women's apparel > accessories and fragrance > children's >  others

# **Caveats and additional remarks**
# - Because of the two extreme peak values, data at the bottom are hard to see.
#     - Possible remedy: zoom-in
# - Note that some (portions of) divisions appear to be flat in some plots.
#     - Zero sales across time?
#     - Might be related to the time when the store was first opened.
# - Multicollinearity between `sales_unit`, `sales_retail` and `traffic`.
#     - Need to be treated in model fitting.

# ## Plotly for Sales Data

import plotly.graph_objs as go

def plotly_sales(df):
    
    fig = go.Figure()
    
    for i in df.group_name.unique():
        fig.add_trace(go.Scatter(x = df.date,
                                 y = df[df.group_name == i].sales_retail,
                                 name = i))
    
    fig.update_layout(
                      width = 800,
                      height = 500,
                      paper_bgcolor = 'white',
                      title_text = 'Sales Retail',
                      # with Range Slider and Selectors
                      #         xaxis=go.layout.XAxis(
                      #             rangeselector=dict(
                      #                 buttons=list([
                      #                     dict(count=1,
                      #                          label="1 Month",
                      #                          step="month",
                      #                          stepmode="backward"),
                      #                     dict(count=6,
                      #                          label="6 Month",
                      #                          step="month",
                      #                          stepmode="backward"),
                      #                     dict(count=1,
                      #                          label="1 Year",
                      #                          step="year",
                      #                          stepmode="backward"),
                      #                     dict(step="all")
                      #                 ])
                      #             ),
                      #             rangeslider=dict(
                      #                 visible=True
                      #             ),
                      #             type="date"
                      #         ),
                      legend = go.layout.Legend(font = dict(size = 8))
                      )

fig.show()
plotly_sales(sales_by_group)


# ## Stacked Histogram for Sales Retail by Group Division vs. Store

# In[35]:


cmp = plt.cm.get_cmap('viridis')
sales_by_store = df.groupby(['store_name', 'group_name']).sum().reset_index()[['store_name', 'group_name', 'sales_retail']]
_ = sales_by_store.pivot(index='store_name',
                         columns='group_name',
                         values='sales_retail').plot.bar(stacked=True,
                                                         figsize=(15, 8),
                                                         cmap=cmp)
_ = plt.xticks(rotation='horizontal')
_ = plt.ylabel('Sales Retail', fontsize=15)
_ = plt.xlabel('Store Name', fontsize=15)
_ = plt.legend(loc='best')
_ = plt.title('Sales Retail by Group Division vs. Store', fontsize=25)
plt.savefig('./img/Sales Retail by Group Division vs. Store.png')
plt.show()


# ## Scatterplot Matrix for Correlation

# In[37]:


import seaborn as sns
_ = sns.pairplot(df[['sales_retail', 'sales_unit', 'traffic', 'group_name']],
                 hue='group_name', plot_kws = {'alpha': 0.6})
_ = plt.suptitle('Scatterplot Matrix for Correlation')
plt.savefig('./img/Scatterplot Matrix for Correlation.png')