import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spacy


def plotBar(df, x, title):

    fig = px.bar(df, x=x, title=title)
    return fig


def barplot(df, x, y, color, color_continuous_scale, title):
    class_eng = df.groupby(x, as_index=False).agg({y: 'sum', })
    fig = px.bar(class_eng,
                 x=x,
                 y=y,
                 color=color,
                 color_continuous_scale=px.colors.sequential.RdBu,
                 title=title)
    return fig


def plotPie(names, values, title):

    fig = px.pie(
        names=names,
        values=values,
        title=title,
        hole=.3,
        color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def add_tracePlot(df):
    line = df.groupby('date', as_index=False).agg({'total_engagement': 'sum'})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=line.date, y=line.total_engagement,
                             mode='lines+markers'))
    return fig


def scatterplot(df):
    december = df.loc[df['month'] == 12]
    day_december = december.groupby('day', as_index=False).agg({
        'total_engagement': 'sum'})

    fig = px.scatter(day_december,
                     x='day',
                     y='total_engagement',
                     color_continuous_scale='Rainbow',
                     color='total_engagement',
                     size='total_engagement',
                     title='Most engaged days in December')
    return fig


def barplot1(df, x, y, color, color_continuous_scale, title):
    tot_eng = df.groupby('user_name', as_index=False).agg(
        {'total_engagement': 'sum'}).sort_values('total_engagement', ascending=False).head(10)

    fig = px.bar(tot_eng,
                 x=x,
                 y=y,
                 color=color,
                 color_continuous_scale=color_continuous_scale,
                 title=title)
    return fig
