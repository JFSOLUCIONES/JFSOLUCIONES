#!/usr/bin/env python3
"""JF SPORTS EDGE — chronological public-domain Poisson evaluation.
Input: OpenFootball CC0 JSON. Output: reproducible research metrics only.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from datetime import date
import json
from math import exp, factorial, log
from pathlib import Path

DATASET="openfootball/football.json (CC0-1.0)"
VERSION="JF_POISSON_CC0_WALKFORWARD_0.1"

def load_matches(root:Path,league:str,cutoff:date):
    if not root.is_dir():raise ValueError("data_dir_missing")
    games=[];seen=set()
    for file in sorted(root.glob(f"????-??/{league}.json")):
        season=file.parent.name
        try:entries=json.loads(file.read_text(encoding="utf-8"))["matches"]
        except (OSError,ValueError,KeyError,TypeError) as exc:raise ValueError(f"bad_dataset:{file}") from exc
        if not isinstance(entries,list):raise ValueError("matches_not_list")
        for match in entries:
            if not isinstance(match,dict):continue
            try:
                when=date.fromisoformat(match["date"])
                h,a=match["team1"],match["team2"]
                score=match["score"]
                if isinstance(score,dict):ft=score.get("ft")
                elif (isinstance(score,list) and score==[0,0]
                      and all(type(x) is int for x in score)
                      and date(2000+int(season[-2:]),7,1)<=cutoff):
                    ft=score
                else:continue
            except (ValueError,KeyError,TypeError):continue
            if when>=cutoff or when<date(1970,1,1):continue
            if not (isinstance(h,str) and isinstance(a,str) and h!=a
                    and isinstance(ft,list) and len(ft)==2
                    and all(type(v) is int and 0<=v<=20 for v in ft)):continue
            key=(when,h,a)
            if key in seen:raise ValueError(f"duplicate_fixture:{key}")
            seen.add(key)
            games.append({"date":when,"season":season,"home":h,"away":a,"hg":ft[0],"ag":ft[1]})
    games.sort(key=lambda x:(x["date"],x["home"],x["away"]))
    if not games:raise ValueError("no_completed_fixtures")
    return games

def outcomes(g):
    return 0 if g["hg"]>g["ag"] else 1 if g["hg"]==g["ag"] else 2

def poisson_probs(lh,la,limit=11):
    ph=[exp(-lh)*lh**k/factorial(k) for k in range(limit+1)]
    pa=[exp(-la)*la**k/factorial(k) for k in range(limit+1)]
    result=[0.0,0.0,0.0]
    for i,x in enumerate(ph):
        for j,y in enumerate(pa):result[0 if i>j else 1 if i==j else 2]+=x*y
    total=sum(result)
    return [z/total for z in result]

def mean_side(history,*,team,location,target,expected,as_of,shrink=8.0):
    v=w=0.0
    for g in history:
        if g[location]!=team:continue
        elapsed=(as_of-g["date"]).days
        if not 0<elapsed<=900:continue
        weight=exp(-elapsed/365.0)
        v+=weight*g[target];w+=weight
    return (v+shrink*expected)/(w+shrink)

def forecast(history,target):
    if len(history)<80:raise ValueError("history_too_short")
    hmean=(sum(g["hg"] for g in history)+12*1.45)/(len(history)+12)
    amean=(sum(g["ag"] for g in history)+12*1.15)/(len(history)+12)
    now=target["date"]
    ha=mean_side(history,team=target["home"],location="home",target="hg",expected=hmean,as_of=now)
    hd=mean_side(history,team=target["home"],location="home",target="ag",expected=amean,as_of=now)
    aa=mean_side(history,team=target["away"],location="away",target="ag",expected=amean,as_of=now)
    ad=mean_side(history,team=target["away"],location="away",target="hg",expected=hmean,as_of=now)
    lh=min(4.2,max(.2,ha*ad/hmean))
    la=min(4.2,max(.2,aa*hd/amean))
    counts=[1,1,1]
    for g in history:counts[outcomes(g)]+=1
    base=[c/sum(counts) for c in counts]
    return poisson_probs(lh,la),base

def calculate_walkforward(games):
    history=[];rows=[];i=0
    while i<len(games):
        today=games[i]["date"];batch=[]
        while i<len(games) and games[i]["date"]==today:
            batch.append(games[i]);i+=1
        if len(history)>=80:
            for g in batch:
                probabilities,base=forecast(history,g)
                rows.append({"date":g["date"].isoformat(),"season":g["season"],
                             "outcome":outcomes(g),"raw":probabilities,"baseline":base})
        history.extend(batch)
    return rows

def temp_scale(p,t):
    nums=[max(1e-9,x)**(1.0/t) for x in p];z=sum(nums)
    return [x/z for x in nums]

def metrics(rows,key,temp=1.0):
    if not rows:raise ValueError("empty_sample")
    probs=[temp_scale(r[key],temp) if key=="raw" else r[key] for r in rows]
    ll=-sum(log(max(1e-12,p[r["outcome"]])) for p,r in zip(probs,rows))/len(rows)
    brier=sum(sum((p[i]-(i==r["outcome"]))**2 for i in range(3)) for p,r in zip(probs,rows))/len(rows)
    acc=sum(max(range(3),key=lambda i:p[i])==r["outcome"] for p,r in zip(probs,rows))/len(rows)
    bins=defaultdict(list)
    for p,r in zip(probs,rows):
        conf=max(p);idx=min(9,int(conf*10))
        ok=int(max(range(3),key=lambda i:p[i])==r["outcome"])
        bins[idx].append((conf,ok))
    ece=sum(abs(sum(x for x,_ in vals)/len(vals)-sum(y for _,y in vals)/len(vals))*len(vals)/len(rows) for vals in bins.values())
    return {"n":len(rows),"log_loss":round(ll,5),"brier":round(brier,5),
            "accuracy":round(acc,5),"ece_top_class":round(ece,5)}

def report(games,calibration_season,test_season):
    if calibration_season>=test_season:raise ValueError("seasons_order_invalid")
    r=calculate_walkforward(games)
    cal=[x for x in r if x["season"]==calibration_season]
    test=[x for x in r if x["season"]==test_season]
    if len(cal)<120 or len(test)<120:raise ValueError(f"sample_short:cal={len(cal)}:test={len(test)}")
    temps=[.65+i*.05 for i in range(23)]
    t=min(temps,key=lambda x:metrics(cal,"raw",x)["log_loss"])
    m=metrics(test,"raw",t);b=metrics(test,"baseline")
    return {
      "version":VERSION,"source":DATASET,"league":"Bundesliga",
      "seasons_present":sorted({g["season"] for g in games}),
      "completed_matches":len(games),
      "calibration_season":calibration_season,"calibration_matches":len(cal),
      "holdout_season":test_season,"holdout_matches":len(test),
      "temperature_fitted_on_calibration_only":round(t,2),
      "holdout_model":m,"holdout_baseline":b,
      "outperformed_baseline_on_both_metrics":m["brier"]<b["brier"] and m["log_loss"]<b["log_loss"],
      "status":"RESEARCH_ONLY_NOT_PRODUCTION_CALIBRATED",
      "notes":["Sin cuotas ni lesionados.","Predicciones cronológicas con holdout independiente.",
               "Exactitud histórica no prueba ganancias futuras."]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data-dir",required=True,type=Path)
    p.add_argument("--league",default="de.1")
    p.add_argument("--before",default="2026-11-21")
    p.add_argument("--cal-season",default="2024-25")
    p.add_argument("--test-season",default="2025-26")
    p.add_argument("--output",type=Path,default=Path("report_cc0.json"))
    args=p.parse_args()
    games=load_matches(args.data_dir,args.league,date.fromisoformat(args.before))
    x=report(games,args.cal_season,args.test_season)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps({k:v for k,v in x.items() if k in (
      "version","completed_matches","calibration_matches","holdout_matches",
      "holdout_model","holdout_baseline","status")},indent=2))

if __name__=="__main__":main()
