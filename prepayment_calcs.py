""" Functions for calculating prepayment features such as 

single monthly mortality (SMM) => SMM = 1 - (1 - CPR)^(1/12)

constant prepayment rate (CPR) => CPR = 1 - ((1 - SMM)^12)

PSA benchmark => PSA = month * 0.002 if month <= 30 else 6

Also contains function to produce CPR curves based on text descriptions, i.e. PSA benchmark = '0.2 ramp 6 for 30, 6'"""

import numpy as np
from bokeh.io import output_file


def SMM(CPR):
    return 1 - (1 - CPR) ** (1 / 12)


def CPR(SMM):
    return 1 - ((1 - SMM) ** 12)


def PSA(month):
    return month * 0.002 if month <= 30 else 6


def cpr_curve_creator(description='.2 ramp 6 for 30, 6'):
    """ Produces a 360 period CPR curve described by a text input string. Acceptable input is of the form
    '<start cpr> ramp <end cpr> for <duration>'.
    
    Periods are separated by commas ','
    
    Only <start cpr> is required. If no <duration> is provided, the final instruction will carry to 360 periods, i.e. 
    '6' as the input will produce a CPR curve of 6 through period 360; 
    
    To produce 100 PSA, the input string is '.2 ramp 6 for 30, 6'
    
    Returns PSA by default
    """

    periods = str(description).split(',')
    nperiods = 360
    end_period = False

    cpr_curve = []

    current_period = 1

    for period in periods:
        start_cpr = 0
        end_cpr = 0
        period_duration = 0
        cpr_increment = 0
        period_curve = None

        if period == periods[-1]:
            end_period = True

        period_duration = nperiods - current_period
        words = period.strip().split(' ')

        for i in range(len(words)):
            if i == 0:
                start_cpr = float(words[i]) / 100.
                end_cpr = float(words[i]) / 100.
            elif words[i] == 'ramp':
                end_cpr = float(words[i + 1]) / 100.
            elif words[i] == 'for':
                period_duration = float(words[i + 1])

        period_curve = np.linspace(start_cpr, end_cpr, period_duration)

        cpr_curve.extend(list(period_curve))
        current_period += period_duration - 1

    return cpr_curve


if __name__ == '__main__':
    output_file('psa.html')
    # hover = HoverTool(tooltips=[
    #     ('Mortgage Age', '$x'),
    #     ('Annual CPR', '$y')
    # ])
    # p = figure(title="PSA speeds", tools=[hover])
    # periods = range(1, 361)
    #
    # for mult in np.linspace(0.5, 1.5, num=3):
    #     x = []
    #     y = []
    #
    #     for period in periods:
    #         x.append(period)
    #         y.append(PSA(period) * mult)
    #     p.line(x, y, name='PSA-{0:.2f}'.format(mult))
    # show(p)
    a = cpr_curve_creator('.2 ramp 6 for 30, 6')
    print(len(a))
    # p = figure()
    # p.circle(range(1, 361),
    #          cpr_curve_creator('0 for 20, .2 ramp 6 for 30, 9 for 15, 9 ramp 8 for 35, 2 ramp 7 for 70, 6'))
    # show(p)