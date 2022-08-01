from copy import copy
from gams import *
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import copy
#import mytimer as timer

class AlcoholicCSTR():
    def __init__(self,):
        self.ws = GamsWorkspace(working_directory = os.getcwd())
        self.model_name = "alcoholicCSTR"
        self.is_show_solve_result = True

        self.Nz = 1
        self.time_len = 240
        self.uncertainParaList = ["Sa","T"]
        self.startDirect = {"Sa": 1, "T": 1}
        self.GAMSModelInstance = None
        self.cp = None
        self.job = None
        self.cp_file = None

    def set_Nz(self,nz):
        self.Nz = nz

    def setStartDirect(self,d):
        self.startDirect = d
        for p in self.uncertainParaList:
            if p not in d:
                raise AttributeError("Uncertain Parameter ", p," not in startdirect dict.")
            p_direct = self.startDirect[p]
            if not (p_direct == 1 or p_direct == -1):
                raise ValueError("Uncertain Parameter ", p, " startdirect is ", p_direct, ", it should be +1 or -1.")
        print("current Uncertain Parameter start direction",self.startDirect)

    def set_uncertain_para(self,uncertain_para):
        if isinstance(uncertain_para,str):
            self.uncertainParaList = [uncertain_para]
        elif isinstance(uncertain_para,list):
            self.uncertainParaList = uncertain_para
        else:
            raise TypeError("uncertain paramaters setting must be str or list type.")

    def set_GAMSfile(self,file=None):
        if file is None:
            file_name = self.model_name+"_modelinstance"
            for p in self.uncertainParaList:
                file_name += '_'+p
            file_name += '_nz'+str(self.Nz)+'.gms'
        else:
            file_name = file
        print(file_name)
        if os.path.isfile('./'+file_name):
            self.jobGAMSfile = file_name
        elif os.path.isfile('./SingleTank/'+file_name):
            self.jobGAMSfile = file_name
        else:
            raise FileNotFoundError("GAMSModelInstance file :"+file_name+"not found")

    def set_GAMSModelInstance(self):
        self.cp = self.ws.add_checkpoint()
        self.job = self.ws.add_job_from_file(self.jobGAMSfile)
        self.job.run(checkpoint=self.cp)
        mi = self.cp.add_modelinstance()

        opt = self.ws.add_options()
        opt.all_model_types = "conopt3"
        opt.solprint = 1
        print("fdopt:\t\t",opt.fdopt)
        print("fddelta:\t",opt.fddelta)

        modifiers = []

        for p in self.uncertainParaList:
            vertex = mi.sync_db.add_parameter(p+'_vertex', 1, p+"_d direction vertex")
            modifiers.append(GamsModifier(vertex))

        mi.instantiate(self.model_name+" using nlp maximizing obj",modifiers,opt)
        self.GAMSModelInstance = mi

    def update_vertex(self,p_name,shift_list):
        parameter = self.GAMSModelInstance.sync_db.get_parameter(p_name+'_vertex')
        parameter.clear()

        v_len_V = len(shift_list)
        d_cur_V = self.startDirect[p_name]
        shift_t = 0
        for rec in self.job.out_db.get_parameter(p_name+'_vertex'):
            if shift_t < v_len_V:
                if shift_list[shift_t] == 't':
                    shift_t = 10000
                elif(int(rec.keys[0])>=shift_list[shift_t]):
                    d_cur_V = -d_cur_V
                    shift_t += 1
            parameter.add_record(rec.keys).value = d_cur_V

    def solve(self,vertex):
        mi = self.GAMSModelInstance

        for p in self.uncertainParaList:
            self.update_vertex(p,vertex[p])
        mi.solve()
        if self.is_show_solve_result:
            print("Scenario vertex=" + str(vertex) + ":")
            print ("  Modelstatus: " + str(mi.model_status))
            print ("  Solvestatus: " + str(mi.solver_status))
            print ("  Obj: " + str(mi.sync_db.get_variable("obj")[()].level))
        result = mi.sync_db.get_variable("obj")[()].level
        return result

    def update_vertex_by_list(self,p_name,verList):
        parameter = self.GAMSModelInstance.sync_db.get_parameter(p_name+'_vertex')
        parameter.clear()

        for rec in self.job.out_db.get_parameter(p_name+'_vertex'):            
            if p_name not in self.act_Table :
                raise IndexError("there is definition of uncertain parameter",p_name," in act Table for transform") 
            index = int("".join(rec.keys))-1
            ver_d = self.act_Table[p_name][verList[index]]
            #print(rec.keys, index, ver_d)
            parameter.add_record(rec.keys).value = ver_d
    def solve_vertexList(self, vertexlist):
        mi = self.GAMSModelInstance

        for p in self.uncertainParaList:
            self.update_vertex_by_list(p,vertexlist[p])
        mi.solve()
        #print("Scenario vertex=" + str(vertexlist) + ":")
        #print ("  Modelstatus: " + str(mi.model_status))
        #print ("  Solvestatus: " + str(mi.solver_status))
        #print ("  Obj: " + str(mi.sync_db.get_variable("obj")[()].level))
        result = mi.sync_db.get_variable("obj")[()].level
        return result

    def solve_outDB(self,vertex,savefig=False):
        mi = self.GAMSModelInstance

        for p in self.uncertainParaList:
            self.update_vertex(p,vertex[p])
        
        mi.solve()
        print("Scenario vertex=" + str(vertex) + ":")
        print("  Modelstatus: " + str(mi.model_status))
        print("  Solvestatus: " + str(mi.solver_status))
        print("  Obj: " + str(mi.sync_db.get_variable("obj")[()].level))
        export_gdx_name = os.getcwd()+'\\'+self.model_name+'-Nz'+str(self.Nz)+'-result.gdx'
        mi.sync_db.export(export_gdx_name)

if __name__ == "__main__":
    test_Nz = 2
    Uncertain_parameter_name = ["Sa","T"]
    startD =  {"Sa": -1, "T": -1}

    solver = AlcoholicCSTR()
    solver.set_Nz(test_Nz)
    solver.set_uncertain_para(Uncertain_parameter_name)
    solver.setStartDirect(startD)
    solver.set_GAMSfile()
    solver.set_GAMSModelInstance()

    vertex = {'Sa': [236,'t'],'T': ['t']}

    """min_FId = 1000
    min_vertex = None
    sa = 235
    t = 5
    for i in range(sa-t,sa+t+1):
        f = solver.solve({'Sa': [i,'t'],'T': ['t']})
        if f < min_FId:
            min_FId = f
            min_vertex = copy.deepcopy({'Sa': [i,'t'],'T': ['t']})
    
    print(min_FId,min_vertex)"""
    #f = solver.solve(min_vertex)
    solver.solve_outDB(vertex)

    exit()