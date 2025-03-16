import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from scipy.stats import linregress

#读取数据
df = pd.read_excel("清洗后经济数据(1).xlsx", sheet_name="清洗后经济数据")

#分离中国和美国数据
df_china = df[df['国家'] == '中国'].copy()
df_usa = df[df['国家'] == '美国'].copy()

#处理年份列
df_china['年份'] = pd.to_datetime(df_china['date']).dt.year
df_usa['年份'] = pd.to_datetime(df_usa['DATE']).dt.year

#图表1：双轴折线图（GDP增长率对比）
#计算增长率
for df_country in [df_china, df_usa]:
    df_country.sort_values('年份', inplace=True)
    df_country['实际GDP增长率'] = df_country['实际GDP（元人民币）'].pct_change() * 100

fig1 = go.Figure()
#添加中国数据
fig1.add_trace(go.Scatter(
    x=df_china['年份'],
    y=df_china['实际GDP增长率'],
    name='China',
    line=dict(color='#1f77b4')
))
#添加美国数据（使用次坐标轴）
fig1.add_trace(go.Scatter(
    x=df_usa['年份'],
    y=df_usa['实际GDP增长率'],
    name='US',
    line=dict(color='#ff7f0e'),
    yaxis="y2"
))

#添加关键事件标注
events = [
    (2008, "2008 Financial Crisis", "#d62728"),
    (2020, "COVID-19", "#2ca02c")
]
for year, text, color in events:
    fig1.add_vline(
        x=year, line_width=2, line_dash="dash",
        line_color=color, annotation_text=text,
        annotation_position="top left"
    )

fig1.update_layout(
    title="Comparison of RGDP Growth Rate between China and US（1978-2023）",
    xaxis=dict(title="Year"),
    yaxis=dict(title="RGDP growth rate in China (%)", showgrid=False),
    yaxis2=dict(
        title="RGDP growth rate in US (%)",
        overlaying="y",
        side="right",
        showgrid=False
    ),
    legend=dict(x=0.02, y=0.95),
    annotations=[dict(
        text="Data Sources：World Bank Open Data&Federal Reserve Economic Data",
        xref="paper", yref="paper",
        x=0, y=-0.15, showarrow=False
    )]
)

#图表2：堆叠面积图（中国消费与投资占比）
df_china['消费率'] = df_china['最终消费支出（元人民币）'] / df_china['实际GDP（元人民币）'] * 100
df_china['资本形成率'] = df_china['资本形成总额（元人民币）'] / df_china['实际GDP（元人民币）'] * 100

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=df_china['年份'],
    y=df_china['消费率'],
    stackgroup='one',
    name='Consumption Rate',
    line=dict(width=0.5, color='#17becf')
))
fig2.add_trace(go.Scatter(
    x=df_china['年份'],
    y=df_china['资本形成率'],
    stackgroup='one',
    name='Capital Formation Rate',
    line=dict(width=0.5, color='#e377c2')
))

#标注投资驱动阶段
fig2.add_vrect(
    x0=2001, x1=2013,
    fillcolor="#ff7f0e", opacity=0.1,
    annotation_text="Infrastructure Boom", 
    annotation_position="top left"
)

fig2.update_layout(
    title="Consumption Rate and Capital Formation Rate in China（1978-2023）",
    xaxis=dict(title="Year"),
    yaxis=dict(title="Rate(%)", range=[0, 100]),
    hovermode="x unified",
    annotations=[dict(
        text="Data Resources:World Bank Open Data",
        xref="paper", yref="paper",
        x=0, y=-0.15, showarrow=False
    )]
)

#图表3：散点图（青年失业率与GDP增长）
years = [2020, 2021, 2022, 2023]
gdp = [101356700223100, 109919790043400, 113163160234882, 119103725812005]
unemployment = [12.678, 12.422, 14.811, 15.745]

gdp_growth = []
for i in range(1, len(gdp)):
    growth = (gdp[i] - gdp[i-1]) / gdp[i-1] * 100
    gdp_growth.append(round(growth, 2))
gdp_2019 = 99137372966400
growth_2020 = (gdp[0] - gdp_2019) / gdp_2019 * 100
gdp_growth = [round(growth_2020, 2)] + gdp_growth  # [2.24, 8.45, 2.95, 5.25]

df = pd.DataFrame({
    'Year': years,
    'GDP增长率 (%)': gdp_growth,
    '青年失业率 (%)': unemployment
})

#计算回归线
x = df['GDP增长率 (%)']
y = df['青年失业率 (%)']
coefficients = np.polyfit(x, y, 1)
trendline = np.poly1d(coefficients)

#绘制散点图
fig3 = px.scatter(
    df,
    x='GDP增长率 (%)',
    y='青年失业率 (%)',
    hover_name='Year',
    title='Relationship between RGDP Growth Rate and YUR（2020-2023）',
    labels={'GDP增长率 (%)': 'RGDP Growth Rate（%）', '青年失业率 (%)': 'YUR（%）'},
    text='Year'
)

# 添加回归线
fig3.add_trace(
    go.Scatter(
        x=x,
        y=trendline(x),
        mode='lines',
        name='Regression Line',
        line=dict(color='red', dash='dash'),
        hovertemplate='Trend: %{y:.2f}%<extra></extra>'
    )
)

# 设置图表样式
fig3.update_layout(
    annotations=[
        dict(
            x=0.95,
            y=0.05,
            xref='paper',
            yref='paper',
            text='Data Resources:World Bank Open Data',
            showarrow=False,
            font=dict(size=10)
        )
    ],
    hoverlabel=dict(bgcolor="white", font_size=12),
    title_font=dict(size=20),
    legend_title='Graph'
)

#保存图表
fig1.write_html("Comparison of RGDP.html")
fig2.write_html("Consumption Rate and Capital Formation Rate.html")
fig3.write_html("Relationship between YUR and RGDP growth.html")
