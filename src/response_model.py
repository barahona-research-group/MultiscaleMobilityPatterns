import lmfit
import numpy as np
import pandas as pd
import scipy.sparse as sp


from sklearn import metrics


def compute_cvrmse(signal, prediction, around=False):
    """
    input: two timeseries
    output: CVRMSE
    """
    signal_mean = np.mean(signal)
    CVRMSE = np.sqrt(metrics.mean_absolute_error(signal, prediction)) / signal_mean

    if around:
        return np.around(CVRMSE, 3)

    else:
        return CVRMSE


def response(x, alpha, beta, lamb, m):
    """
    Defines response function for activation response model
    """
    y = (
        1
        + alpha / (beta - lamb) * (np.exp(-lamb * x) - np.exp(-beta * x))
        + alpha * m / beta * (1 - np.exp(-beta * x))
    )
    return np.nan_to_num(y)


def select_model(
    feature, base_value, name=None, decimals=3, use_window=True, use_m=True
):
    """
    input: time series and baseline value
    output: the response function is fitted to the normalised time series and optimal response                  parameters
            and CIs are returned with a model quality assesment
    """

    # Define model
    mod = lmfit.Model(response)

    # Define parameters
    params = lmfit.Parameters()
    params.add("alpha", value=1)
    params.add("beta", value=0.01, min=0.00001)

    params.add("lamb", value=0.1, min=0.00001)
    params.add("m", value=0)

    ################
    # Select Model #
    ################

    if use_window:

        # Compute MM
        signal = pd.Series(pd.Series(feature / base_value))
        signal_mm = np.roll(
            np.asarray(signal.rolling(window=7, win_type="triang").mean()), -3
        )
        x_mm = np.arange(len(signal))[np.nan_to_num(signal_mm) > 0]
        signal_mm = signal_mm[np.nan_to_num(signal_mm) > 0]

    else:
        signal = np.asarray(feature / base_value)
        x_mm = np.arange(len(signal))[np.nan_to_num(signal) > 0]
        signal_mm = signal[np.nan_to_num(signal) > 0]

    # Compute BIC for m=0
    params["m"].vary = False
    ls1 = mod.fit(signal_mm, params, x=x_mm)
    bic1 = ls1.bic
    params["m"].vary = True

    # Compute BIC for m!=0
    ls2 = mod.fit(signal_mm, params, x=x_mm)
    bic2 = ls2.bic

    # Compute DeltaBIC
    delta_bic = bic1 - bic2

    if use_m:

        if delta_bic > 0:
            ls = ls2
        else:
            ls = ls1

    else:

        ls = ls1

    ###########################
    # Report model parameters #
    ###########################

    # Compute CI
    ci = ls.conf_interval(sigmas=[2])

    # Get parameter names
    para = list(params.keys())

    # Create string
    result_string = str(name) + " & "

    # Add baseline value
    # result_string += str(np.around(base_value, 3)) + " & "

    # Add parameters and CIs
    for i in range(len(para)):
        # decimals = decimals
        # decimals_enough = False
        try:
            # while decimals_enough == False:
            #     if np.around(ci[para[i]][1][1], decimals) == 0:
            #         decimals += 1
            #     else:
            #         decimals_enough = True
            if i == 0:
                result_string += str(np.around(ci[para[i]][1][1], decimals + 2)) + " "
                result_string += (
                    str(
                        (
                            np.around(ci[para[i]][0][1], decimals + 2),
                            np.around(ci[para[i]][2][1], decimals + 2),
                        )
                    )
                    + " & "
                )
            else:
                result_string += str(np.around(1 / ci[para[i]][1][1], decimals)) + " "
                result_string += (
                    str(
                        (
                            np.around(1 / ci[para[i]][2][1], decimals),
                            np.around(1 / ci[para[i]][0][1], decimals),
                        )
                    )
                    + " & "
                )

        except:
            result_string += " 0 (-) & "

    # Add equilibrium
    alpha = ls.params["alpha"].value
    beta = ls.params["beta"].value
    m = ls.params["m"].value
    lim = np.around(100 * (m * alpha / beta + 1), 2)
    result_string += str(lim) + " & "

    # Add CI for equilibrium
    if m == 0:
        result_string += "- & "
    else:
        alpha_l = ci["alpha"][0][1]
        beta_l = ci["beta"][0][1]
        m_l = ci["m"][0][1]
        alpha_r = ci["alpha"][2][1]
        beta_r = ci["beta"][2][1]
        m_r = ci["m"][2][1]
        if m < 0 and alpha < 0:
            lim_l = np.around(100 * (m_r * alpha_r / beta_r + 1), 2)
            lim_r = np.around(100 * (m_l * alpha_l / beta_l + 1), 2)
        elif 0 < m and alpha < 0:
            lim_l = np.around(100 * (m_r * alpha_l / beta_l + 1), 2)
            lim_r = np.around(100 * (m_l * alpha_r / beta_r + 1), 2)
        elif m < 0 and 0 < alpha:
            lim_l = np.around(100 * (m_l * alpha_r / beta_l + 1), 2)
            lim_r = np.around(100 * (m_r * alpha_l / beta_r + 1), 2)
        else:
            lim_l = np.around(100 * (m_l * alpha_l / beta_r + 1), 2)
            lim_r = np.around(100 * (m_r * alpha_r / beta_l + 1), 2)
        result_string += str([lim_l, lim_r]) + " & "

    # Add CVRMSE
    prediction = ls.eval(ls.params, x=np.arange(len(signal)))
    CVRMSE = compute_cvrmse(signal, prediction)
    result_string += str(np.around(CVRMSE, 3)) + " & "

    # Add BIC
    result_string += str(np.around(bic1, 1)) + " & " + str(np.around(bic2, 1))

    # Print report
    print(result_string + "\n")

    return ls


def return_response_parameters(feature, base_value, use_window=True, use_m=True):
    """
    input: time series and baseline value
    output: the response function is fitted to the normalised time series
            and optimal response parameters are returned
    """

    # Define model
    mod = lmfit.Model(response)

    # Define parameters
    params = lmfit.Parameters()
    params.add("alpha", value=1)
    params.add("beta", value=0.01, min=0.00001)

    params.add("lamb", value=0.1, min=0.00001)
    params.add("m", value=0)

    if use_window:

        # Compute MM
        signal = pd.Series(pd.Series(feature / base_value))
        signal_mm = np.roll(
            np.asarray(signal.rolling(window=7, win_type="triang").mean()), -3
        )
        x_mm = np.arange(len(signal))[np.nan_to_num(signal_mm) > 0]
        signal_mm = signal_mm[np.nan_to_num(signal_mm) > 0]

    else:
        signal = np.asarray(feature / base_value)
        x_mm = np.arange(len(signal))[np.nan_to_num(signal) > 0]
        signal_mm = signal[np.nan_to_num(signal) > 0]

    # Compute BIC for m=0
    params["m"].vary = False
    ls1 = mod.fit(signal_mm, params, x=x_mm)
    bic1 = ls1.bic

    if use_m:
        # Compute BIC for m!=0
        params["m"].vary = True
        ls2 = mod.fit(signal_mm, params, x=x_mm)
        bic2 = ls2.bic

        # Compute DeltaBIC
        delta_bic = bic1 - bic2

        if delta_bic > 0:
            ls = ls2
        else:
            ls = ls1

    else:
        ls = ls1

    ###########################
    # Report model parameters #
    ###########################

    alpha = ls.params["alpha"].value
    beta = ls.params["beta"].value
    lamb = ls.params["lamb"].value
    m = ls.params["m"].value
    lim = np.around(100 * (m * alpha / beta + 1), 2)

    # Compute CVRMSE
    signal_mean = np.mean(signal)
    prediction = ls.eval(ls.params, x=np.arange(len(signal)))
    CVRMSE = np.sqrt(metrics.mean_absolute_error(signal, prediction)) / signal_mean

    return alpha, beta, lamb, m, lim, CVRMSE
