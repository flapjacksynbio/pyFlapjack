from scipy.optimize import curve_fit
import numpy as np
import plotly.graph_objects as go

# Layout plots returned by flapjack
def layout_print(fig, width=3.3, height=1.5, font_size=6):
    '''
    Layout figure optimized for print at 300dpi

    fig = figure to layout
    width,height = size in inches
    font_size = font size in pts

    Returns:
    fig = figure with correct layout
    '''
        
    width = width*300
    height = height*300
    font_size = font_size * 300/72
    fig.update_layout(  autosize=False,
                        width=width, height=height,
                        margin=go.layout.Margin(
                            l=50,
                            r=50,
                            b=50,
                            t=50,
                            pad=0
                        ),
                        paper_bgcolor="rgb(255,255,255)",
                        template='simple_white',
                        font_size=font_size
                    )
    for a in fig['layout']['annotations']:
        a['font'] = dict(size=font_size)
    fig.update_traces(marker=dict(size=6), line=dict(width=4), selector=dict(type='scatter'))
    fig.update_traces(marker=dict(size=6), line=dict(width=4), selector=dict(type='line'))
    fig.update_traces(line=dict(width=0), selector=dict(fill="toself"))
    fig.update_yaxes(linewidth=3, 
                    tickwidth=3, 
                    title_font=dict(size=font_size), 
                    tickfont=dict(size=font_size))
    fig.update_xaxes(linewidth=3, 
                    tickwidth=3, 
                    title_font=dict(size=font_size), 
                    tickfont=dict(size=font_size))
    return fig

# Model functions for fitting to data
# -----------------------------------------------------------------------------------
def exponential_growth(t, y0, k):
    od = y0*np.exp(k*t)
    return(od)

def exponential_growth_rate(t, y0, k):
    return(k)

def gompertz(t, y0, ymax, um, l):
    A = np.log(ymax/y0)
    log_rel_od = (A*np.exp(-np.exp((((um*np.exp(1))/A)*(l-t))+1)))
    od = y0 * np.exp(log_rel_od)
    return(od)

def gompertz_growth_rate(t, y0, ymax, um, l):
    A = np.log(ymax/y0)
    gr = um *np.exp((np.exp(1)* um *(l - t))/A - \
            np.exp((np.exp(1)* um *(l - t))/A + 1) + 2)
    return(gr)

def hill(x, a, b, k, n):
    return (a*(x/k)**n + b) / (1 + (x/k)**n)

def fit_curve(func, data, x, y, **kwargs):
    z,C = curve_fit(func, data[x], data[y], **kwargs)
    std = np.sqrt(np.diag(C))
    return z,std
