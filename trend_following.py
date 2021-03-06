"""
trend_following.py
===========================
    author: erichamer
"""
import numpy as np
import sys

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    ''' This system uses trend following techniques to allocate capital into the desired equities'''

    nMarkets = CLOSE.shape[1]

    periodLonger = 200 #%[200:25:400]#
    periodShorter = 40 #%[40:10:100]#

    # Calculate Simple Moving Average (SMA)
    smaLongerPeriod = np.nansum(CLOSE[-periodLonger:, :], axis=0)/periodLonger
    smaShorterPeriod = np.nansum(CLOSE[-periodShorter:, :], axis=0)/periodShorter

    longEquity = smaShorterPeriod > smaLongerPeriod
    shortEquity = ~longEquity

    pos = np.zeros(nMarkets)
    pos[longEquity] = 1
    pos[shortEquity] = -1

    weights = pos/np.nansum(abs(pos))
    return weights, settings


def mySettings():
    ''' Define your trading system settings here '''

    settings = {}

    # Futures Contracts
    settings['markets'] = ['CASH','F_AD','F_AE','F_AH','F_AX','F_BC','F_BG','F_BO','F_BP','F_C','F_CA','F_CC','F_CD',
                           'F_CF','F_CL','F_CT','F_DL','F_DM','F_DT','F_DX','F_DZ','F_EB','F_EC','F_ED','F_ES','F_F',
                           'F_FB','F_FC','F_FL','F_FM','F_FP','F_FV','F_FY','F_GC','F_GD','F_GS','F_GX','F_HG','F_HO',
                           'F_HP','F_JY','F_KC','F_LB','F_LC','F_LN','F_LQ','F_LR','F_LU','F_LX','F_MD','F_MP','F_ND',
                           'F_NG','F_NQ','F_NR','F_NY','F_O','F_OJ','F_PA','F_PL','F_PQ','F_RB','F_RF','F_RP','F_RR',
                           'F_RU','F_RY','F_S','F_SB','F_SF','F_SH','F_SI','F_SM','F_SS','F_SX','F_TR','F_TU','F_TY',
                           'F_UB','F_US','F_UZ','F_VF','F_VT','F_VW','F_VX','F_W','F_XX','F_YM','F_ZQ']

    settings['lookback'] = 210
    settings['budget'] = 10**6
    settings['slippage'] = 0.05

    return settings

def CalcLongExposure(mktExposure, lookBack):
    import numpy as np

    Long = np.transpose(mktExposure)
    Long[Long < 0] = 0

    Long = Long[:-1]  # Market Exposure lagged by one day
    Long = Long.sum(axis=0)
    return Long


def CalcShortExposure(mktExposure, lookBack):
    import numpy as np

    Short = -np.transpose(mktExposure)
    Short[Short < 0] = 0

    Short = Short[:-1]  # Market Exposure lagged by one day
    Short = Short.sum(axis=0)
    return Short

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    from quantiacsToolbox import runts, optimize

    #optimize()
    res = runts(reloadData=False)
    l1 = CalcLongExposure(res['marketExposure'], 0)
    s1 = CalcShortExposure(res['marketExposure'], 0)



    sys.exit(0)