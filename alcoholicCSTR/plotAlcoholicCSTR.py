from gams import *
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import AlcoholicCSTR as problem

model_name = "alcoholicCSTR"

def getPlotData(gdxfile,savefig=True,showfig=False):
    ws = GamsWorkspace(working_directory = os.getcwd())
    db = ws.add_database_from_gdx(gdxfile)
    Nz = ""
    for c in gdxFileName:
        if c.isdigit():
            Nz += c

    FId = db.get_variable("obj").first_record().level
    time_len = 240
    t = np.linspace(0,time_len,time_len,endpoint=True)
    S = [rec.level for rec in db['S']]
    S_ub = 80
    S_lb = 0.5
    t_Sact = [int(rec.keys[0]) for rec in db['S'] if abs(rec.level-S_ub ) <= 0.0001 or abs(rec.level-S_lb ) <= 0.0001]
    Sact = [S[act-1] for act in t_Sact]

    C = [rec.level for rec in db['C']]
    C_ub = 15
    C_lb = 0
    t_Cact = [int(rec.keys[0]) for rec in db['C'] if abs(rec.level-C_ub ) <= 0.0001 or abs(rec.level-C_lb ) <= 0.0001]
    Cact = [C[act-1] for act in t_Cact]

    P = [rec.level for rec in db['P']]
    # P_ub = 10
    P_lb = 40
    t_Pact = [int(rec.keys[0]) for rec in db['P'] if abs(rec.level-P_lb ) <= 0.0001]
    Pact = [P[act-1] for act in t_Pact]

    V = [rec.level for rec in db['V']]
    V_ub = 5
    V_lb = 1.5
    t_Vact = [int(rec.keys[0]) for rec in db['V'] if abs(rec.level-V_ub ) <= 0.0001 or abs(rec.level-V_lb ) <= 0.0001]
    Vact = [V[act-1] for act in t_Vact]
    
    # t_act = [int(rec.keys[0]) for rec in db['h'] if abs(rec.level-h_lb ) <= 0.0001 or abs(rec.level-h_ub ) <= 0.0001]
    # h_act = [h[act-1] for act in t_act]
    # print(h_act)
    Fin = [rec.level for rec in db['Fin']]
    Fin_ub = 0.5
    Fin_lb = 0.01
    Fout = [rec.level for rec in db['Fout']]
    Fout_ub = 0.5
    Fout_lb = 0.05

    Sa = [rec.level for rec in db['Sa']]
    Sa_n = 100
    T = [rec.level for rec in db['T']]
    T_n = 25

    fig_SV, [[ax_SV_C, ax_SV_P],[ax_SV_S, ax_SV_V]] = plt.subplots(nrows=2, ncols=2,figsize=(8, 6))
    ax_SV_List = [ax_SV_C,ax_SV_P,ax_SV_S,ax_SV_V] 

    line_c, = ax_SV_C.plot(t,C,color='green',linestyle='-',label=r'$C$')
    ax_SV_C.scatter(t_Sact,Sact,marker='o',s=120, facecolors='none', edgecolors='r')
    ax_SV_C.hlines(C_ub,xmin=t[0],xmax=t[-1],color='green',linestyle='--')
    ax_SV_C.hlines(C_lb,xmin=t[0],xmax=t[-1],color='green',linestyle='--')
    ax_SV_C.set_xlabel("time (hr)")
    ax_SV_C.set_ylabel("Conc (g/L)")
    
    line_p, = ax_SV_P.plot(t,P,color='red',linestyle='-',label=r'$P$')
    ax_SV_P.scatter(t_Pact,Pact,marker='o',s=120, facecolors='none', edgecolors='r')
    ax_SV_P.hlines(P_lb,xmin=t[0],xmax=t[-1],color='red',linestyle='--')
    ax_SV_P.set_xlabel("time (hr)")
    ax_SV_P.set_ylabel("Conc (g/L)")
    
    line_s, = ax_SV_S.plot(t,S,color='orange',linestyle='-',label=r'$S$')
    ax_SV_S.scatter(t_Sact,Sact,marker='o',s=120, facecolors='none', edgecolors='r')
    ax_SV_S.hlines(S_ub,xmin=t[0],xmax=t[-1],color='orange',linestyle='--')
    ax_SV_S.hlines(S_lb,xmin=t[0],xmax=t[-1],color='orange',linestyle='--')
    ax_SV_S.set_xlabel("time (hr)")
    ax_SV_S.set_ylabel("Conc (g/L)")

    line_v, = ax_SV_V.plot(t,V,color='royalblue',linestyle='-',label=r'$V$')
    ax_SV_V.scatter(t_Vact,Vact,marker='o',s=120, facecolors='none', edgecolors='r')
    ax_SV_V.hlines(V_ub,xmin=t[0],xmax=t[-1],color='royalblue',linestyle='--')
    ax_SV_V.hlines(V_lb,xmin=t[0],xmax=t[-1],color='royalblue',linestyle='--')
    ax_SV_V.set_xlabel("time (hr)")
    ax_SV_V.set_ylabel("Volume (L)")

    for as_sv in ax_SV_List:
        as_sv.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
        as_sv.legend()
    
    plt.tight_layout()

    fig_CV, [ax_CV_Fin, ax_CV_Fout] = plt.subplots(nrows=1, ncols=2,figsize=(8, 3))
    ax_CV_List = [ax_CV_Fin,ax_CV_Fout]

    line_fin, = ax_CV_Fin.plot(t,Fin,color='steelblue',linestyle='-',label=r'F$_{in}$')
    ax_CV_Fin.hlines(Fin_ub,xmin=t[0],xmax=t[-1],color='steelblue',linestyle='--')
    ax_CV_Fin.hlines(Fin_lb,xmin=t[0],xmax=t[-1],color='steelblue',linestyle='--')
    ax_CV_Fin.set_xlabel("time (hr)")
    ax_CV_Fin.set_ylabel("F$_{in}$ (L/hr)")
    ax_CV_Fin.set_ylim([0.0, 0.55])

    line_fout, = ax_CV_Fout.plot(t,Fout,color='dodgerblue',linestyle='-',label=r'F$_{out}$')
    ax_CV_Fout.hlines(Fout_ub,xmin=t[0],xmax=t[-1],color='dodgerblue',linestyle='--')
    ax_CV_Fout.hlines(Fout_lb,xmin=t[0],xmax=t[-1],color='dodgerblue',linestyle='--')
    ax_CV_Fout.set_xlabel("time (hr)")
    ax_CV_Fout.set_ylabel("F$_{out}$ (L/hr)")
    ax_CV_Fout.set_ylim([0.0, 0.55])

    for as_cv in ax_CV_List:
        as_cv.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
        as_cv.legend()

    plt.tight_layout()

    fig_UP, [ax_UP_Sa, ax_UP_T] = plt.subplots(nrows=1, ncols=2,figsize=(8, 3))
    ax_UP_List = [ax_UP_Sa, ax_UP_T]

    line_sa, = ax_UP_Sa.plot(t,Sa,color='gold',linestyle='-',label=r'$Sa$')
    line_sa_n = ax_UP_Sa.hlines(y=Sa_n,xmin=t[0],xmax=t[-1],color='gold',linestyle='--',label=r'$Sa_{nominal}$')
    ax_UP_Sa.set_ylim([Sa_n-50, Sa_n+50])
    ax_UP_Sa.set_xlabel("time (hr)")
    ax_UP_Sa.set_ylabel("Conc (g/L)")

    line_t, = ax_UP_T.plot(t,T,color='lightcoral',linestyle='-',label=r'$T$')
    line_t_n = ax_UP_T.hlines(y=T_n,xmin=t[0],xmax=t[-1],color='lightcoral',linestyle='--',label=r'$T_{nominal}$')
    ax_UP_T.set_ylim([T_n-10, T_n+10])
    ax_UP_T.set_xlabel("time (hr)")
    ax_UP_T.set_ylabel("Temp (°C)")

    for ax_up in ax_UP_List:
        ax_up.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
        ax_up.legend()
    plt.tight_layout()

    if savefig:
        dirPath = os.getcwd()+'\\'+model_name+'-Nz'+Nz+'-result'
        if os.path.isdir(dirPath) == False:
            os.mkdir(dirPath)
        figName = model_name+'-Nz'+Nz+'-result-SV.png'
        figPath = os.path.join(dirPath, figName)
        fig_SV.savefig(figPath,dpi=200)
        print("save fig:",figPath)
        figName = model_name+'-Nz'+Nz+'-result-CV.png'
        figPath = os.path.join(dirPath, figName)
        fig_CV.savefig(figPath,dpi=200)
        print("save fig:",figPath)
        figName = model_name+'-Nz'+Nz+'-result-UP.png'
        figPath = os.path.join(dirPath, figName)
        fig_UP.savefig(figPath,dpi=200)
        print("save fig:",figPath)
    
    if showfig:
        plt.show()

    return

if __name__ == "__main__":
    gdxFileName = "alcoholicCSTR-Nz2-result.gdx"

    getPlotData(gdxFileName,True)