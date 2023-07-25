# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 10:11:37 2023

@author: LUM
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import imp
bend_radius = [0,30e-6]
loss = np.array(np.zeros(4))
s_count = -1
 




lumapi = imp.load_source("lumapi","C:\\Program Files\\Lumerical\\v231\\api\python\\lumapi.py") 

MODE = lumapi.MODE() 
     
    

    




    

   

    

MODE.addrect(x = 0,y = 0 ,z = 0 , x_span = 10e-6 , y_span = 5e-6)
MODE.set("material","SiO2 (Glass) - Palik")
MODE.set("name","SiO2 sub")
    
MODE.addrect(x = 0,y = 0 ,z = 0 , x_span = 1e-6 , y_span = 0.3e-6)
MODE.set("material","Si3N4 (Silicon Nitride) - Luke")
MODE.set("name","Si3N4")
    
    
  
    
    
    



    
solver = MODE.addfde(x = 0,x_span = 5e-6,y = 0 , y_span = 7e-6)
solver["mesh cells x"]=600
solver["mesh cells y"]=600
solver["wavelength"]=1.55e-6
solver["number of trial modes"]=2
solver["use max index"]=1
    
MODE.set("x min bc","PML")
MODE.set("x max bc","PML")
MODE.set("y min bc","PML")
MODE.set("y max bc","PML")

            
MODE.run()
MODE.mesh()
nmodes = MODE.findmodes()

    
    
fig=plt.figure(figsize=(15,15))
fig.tight_layout()
    
    
for modeN in range(1,int(nmodes+1)): 
        dataStr="FDE::data::mode"+str(modeN)
        TETM=MODE.getdata(dataStr,"TE polarization fraction");
        
        MODE.selectmode(modeN)
        
        
        if(TETM > 0.5):
                s_count = s_count +1
                x=MODE.getdata(dataStr,"x")*1e6
                y=MODE.getdata(dataStr,"y")*1e6
                neff=MODE.getdata(dataStr,"neff");
                
                   
                Ex=MODE.getdata(dataStr,"Ex")
                Ey=MODE.getdata(dataStr,"Ey");
                Ez=MODE.getdata(dataStr,"Ez");
                E2=abs(Ex[:,:,0,0]**2+Ey[:,:,0,0]**2+Ez[:,:,0,0]**2)  
                loss[s_count] = MODE.getdata(dataStr,"loss") 
                
                
                ind = MODE.getdata("FDE::data::material","index_x")
                index = ind[:,:,0,0]
                
                
                
                
                
                
                title="\n\n\n\n Neff=" + str(np.round(np.real(neff[0][0]),3)) +", TE/TM = "  +str(np.round(TETM,2)) 
                plt.subplot(2, 1,1)
                
                plt.imshow(np.transpose(E2), aspect='equal', interpolation='bicubic', cmap=cm.jet, #cmap=cm.RdYlGn
                           origin='lower', extent=[x.min(), x.max(), y.min(), y.max()],
                           vmax=E2.max(), vmin=E2.min())         
                       
                plt.subplot(2,1,1 ).set_title(title)
                plt.colorbar()
                plt.contour(np.transpose(np.sqrt(np.real((index))**2 + np.imag((index))**2)),colors = "k",width = 1, extent = [x.min(),x.max(),y.min(),y.max()])
                plt.xlabel('x (um)')
                plt.ylabel('y (um)')
                
               
        if(TETM < 0.5):
                
                x=MODE.getdata(dataStr,"x")*1e6
                y=MODE.getdata(dataStr,"y")*1e6
                neff=MODE.getdata(dataStr,"neff")
                        
                Ex=MODE.getdata(dataStr,"Ex")
                Ey=MODE.getdata(dataStr,"Ey");
                Ez=MODE.getdata(dataStr,"Ez");
                E2=abs(Ex[:,:,0,0]**2+Ey[:,:,0,0]**2+Ez[:,:,0,0]**2)
                loss[s_count] = MODE.getdata(dataStr,"loss") 
                
                #plt.subplots_adjust(wspace=2,hspace=2)
                ind = MODE.getdata("FDE::data::material","index_x")
                index = ind[:,:,0,0]
                
                
                
                title="\n\n\n\n Neff=" + str(np.round(np.real(neff[0][0]),3)) +", TE/TM = "  +str(np.round(TETM,2)) 
                plt.subplot(2, 1 , 2)
                
                plt.imshow(np.transpose(E2), aspect='equal', interpolation='bicubic', cmap=cm.jet, #cmap=cm.RdYlGn
                           origin='lower', extent=[x.min(), x.max(), y.min(), y.max()],
                           vmax=E2.max(), vmin=E2.min())         
                       
                plt.subplot(2,1,2).set_title(title)
                plt.colorbar()
                plt.contour(np.transpose(np.sqrt(np.real((index))**2 + np.imag((index))**2)),colors = "k",width = 1,extent = [x.min(),x.max(),y.min(),y.max()])
                plt.xlabel('x (um)')
                plt.ylabel('y (um)')
                
                
                
                
               
    
    
plt.suptitle("Si3N4_WG",fontsize=15) # or plt.suptitle('Main title')
plt.savefig("Si3N4_WG")
        
    #MODE.close()
    