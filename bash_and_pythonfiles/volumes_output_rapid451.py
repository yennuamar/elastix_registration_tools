# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 12:02:54 2016

@author: sorenc
"""

import re
import os.path
import glob
import scutils.io.rapidbinread as rapidbinread
import scutils.imquant.framecorr as framecorr
import scutils.common as common



def r451logread(location):
    
    mydict={}
    #lets dig out some info.
    #did it finalize?
    if not os.path.isfile(location):
          mydict["returncode"]=3
          return mydict
          
    fid=open(location,'r')      
    logtxt=fid.read()
    fid.close()    
    
     
    op=re.search("Magnetic field strength: (.*T)",logtxt)
    if op==None:
         mydict["FieldStrength"]="NA"
    else:
         mydict["FieldStrength"]=op.group(1)     
    
    
    op=re.search("Finished RAPID post-processing",logtxt)  
    mydict["errormessage"]= " "
    
    if op==None:   #find out what happened then - should be limited range of outcomes here
        op=re.search("no valid AIF/VOF points|error in profile determination",logtxt)  
        if not op==None:        
            mydict["returncode"]=1
            mydict["errormessage"]="AIF error"
        else: #unknown
            mydict["returncode"]=2
            mydict["errormessage"]="Unknown error"    
    else:
        mydict["returncode"]=0    

    return mydict
    

    
def get451_corr(location):    
     binfile=glob.glob(location+"/*_motionCorrectedImportedData.bin")
     if not len(binfile)==1:
          return []   

     rawmat=rapidbinread.rapidbinread(binfile[0])
 

     return framecorr.framecorr(rawmat,2)

         
    
def get451_volumes(location):
    mydict={}
    mydict["returncode"]=0
    if not os.path.isfile(location):
         mydict["returncode"]=1
         return mydict    
          
     #work out if CT or MR     
    fid=open(location,'r')
    txt=fid.read()
    fid.close()
    op=re.search("DWI",txt)  
     
    if op==None:   #nomenclature is 4.5.1 specific. RAPID451OP must abstract
        mydict["modality"]="CT"
        recbf=re.search("CBF \(\<([0-9]+)%\) volume: ([<]?[0-9]+\.[0-9]) ml",txt)
        recbv=re.search("CBV \(\<([0-9]+)%\) volume: ([<]?[0-9]+\.[0-9]) ml",txt)
        retmax4=re.search("Perfusion \(Tmax>4.0s\) volume: ([<]?[0-9]+\.[0-9]) ml",txt)
        retmax6=re.search("Perfusion \(Tmax>6.0s\) volume: ([<]?[0-9]+\.[0-9]) ml",txt)
        retmax8=re.search("Perfusion \(Tmax>8.0s\) volume: ([<]?[0-9]+\.[0-9]) ml",txt)
        retmax10=re.search("Perfusion \(Tmax>10.0s\) volume: ([<]?[0-9]+\.[0-9]) ml",txt)
        
        mydict["CBFvol"]=float(re.sub('<.*','0',recbf.group(2)))
        mydict["CBFthold"]=float(recbf.group(1))
        mydict["CBVvol"]=float(re.sub('<.*','0',recbv.group(2)))
        mydict["CBVthold"]=float(recbv.group(1))
        
        #entries with < will be 0        
        
        mydict["tmaxvolumes"]=[ float(re.sub('<.*','0',retmax4.group(1))),
                                float(re.sub('<.*','0',retmax6.group(1))),
                                float(re.sub('<.*','0',retmax8.group(1))),
                                float(re.sub('<.*','0',retmax10.group(1))) ]
        mydict["tmaxthresholds"]=[4,6,8,10]
    else:
        mydict["modality"]="MR"
        readc=re.search("DWI \(ADC<([0-9]+)\) volume: ([<]?[0-9]+\.[0-9]) ml",txt)
        mydict["ADCthold"]=float(readc.group(1))
        mydict["ADCvolume"]=float(re.sub('<.*','0',readc.group(2)))
        #recbv=re.search("CBV \(\<([0-9]+)%\) volume: ([<]?[0-9]+\.[0-9]) ml",txt)
        retmax4=re.search("Perfusion \(Tmax>4.0s\) volume: ([<]?[0-9]+\.[0-9]) ml",txt)
        retmax6=re.search("Perfusion \(Tmax>6.0s\) volume: ([<]?[0-9]+\.[0-9]) ml",txt)
        retmax8=re.search("Perfusion \(Tmax>8.0s\) volume: ([<]?[0-9]+\.[0-9]) ml",txt)
        retmax10=re.search("Perfusion \(Tmax>10.0s\) volume: ([<]?[0-9]+\.[0-9]) ml",txt)
        mydict["tmaxvolumes"]=[ float(re.sub('<.*','0',retmax4.group(1))),
                                float(re.sub('<.*','0',retmax6.group(1))),
                                float(re.sub('<.*','0',retmax8.group(1))),
                                float(re.sub('<.*','0',retmax10.group(1))) ]
        mydict["tmaxthresholds"]=[4,6,8,10]
    return mydict
    

class RAPID451OP:
    def __init__(self,foldername,calccorr=False):  
#        logfile=foldername+"/log.log"
        logfile=foldername+"/rapid_processing.log.txt"
        self.modality="NA"
        self.fieldstrength="NA"
        log451=r451logread(logfile)     #errcode: exit 0 = ok, 1 = aif, 2 =  unspec, 3= no file        
      
        self.allpng=[]
        self.summaryimg=-1
        self.aifcurve=-1
        self.aifloc=-1
        if log451["returncode"]==0:
            fname=glob.glob(foldername+"/*_protocol.txt")
            assert(len(fname)==1)            
            vols451=get451_volumes(fname[0])
            
            #rest us standardized to match 4.6
            # {"tmaxthresholds":thresholds,"tmaxvolumes":tmaxvolumes,"coremodal":coremodal,
            #"corevolumes":corevols,"corethresholds":coretholds} 
            if vols451["modality"]=="CT":
                self.modality="CT"
                self.fieldstrength=log451["FieldStrength"]
                self.voldict={"tmaxthresholds":vols451["tmaxthresholds"],"tmaxvolumes":vols451["tmaxvolumes"],"coremodal":"rCBF",
            "corevolumes":[vols451["CBFvol"]],"corethresholds":[ vols451["CBFthold"] ]}
            else:
                self.modality="MR"
                self.fieldstrength=log451["FieldStrength"]
                self.voldict={"tmaxthresholds":vols451["tmaxthresholds"],"tmaxvolumes":vols451["tmaxvolumes"],"coremodal":"ADC",
            "corevolumes":[vols451["ADCvolume"]],"corethresholds":[ vols451["ADCthold"] ]}
            
            
            self.foldername=foldername
            self.statuscode=False
            self.errormessage="no error"
            self.allpng=glob.glob(foldername+"/*.jpeg")
            self.summaryimg=common.get_indx(self.allpng,".*_finalMismatchSummary.jpeg")
            self.aifcurve=common.get_indx(self.allpng,".*_colorAIF_plot.jpeg")
            self.aifloc=common.get_indx(self.allpng,".*_aifvofloc_tiles.jpeg")
           
            #if correlations should be calculated then let's do this (function will test for data presence, cannot necesarrily infer from the error code if it will be there or not)            
            
        else:
            self.statuscode=log451["returncode"]
            self.errormessage=log451["errormessage"]
            self.voldict={"tmaxthresholds":[-1,-1,-1,-1],"tmaxvolumes":[-1,-1,-1,-1],"coremodal":"NA",
            "corevolumes":[-1],"corethresholds":[-1]}

        if calccorr:
            bake=False
            import cPickle as pickle
            if bake:
                corr=get451_corr(foldername)
                fp=open(foldername+"/corr.p", 'wb')
                pickle.dump(corr, fp)  
                fp.close() 
            else:
                fp=open(foldername+"/corr.p") 
                corr = pickle.load(fp)
                fp.close()
            
            self.corr=corr
        else:
            self.corr=[]
            

    def modality(self):
        return self.modality
        
    def __str__(self):
        return self.errormessage        
        
    def status(self):
        return self.statuscode
    
    def tmaxthreshvols(self):
        return {"thresholds":self.voldict["tmaxthresholds"],"volumes":self.voldict["tmaxvolumes"]}
        
    def corethreshvols(self):
        return {"corethresholds":self.voldict["corethresholds"],"volumes":self.voldict["corevolumes"]}
    
    def thesholds(self):
        return 
        
        

files=[]
for dir,_,_ in os.walk('/Volumes/RAPID_PROCESSING/proc_rapid45_44cases'):
    files.extend(glob.glob(os.path.join(dir,'rapid_processing.log.txt')))         
mydict={}    
for i in range(len(files)):
    if re.search('Results_PWI_DWI',files[i]) and not re.search('_R46',files[i]) :
        r451=RAPID451OP(os.path.dirname(files[i])) 
        finalvols=r451.voldict
        print('Results_PWI_DWI')
        print(finalvols)
        print(r451.errormessage)
        patientid=files[i].split("/")[-4]
        blorfu=files[i].split("/")[-3]
        
        mydict={'Patient_ID':patientid,'BLorFU':blorfu,'corevolume':float(finalvols['corevolumes'][0]),'tmax6': float(finalvols['tmaxvolumes'][1]),'tmax10': float(finalvols['tmaxvolumes'][3]),'error': r451.errormessage  }
        with open('/Users/amar/Desktop/data_arrange/volumes/' + 'ALL2' + '.txt', 'a') as f:
            print(mydict.values(), file=f)
    if re.search('Results_CTP1',files[i]) and not re.search('_R46',files[i]) :
        r451=RAPID451OP(os.path.dirname(files[i]))
        finalvols=r451.voldict
        print('Results_CTP1')
        print(finalvols)
        print(r451.errormessage)
        patientid=files[i].split("/")[-4]
        blorfu=files[i].split("/")[-3]
        mydict={'Patient_ID':patientid,'BLorFU':blorfu,'corevolume':float(finalvols['corevolumes'][0]),'tmax6': float(finalvols['tmaxvolumes'][1]),'tmax10': float(finalvols['tmaxvolumes'][3]),'error': r451.errormessage   }
        with open('/Users/amar/Desktop/data_arrange/volumes/' + 'ALL2' + '.txt', 'a') as f:
            print(mydict.values(), file=f)
    if re.search('Results_CTP2',files[i]) and not re.search('_R46',files[i]):
        r451=RAPID451OP(os.path.dirname(files[i]))
        finalvols=r451.voldict 
        print('Results_CTP2')
        print(finalvols)
        print(r451.errormessage)
        patientid=files[i].split("/")[-4]
        blorfu=files[i].split("/")[-3]
        mydict={'Patient_ID':patientid,'BLorFU':blorfu,'corevolume':float(finalvols['corevolumes'][0]),'tmax6': float(finalvols['tmaxvolumes'][1]),'tmax10': float(finalvols['tmaxvolumes'][3]),'error': r451.errormessage   }
        with open('/Users/amar/Desktop/data_arrange/volumes/' + 'ALL2' + '.txt', 'a') as f:
            print(mydict.values(), file=f)
    if re.search('Results_only_DWI',files[i]) and not re.search('_R46',files[i] ):
        r451=RAPID451OP(os.path.dirname(files[i]))
        finalvols=r451.voldict
        print('Results_only_DWI')
        print(finalvols)
        print(r451.errormessage)
        patientid=files[i].split("/")[-4]
        blorfu=files[i].split("/")[-3]
        
        mydict={'Patient_ID':patientid,'BLorFU':blorfu,'corevolume':float(finalvols['corevolumes'][0]),'tmax6': float(finalvols['tmaxvolumes'][1]),'tmax10': float(finalvols['tmaxvolumes'][3]),'error': r451.errormessage   }
        with open('/Users/amar/Desktop/data_arrange/volumes/' + 'ALL2' + '.txt', 'a') as f:
            print(mydict.values(), file=f)



    
#test stuff

#if False:
#    lst=open("/home/sorenc/RAPID46_TEST_OUTPUT/cases20v1.lst","r").read().rstrip()
#    lst=lst.split("\n")
#    
#    for iline in lst:
#        
#        loc="/home/sorenc/RAPID451_TEST_OUTPUT/" + iline +"/log.log"
#        print loc
#        #op=r451logread(loc)
#        #print op["returncode"]        
#        r451=RAPID451OP("/home/sorenc/RAPID451_TEST_OUTPUT/" + iline)
#    
#        if r451.status():
#            print r451.errormessage
        
       
            
