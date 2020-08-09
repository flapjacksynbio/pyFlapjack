from scipy.optimize import curve_fit
import numpy as np

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
