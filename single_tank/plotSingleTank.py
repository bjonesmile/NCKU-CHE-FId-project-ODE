from gams import *
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import SingleTank as problem

model_name = "singletank"

def getPlotData(gdxfile,savefig=True):
    ws = GamsWorkspace(working_directory = os.getcwd())
    db = ws.add_database_from_gdx(gdxfile)
    Nz = ""
    for c in gdxFileName:
        if c.isdigit():
            Nz += c

    FId = db.get_variable("obj").first_record().level
    time_len = 800
    t = np.linspace(0,time_len,time_len,endpoint=True)
    h_ub = 10
    h_lb = 1
    h = [rec.level for rec in db['h']]
    t_act = [int(rec.keys[0]) for rec in db['h'] if abs(rec.level-h_lb ) <= 0.0001 or abs(rec.level-h_ub ) <= 0.0001]
    h_act = [h[act-1] for act in t_act]
    print(h_act)
    qout = [rec.level for rec in db['qout']]
    theta = [rec.level for rec in db['theta']]

    fig, ax_SV = plt.subplots()
    ax_CV = ax_SV.twinx()

    line_h, = ax_SV.plot(t,h,color='black',linestyle='-',label=r'$h$')
    ax_SV.scatter(t_act,h_act,marker='o',s=120, facecolors='none', edgecolors='r')
    line_h_ub = ax_SV.hlines(y=10,xmin=t[0],xmax=t[-1],color='black',linestyle='-.',label=r'$\th _{ub}$')
    line_h_lb = ax_SV.hlines(y=1,xmin=t[0],xmax=t[-1],color='black',linestyle='-.',label=r'$\th _{lb}$')

    line_theta, = ax_CV.plot(t,theta,color='deepskyblue',linestyle='-',label=r'$\theta _{deviated}$')
    line_theta_n = ax_CV.hlines(y=0.5,xmin=t[0],xmax=t[-1],color='deepskyblue',linestyle='--',label=r'$\theta _{nominal}$')
    line_qout, = ax_CV.plot(t,qout,color='darkorange',label=r'$q_{out}$')
    ax_CV.set_ylim([0.0, 1.0])

    lns = [line_h, line_theta, line_theta_n, line_qout]
    labs = [l.get_label() for l in lns]
    ax_SV.legend(lns,labs,loc="upper left")

    ax_SV.set_xlabel("time (min)")
    ax_SV.set_ylabel("water level (m)")
    ax_CV.set_ylabel("flow rate (m$^3$/min)")
    
    #ax_SV.legend(handles=[line_h], loc="upper left")
    #ax_CV.legend(handles=[line_qout,line_theta,line_theta_n], loc="lower right")

    ax_SV.grid(color='gray', linestyle='dotted', linewidth=1)
    #plt.legend()
    if savefig:
        dirPath = os.getcwd()+'\\'+model_name+'-Nz'+Nz+'-result'
        if os.path.isdir(dirPath) == False:
            os.mkdir(dirPath)
        figName = model_name+'-Nz'+Nz+'-result-SV-CV-UP.png'
        figPath = os.path.join(dirPath, figName)
        plt.savefig(figPath,dpi=200)
        print("save fig:",figPath)
    plt.show()
    return

if __name__ == "__main__":
    gdxFileName = "singletank-Nz1-result.gdx"

    getPlotData(gdxFileName)