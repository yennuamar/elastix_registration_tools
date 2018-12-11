# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 14:54:44 2016

@author: sorenc
"""
import RPDjsonR47
import os.path
import glob
import json
#import scutils.io.mhdread as mhdread
import scutils.imquant.framecorr as framecorr
import scutils.common as common
import re

#add query of datetime
class RAPID46OP:
    def __init__(self,foldername,calccorr=False):  
        
        #corr from actual image files
        self.corr=[]    
        self.allpng=[]
        self.summaryimg=-1
        self.aifcurve=-1
        self.aifloc=-1
        self.zcoverage_slab1=''
        self.zcoverage_slab2=''
        self.SeriesDateTime_slab1=''
        self.SeriesDateTime_slab2=''
        self.numberofslabs=-1
        self.type='Not set'
        self.HypoperfusionIndex_slab1=''
        self.CBVIndex_slab1=''
        self.HypoperfusionIndex_slab2=''
        self.CBVIndex_slab2=''
        
        if calccorr:
            tps=glob.glob(foldername + "/post_volume_slab0_band0_timepoint*")
            if len(tps)>0:
                t=mhdread.readmhd(foldername + "/post_volume_slab0_band0_timepoint*")    #ISSUE: this creates an instance that holds the mat. this instance is not deleted until this RAPID46OP instance is deleted
                
                self.corr=framecorr.framecorr(t.getNPmat(),2)
                del t
            else:
                self.corr=[]
        
        #corr from json        
        opjson=foldername+"/post_afterMotionCorrection_slab0.json"   
        if os.path.isfile(opjson):
            fid=open(opjson,"r")
            dat=json.loads(fid.read())
            fid.close()
            self.json_corr_pre=dat["TimepointCorrelationBeforeMoCo"]
            self.json_corr_post=dat["TimepointCorrelationAfterMoCo"]
        else:        
            self.json_corr_pre=[]
            self.json_corr_post=[]
            
            
        jsonfile=foldername+"/output.json"
        if os.path.isfile(jsonfile):    #for zcoverage
            fid=open(jsonfile)
            self.voldict_outputjson=json.loads(fid.read())
            fid.close()
       
            try: 
                if self.voldict_outputjson['NumberOfPerfusionSlabs']==1:
                    numberofperfusionslabs=1 
                elif self.voldict_outputjson['NumberOfPerfusionSlabs']==2:
                    numberofperfusionslabs=2 
            except:
                numberofperfusionslabs=0 #onlydwicase
            try:    
                if numberofperfusionslabs == 0 :
                    self.numberofslices_slab1=self.voldict_outputjson['DICOMHeaderInfo']['DiffusionSeries'][0]['NumberOfSlices']
                    self.slicethickness_slab1=self.voldict_outputjson['DICOMHeaderInfo']['DiffusionSeries'][0]['SliceThickness']
                    self.zcoverage_slab1=self.numberofslices_slab1*float(self.slicethickness_slab1)
            except:
                print("diffusion rapid processing error")
                
                
            if numberofperfusionslabs == 1 : 
                try: 
                    self.numberofslices_slab1=self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][0]['NumberOfSlices']
                    self.slicethickness_slab1=self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][0]['SliceThickness']  #cannot be read for tosh data
                    self.zcoverage_slab1=self.numberofslices_slab1*float(self.slicethickness_slab1)
                except:
                    try:
                        if self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][0]['ManufacturerModelName']=='Aquilion ONE' and self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][0]['NumberOfSlices']==16:
                            self.zcoverage_slab1=160   #this is a hardcoded case because this info is not stored in header    
                    except:
                        print('numberofslices and/or slicethickness not available')


            if numberofperfusionslabs == 2:
                self.numberofslices_slab1=self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][0]['NumberOfSlices']
                self.slicethickness_slab1=self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][0]['SliceThickness']
                self.numberofslices_slab2=self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][1]['NumberOfSlices']
                self.slicethickness_slab2=self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][1]['SliceThickness']
                self.zcoverage_slab1=self.numberofslices_slab1*float(self.slicethickness_slab1)
                self.zcoverage_slab2=self.numberofslices_slab2*float(self.slicethickness_slab2)
                self.zcoverage=self.zcoverage_slab1+self.zcoverage_slab2
                 
            try:   #why are we using try catch here?
                if numberofperfusionslabs == 1:            
                    Seriesdate_slab1=self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][0]['SeriesDate']
                    Seriestime_slab1=self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][0]['SeriesTime']
                    self.SeriesDateTime_slab1=Seriesdate_slab1+ '_' +Seriestime_slab1
                elif numberofperfusionslabs == 0:    
                    Seriesdate_slab1=self.voldict_outputjson['DICOMHeaderInfo']['DiffusionSeries'][0]['SeriesDate']
                    Seriestime_slab1=self.voldict_outputjson['DICOMHeaderInfo']['DiffusionSeries'][0]['SeriesTime']
                    self.SeriesDateTime_slab1=Seriesdate_slab1+ '_' +Seriestime_slab1
                elif numberofperfusionslabs == 2: 
                    Seriesdate_slab1=self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][0]['SeriesDate']
                    Seriestime_slab1=self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][0]['SeriesTime']
                    self.SeriesDateTime_slab1=Seriesdate_slab1+ '_' +Seriestime_slab1
       
                    
                    Seriesdate_slab2=self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][1]['SeriesDate']
                    Seriestime_slab2=self.voldict_outputjson['DICOMHeaderInfo']['PerfusionSeries'][1]['SeriesTime']
                    self.SeriesDateTime_slab2=Seriesdate_slab2+ '_' +Seriestime_slab2
            except:
                #self.SeriesDateTime=-1
                self.SeriesDateTime_slab1=-1
                self.SeriesDateTime_slab2=-1
                
        measfile=foldername+"/measurements.json"
        if os.path.isfile(measfile):
            self.voldict=RPDjsonR47.readJSON(measfile)
            self.numberofslabs=self.voldict["numberofslabs"]
            self.HypoperfusionIndex_slab1=self.voldict["HypoperfusionIndex_slab1"]
            self.HypoperfusionIndex_slab2=self.voldict["HypoperfusionIndex_slab2"]
            self.CBVIndex_slab1=self.voldict["CBVIndex_slab1"]
            self.CBVIndex_slab2=self.voldict["CBVIndex_slab2"]
            
            if self.voldict["returncode"]==0:
                self.foldername=foldername
                self.statuscode=bool(0)
                self.errormessage=""
                self.modality=self.voldict["coremodal"]
                if self.modality=='CT':
                    self.type='CTP'
                    self.allpng=[k for k in glob.glob(foldername+"/results/*Mismatch.png") if not re.search('thumbnail',k)]
                    self.summaryimg=common.get_indx(self.allpng,".*series.*Mismatch.png")
                     
                    self.aifcurve=common.get_indx(self.allpng,".*series.*_AIF_VOF_Curves.png")
                    self.aifloc=common.get_indx(self.allpng,".*series.*_AIF_VOF_Locations.png")
                    
                else: #it was MR
                    self.allpng=[k for k in glob.glob(foldername+"/results/*series*view*.png") if not re.search('thumbnail',k)]
                    
                    if self.voldict["tmaxvolumes"][0]=='NA' and self.voldict["corevolumes"][0]!='NA':  #DWI only
                        self.type='DWI'
                        self.summaryimg=common.get_indx(self.allpng,".*series.*_ADC_Threshold.png")
                    else:
                        self.type='DWIPWI'
                        self.summaryimg=common.get_indx(self.allpng,".*series.*ADC_Tmax_Mismatch.png")
                        self.aifcurve=common.get_indx(self.allpng,".*series.*_AIF_VOF_Curves.png")
                        self.aifloc=common.get_indx(self.allpng,".*series.*_AIF_VOF_Locations.png")
            
                    
                return
            else:
                self.statuscode=bool(1)
                self.errormessage="Measurements.json is incomplete"
                self.modality=""   
                return
        else:       
            self.statuscode=bool(1)
            self.errormessage="No measurements.json available"
            self.modality=""
            self.voldict=RPDjsonR47.get_no_voldict()
            return
        

                
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
    
    def zcoverage(self):
        return self.zcoverage
    
    def zcoverage_slab1(self):
        return self.zcoverage_slab1
    
    def zcoverage_slab2(self):
        return self.zcoverage_slab2
    
    def HypoperfusionIndex_slab1(self):
        return self.HypoperfusionIndex_slab1
    
    def CBVIndex_slab1(self):
        return self.CBVIndex_slab1
    
    def HypoperfusionIndex_slab2(self):
        return self.HypoperfusionIndex_slab2
    
    def CBVIndex_slab2(self):
        return self.CBVIndex_slab2
    
    
#    
#if __name__ == "__main__":
#     op=RAPID46OP("/Users/icasdb/Desktop/D3_R47_RANDOMIZED_FINAL/254/FU/Results_CTP_R47/")
#     print(op.HypoperfusionIndex_slab1)
#     print(op.HypoperfusionIndex_slab2)
#     print(op.CBVIndex_slab1)
#     print(op.CBVIndex_slab2)
        
    
    
    