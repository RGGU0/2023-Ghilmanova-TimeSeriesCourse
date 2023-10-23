import numpy as np
import pandas as pd

# for visualization
import plotly
from plotly.subplots import make_subplots
from plotly.offline import init_notebook_mode
import plotly.graph_objs as go
import plotly.express as px
plotly.offline.init_notebook_mode(connected=True)

def plot_bestmatch_results_and_time(ts, wind_size, bestmatch_results1, bestmatch_results2, time1, time2):
    """
    Visualize the best match results.

    Parameters
    ----------
    ts : numpy.ndarrray
        Time series.

    query : numpy.ndarrray
        Query.

    bestmatch_results : dict 
        The output data found by the best match algorithm.  
    """

    # INSERT YOUR CODE

    ts_len = len(ts)

    fig = make_subplots(rows=2, cols=2,
    specs=[[{}, {"rowspan": 2}],
           [{}, None]], subplot_titles=("brute_force", '',"hotsax"), horizontal_spacing=0.04)

    fig.add_trace(go.Scatter(x=np.arange(ts_len), y=ts, 
                line=dict(color=px.colors.qualitative.Plotly[4])),
                row=1, col=1)
    fig.add_trace(go.Scatter(x=np.arange(ts_len // 2), y=ts, 
                line=dict(color=px.colors.qualitative.Plotly[5])),
                row=1, col=1)
    fig.add_trace(go.Scatter(x=np.arange(ts_len), y=ts, 
                line=dict(color=px.colors.qualitative.Plotly[4])),
                row=2, col=1)
    fig.add_trace(go.Scatter(x=np.arange(ts_len // 2), y=ts, 
                line=dict(color=px.colors.qualitative.Plotly[5])),
                row=2, col=1)
    for ind, i in enumerate(bestmatch_results1):
      start_res = int(i)
      stop_res = int(i + wind_size)
      fig.add_vrect(
          x0=start_res,
          x1=stop_res,
          fillcolor=px.colors.qualitative.Plotly[0],
          opacity=0.5,
          line_width=0,
          row=1,
          col=1,
          annotation_text="#"+str(ind),
          annotation_position="top right",
      )
    for ind, i in enumerate(bestmatch_results2):
      start_res = int(i)
      stop_res = int(i + wind_size)
      fig.add_vrect(
          x0=start_res,
          x1=stop_res,
          fillcolor=px.colors.qualitative.Plotly[1],
          opacity=0.5,
          line_width=0,
          row=2, 
          col=1,
          annotation_text="#"+str(ind),
          annotation_position="top right",
      )
    fig.add_trace(go.Bar(go.Bar(
      x = ['brute force'],
      y = [time1],
      marker_color=px.colors.qualitative.Plotly[0]
    )),row=1, col=2)
    fig.add_trace(go.Bar(go.Bar(
      x = ['hotsax'],
      y =[time2],
      marker_color=px.colors.qualitative.Plotly[1]
    )),row=1, col=2)    

    fig.update_xaxes(showgrid=False,
                     linecolor='#000',
                     ticks="outside",
                     tickfont=dict(size=18, color='black'),
                     linewidth=1,
                     tickwidth=1,
                     mirror=True)
    fig.update_yaxes(showgrid=False,
                     linecolor='#000',
                     ticks="outside",
                     tickfont=dict(size=18, color='black'),
                     zeroline=False,
                     linewidth=1,
                     tickwidth=1,
                     mirror=True)

    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor='rgba(0,0,0,0)',
                      showlegend=False,
                      title_x=0.5)
                  
    fig.show(renderer="colab")

def plot_bestmatch_results(ts, wind_size, bestmatch_results1, bestmatch_results2):
    """
    Visualize the best match results.

    Parameters
    ----------
    ts : numpy.ndarrray
        Time series.

    query : numpy.ndarrray
        Query.

    bestmatch_results : dict 
        The output data found by the best match algorithm.  
    """

    # INSERT YOUR CODE

    ts_len = len(ts)

    fig = make_subplots(rows=2, cols=1,
    row_heights=[0.5, 0.5], subplot_titles=("brute_force", '',"hotsax"), horizontal_spacing=0.04)

    fig.add_trace(go.Scatter(x=np.arange(ts_len), y=ts, 
                line=dict(color=px.colors.qualitative.Plotly[4])),
                row=1, col=1)
    fig.add_trace(go.Scatter(x=np.arange(ts_len // 2), y=ts, 
                line=dict(color=px.colors.qualitative.Plotly[5])),
                row=1, col=1)
    fig.add_trace(go.Scatter(x=np.arange(ts_len), y=ts, 
                line=dict(color=px.colors.qualitative.Plotly[4])),
                row=2, col=1)
    fig.add_trace(go.Scatter(x=np.arange(ts_len // 2), y=ts, 
                line=dict(color=px.colors.qualitative.Plotly[5])),
                row=2, col=1)
    for ind, i in enumerate(bestmatch_results1):
      start_res = int(i)
      stop_res = int(i + wind_size)
      fig.add_vrect(
          x0=start_res,
          x1=stop_res,
          fillcolor=px.colors.qualitative.Plotly[0],
          opacity=0.5,
          line_width=0,
          row=1, 
          col=1,
          annotation_text="#"+str(ind),
          annotation_position="top right",          
      )
    for ind, i in enumerate(bestmatch_results2):
      start_res = int(i)
      stop_res = int(i + wind_size)
      fig.add_vrect(
          x0=start_res,
          x1=stop_res,
          fillcolor=px.colors.qualitative.Plotly[1],
          opacity=0.5,
          line_width=0,
          row=2, 
          col=1,
          annotation_text="#"+str(ind),
          annotation_position="top right",         
      )

    fig.update_xaxes(showgrid=False,
                     linecolor='#000',
                     ticks="outside",
                     tickfont=dict(size=18, color='black'),
                     linewidth=1,
                     tickwidth=1,
                     mirror=True)
    fig.update_yaxes(showgrid=False,
                     linecolor='#000',
                     ticks="outside",
                     tickfont=dict(size=18, color='black'),
                     zeroline=False,
                     linewidth=1,
                     tickwidth=1,
                     mirror=True)

    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor='rgba(0,0,0,0)',
                      showlegend=False,
                      title_x=0.5)
                  
    fig.show(renderer="colab")

def plot_bestmatch_results_one(ts, wind_size, bestmatch_results1):
    """
    Visualize the best match results.

    Parameters
    ----------
    ts : numpy.ndarrray
        Time series.

    query : numpy.ndarrray
        Query.

    bestmatch_results : dict 
        The output data found by the best match algorithm.  
    """

    # INSERT YOUR CODE

    ts_len = len(ts)

    fig = make_subplots(rows=1, cols=1, subplot_titles=("brute_force", '',"hotsax"), horizontal_spacing=0.04)

    fig.add_trace(go.Scatter(x=np.arange(ts_len), y=ts, 
                line=dict(color=px.colors.qualitative.Plotly[0])),
                row=1, col=1)
    for ind, i in enumerate(bestmatch_results1):
      start_res = int(i)
      stop_res = int(i + wind_size)
      fig.add_vrect(
          x0=start_res,
          x1=stop_res,
          fillcolor=px.colors.qualitative.Plotly[1],
          opacity=0.5,
          line_width=0,
          row=1, 
          col=1,
          annotation_text="#"+str(ind),
          annotation_position="top right",
      )
    fig.update_xaxes(showgrid=False,
                     linecolor='#000',
                     ticks="outside",
                     tickfont=dict(size=18, color='black'),
                     linewidth=1,
                     tickwidth=1,
                     mirror=True)
    fig.update_yaxes(showgrid=False,
                     linecolor='#000',
                     ticks="outside",
                     tickfont=dict(size=18, color='black'),
                     zeroline=False,
                     linewidth=1,
                     tickwidth=1,
                     mirror=True)

    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor='rgba(0,0,0,0)',
                      showlegend=False,
                      title_x=0.5)
                  
    fig.show(renderer="colab")
    