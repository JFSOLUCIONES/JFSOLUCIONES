"""Transparent Poisson market calculations for research only.
Different markets require separate chronological calibration.
"""
from __future__ import annotations
from math import exp, factorial, isfinite

def score_grid(home_rate:float,away_rate:float,cap:int=14):
    if any(type(x) not in (float,int) or not isfinite(x) or not 0.05 <= x <= 6.0 for x in (home_rate,away_rate)):
        raise ValueError("invalid_goal_rates")
    if type(cap) is not int or not 10<=cap<=20:raise ValueError("invalid_cap")
    hs=[exp(-home_rate)*home_rate**i/factorial(i) for i in range(cap+1)]
    aw=[exp(-away_rate)*away_rate**i/factorial(i) for i in range(cap+1)]
    total=sum(a*b for a in hs for b in aw)
    return [[a*b/total for b in aw] for a in hs]

def market_probabilities(home_rate,away_rate):
    g=score_grid(home_rate,away_rate)
    m={"local":0.0,"empate":0.0,"visitante":0.0,"ambos_si":0.0,"ambos_no":0.0,
       "mas_1_5":0.0,"menos_1_5":0.0,"mas_2_5":0.0,"menos_2_5":0.0,
       "doble_1x":0.0,"doble_x2":0.0}
    for h,row in enumerate(g):
        for a,p in enumerate(row):
            m["local" if h>a else "empate" if h==a else "visitante"]+=p
            m["ambos_si" if h>0 and a>0 else "ambos_no"]+=p
            m["mas_1_5" if h+a>=2 else "menos_1_5"]+=p
            m["mas_2_5" if h+a>=3 else "menos_2_5"]+=p
            if h>=a:m["doble_1x"]+=p
            if h<=a:m["doble_x2"]+=p
    return m

def fair_odds(p:float):
    if type(p) not in (int,float) or not isfinite(p) or p<=0 or p>1:raise ValueError("invalid_probability")
    return 1/p

def expected_value(p:float,decimal_odds:float):
    fair_odds(p)
    if type(decimal_odds) not in (int,float) or not isfinite(decimal_odds) or decimal_odds<=1:
        raise ValueError("invalid_decimal_odds")
    return p*decimal_odds-1
