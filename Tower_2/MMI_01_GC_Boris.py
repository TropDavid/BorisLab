# HyperLight Chip 01
#
#
#
import os
import numpy as np
import gdspy
import math
import uuid



exportname = "MMI_Tower"

bend_rad=50
taperW=2
chipW=6000
chipH=6000

LayerText   = 1
LayerWaveguides= 2
LayerResonators= 3
LayerGratings= 4
LayerAlignmentMarks= 5
LayerSlabetch = 6 
GC_pich=127

ld_NWG = {"layer": 174, "datatype": 0}
ld_Silox = {"layer": 9, "datatype": 0}
ld_taper = {"layer": 8, "datatype": 0}
ld_GC = {"layer": 118, "datatype": 121}
ld_taperMark = {"layer": 118, "datatype": 120}






def grating(period, number_of_teeth, fill_frac, width, position, direction, lda=1, sin_theta=0,
            focus_distance=-1, focus_width=-1, tolerance=0.001, layer=0, datatype=0):
    '''
    Straight or focusing grating.

    period          : grating period
    number_of_teeth : number of teeth in the grating
    fill_frac       : filling fraction of the teeth (w.r.t. the period)
    width           : width of the grating
    position        : grating position (feed point)
    direction       : one of {'+x', '-x', '+y', '-y'}
    lda             : free-space wavelength
    sin_theta       : sine of incidence angle
    focus_distance  : focus distance (negative for straight grating)
    focus_width     : if non-negative, the focusing area is included in
                      the result (usually for negative resists) and this
                      is the width of the waveguide connecting to the
                      grating
    tolerance       : same as in `path.parametric`
    layer           : GDSII layer number
    datatype        : GDSII datatype number

    Return `PolygonSet`
    '''
    if focus_distance < 0:
        p = gdspy.L1Path((position[0] - 0.5 * width,
                          position[1] + 0.5 * (number_of_teeth - 1 + fill_frac) * period),
                         '+x', period * fill_frac, [width], [], number_of_teeth, period,
                         **ld_Silox )
    else:
        neff = lda / float(period) + sin_theta
        qmin = int(focus_distance / float(period) + 0.5)
        p = gdspy.Path(period * fill_frac, position)
        c3 = neff**2 - sin_theta**2
        w = 0.5 * width
        for q in range(qmin, qmin + number_of_teeth):
            c1 = q * lda * sin_theta
            c2 = (q * lda)**2
            p.parametric(lambda t: (width * t - w,
                                    (c1 + neff * np.sqrt(c2 - c3 * (width * t - w)**2)) / c3),
                         tolerance=tolerance, max_points=0, **ld_NWG )
            p.x = position[0]
            p.y = position[1]
        sz = p.polygons[0].shape[0] // 2
        if focus_width == 0:
            p.polygons[0] = np.vstack((p.polygons[0][:sz, :], [position]))
        elif focus_width > 0:
            p.polygons[0] = np.vstack((p.polygons[0][:sz, :],
                                          [(position[0] + 0.5 * focus_width, position[1]),
                                           (position[0] - 0.5 * focus_width, position[1])]))
        p.fracture()
        circle = gdspy.Round((position[0],position[1]+25), 30, tolerance=0.01,**ld_Silox)
        Rec = gdspy.Rectangle((position[0] - 15,position[1]+25 -15 ), (position[0] +15,position[1]+25 + 15))
        bound = gdspy.Round((position[0],position[1]+25), 30, tolerance=0.01,**ld_GC )

    if direction == '-x':
        return p.rotate(0.5 * np.pi, position),Rec,bound
    elif direction == '+x':
        return p.rotate(-0.5 * np.pi, position),Rec,bound
    elif direction == '-y':
        return p.rotate(np.pi, position),Rec,bound
    else:
        return p,Rec,bound


def sbendPath(wgsbend,L=100,H=50,layer=1,datatype=0):
# the formula for cosine-shaped s-bend is: y(x) = H/2 * [1- cos(xpi/L)]
# the formula for sine-shaped s-bend is: y(x) = xH/L - H/(2pi) * sin(x2*pi/L)
    def sbend(t):
        x = H/2 * (1- np.cos(t*np.pi))
        y =L*t
        
        return (x,y)
    def dtsbend(t):
        dx_dt = H/2*np.pi*np.sin(t*np.pi)
        dy_dt = L

        return (dx_dt, dy_dt)

    wgsbend.parametric(sbend ,dtsbend , number_of_evaluations=100,layer=layer,datatype=datatype)  
    return wgsbend

# def sbendPath1(x0=0,y0=0,w0=1,L=100,H=50,layer=1):
#     def sbend(t):
#         x=t*L
#         y = t*H - H/(2*np.pi) * np.sin(t*2*np.pi)
#         return (x,y)
#     wgsbend = gdspy.Path(w0, (x0,y0))
#     wgsbend.parametric(sbend,number_of_evaluations=90,layer=layer)  
#     return wgsbend

def MMI2x2(x0=0,y0=0,w0=0.8,MMILength=60,MMIW=9,MMISeparate=3,taperL=10, taperW=1.3,layer=1,datatype=0):
    MMICell=gdspy.Cell("mmi"+str(uuid.uuid4() ))
    yc=MMILength/2+taperL
    port1 = gdspy.Path(w0, (x0+MMISeparate/2, y0-yc))
    port1.segment(taperL,direction='+y', final_width=taperW,layer=layer,datatype=datatype)    # taper
    
    port2 = gdspy.Path(w0, (x0-MMISeparate/2, y0-yc))
    port2.segment(taperL,direction='+y', final_width=taperW,layer=layer,datatype=datatype)    # taper
   
    port3 = gdspy.Path(taperW, (x0+MMISeparate/2, y0+MMILength+taperL-yc))
    port3.segment(taperL,direction='+y', final_width=w0,layer=layer,datatype=datatype)    # taper
    
    port4 = gdspy.Path(taperW, (x0-MMISeparate/2, y0+MMILength+taperL-yc))
    port4.segment(taperL,direction='+y', final_width=w0,layer=layer,datatype=datatype)    # taper
   
    ports=[(x0-yc, y0+MMISeparate/2),(x0-yc, y0-MMISeparate/2),(port3.x,port3.y),(port4.x,port4.y)]

    MMI=gdspy.Rectangle((0,0), (MMIW,MMILength), layer=layer,datatype=datatype)
    MMI.translate(x0-MMIW/2,y0-MMILength/2)
    MMI2=gdspy.Rectangle((-5,-5), (MMIW +5,MMILength + 5), **ld_taperMark)
    MMI2.translate(x0-MMIW/2,y0-MMILength/2)
    MMICell.add([MMI,MMI2,port1,port2,port3,port4])
    return [MMICell, ports]

def MMI1x2(x0=0,y0=0,w0=0.8,MMILength=60,MMIW=9,MMISeparate=3,taperL=10, taperW=1.3,layer=0,datatype=0):
    MMICell=gdspy.Cell("mmi"+str(uuid.uuid4() ))
    yc=MMILength/2+taperL
    port1 = gdspy.Path(w0, (x0, y0-yc))
    port1.segment(taperL,direction='+y', final_width=taperW,layer=layer,datatype=datatype)    # taper
    
    port2 = gdspy.Path(w0, (x0-MMISeparate/2, y0-yc))
    port2.segment(taperL,direction='+y', final_width=taperW,layer=layer,datatype=datatype)    # taper
   
    port3 = gdspy.Path(taperW, (x0+MMISeparate/2, y0+MMILength+taperL-yc))
    port3.segment(taperL,direction='+y', final_width=w0,layer=layer,datatype=datatype)    # taper
    
    port4 = gdspy.Path(taperW, (x0-MMISeparate/2, y0+MMILength+taperL-yc))
    port4.segment(taperL,direction='+y', final_width=w0,layer=layer,datatype=datatype)    # taper
   
    ports=[(x0-yc, y0+MMISeparate/2),(x0-yc, y0-MMISeparate/2),(port3.x,port3.y),(port4.x,port4.y)]

    MMI=gdspy.Rectangle((0,0), (MMIW,MMILength), layer)
    MMI.translate(x0-MMIW/2,y0-MMILength/2)
    MMICell.add([MMI,port1,port3,port4])
    return [MMICell, ports]



def aligmentMarkLW(x0=0,y0=0,L=100,W=1,layer=1):
    alig = gdspy.Cell('aligMarkLW')
    sline1 = gdspy.Path(W, (x0-L*0.5, y0))
    sline1.segment(L,direction='+x', final_width=W,layer=layer) 
    sline2 = gdspy.Path(W, (x0, y0-L*0.5))
    sline2.segment(L,direction='+y', final_width=W,layer=layer) 
    rr = gdspy.Round((x0+L/4, y0+L/4), 2,layer=layer)
    alig.add([sline1,sline2,rr])
    return  alig


def GC_test(period=0.83, number_of_teeth=20, fill_frac=0.3, width=21.5,wGwidth=0.8, position=(0,0), lda=1.55, sin_theta=0,layer=1,datatype=0):
    GCTC=gdspy.Cell("GC"+str(uuid.uuid4() ))
    
    GCTC.add(grating(period=period, number_of_teeth=number_of_teeth, fill_frac=fill_frac, width=width, position=position, direction='+y', lda=lda,
                     sin_theta=np.sin(np.pi * -8 / 180), focus_distance=21.5,focus_width= wGwidth,tolerance=0.001,layer=layer,datatype=datatype))
    

    GCTC.add(grating(period=period, number_of_teeth=number_of_teeth, fill_frac=fill_frac, width=width, position=(position[0]+GC_pich,position[1]), direction='+y', lda=lda,
                     sin_theta=np.sin(np.pi * -8 / 180), focus_distance=21.5,focus_width= wGwidth,tolerance=0.001,layer=layer,datatype=datatype))
    
    wg1 = gdspy.Path(wGwidth, position)
    wg1.segment(100,direction='-y',layer=layer,datatype=datatype)

    wg1.turn(GC_pich/2,angle=np.pi,layer=layer,datatype=datatype,number_of_points=500)
    wg1.segment(100,direction='+y',layer=layer,datatype=datatype)

    GCTC.add(wg1)


    return GCTC





def MMI2x2_test(period=1.15, number_of_teeth=20, fill_frac=0.41, width=21.5,wGwidth=1, position=(0,0), lda=1.55, sin_theta=0,layer=1,
    MMILength=75,MMIW=9,MMISeparate=3,taperL=10,
    taperW=1.2,datatype=0 , C = 0 , R = 0):
    string = "R" + str(R) + "C" + str(C)
    text = gdspy.Text(string, 100 , position =( position[0]  , position[1] - 150))
    #top_cell.add(text)
   
    MMI2x2_test=gdspy.Cell("MMI2x2_test"+str(uuid.uuid4() ))
    
    
    GC=grating(period=period, number_of_teeth=number_of_teeth, fill_frac=fill_frac, width=width, position=position, direction='+y', lda=lda,
                     sin_theta=np.sin(np.pi * -8 / 180), focus_distance=21.5,focus_width= wGwidth,tolerance=0.001,layer=layer,datatype=datatype)
    GCcell=gdspy.Cell('GCcell'+str(uuid.uuid4() )).add(GC)


    MMI2x2_test.add(gdspy.CellArray(GCcell,4,1,(GC_pich,0),(0,0),))
  
    shifterS=GC_pich-MMISeparate
    print(position)
    wg1 = gdspy.Path(wGwidth, (position[0]+GC_pich,position[1]))
    print(position)
    wg1.segment(0,direction='-y',layer=layer,datatype=datatype)
    sbendPath(wgsbend=wg1,L=-100,H=shifterS/2,layer=layer,datatype=datatype)
    print(wg1.x )
 
    wg2 = gdspy.Path(wGwidth, (position[0]+GC_pich*2,position[1]))
    wg2.segment(0,direction='-y',layer=layer,datatype=datatype)
    sbendPath(wgsbend=wg2,L=-100,H=-shifterS/2,layer=layer,datatype=datatype)
    
    # wg1.turn(GC_pich/2,angle=np.pi,layer=LayerWaveguides,number_of_points=500)
    # wg1.segment(100,direction='+y',layer=LayerWaveguides)
    MMICell,ports2=MMI2x2(x0=wg1.x+MMISeparate/2,y0=wg1.y-(MMILength/2+taperL),MMIW=MMIW,taperW=taperW,MMISeparate=MMISeparate,MMILength=MMILength,w0=wGwidth,layer=layer,datatype=datatype)

    wg4= gdspy.Path(wGwidth, (wg2.x,wg2.y-MMILength-2*taperL))
    wg4.segment(0,direction='-y',layer=layer,datatype=datatype)
    sbendPath(wgsbend=wg4,L=-100,H=shifterS/2,layer=layer,datatype=datatype)
    wg4.turn(GC_pich/2,np.pi,layer=layer,datatype=datatype)
    wg4.segment(wg4.y-position[1],direction='-y',layer=layer,datatype=datatype)
    


    wg3 = gdspy.Path(wGwidth, (wg1.x,wg1.y-MMILength-2*taperL))
    wg3.segment(0,direction='-y',layer=layer,datatype=datatype)
    sbendPath(wgsbend=wg3,L=-100,H=-shifterS/2,layer=layer,datatype=datatype)
    wg3.turn(GC_pich/2,-np.pi,layer=layer,datatype=datatype)
    wg3.segment(wg3.y-position[1],direction='-y',layer=layer,datatype=datatype)
    

    MMI2x2_test.add([wg1, wg2,wg3,wg4])




    MMI2x2_test.add(gdspy.CellReference(MMICell,(0,0)))

    return MMI2x2_test


def MMI1x2_test(period=1.15, number_of_teeth=20, fill_frac=0.41, width=21.5,wGwidth=1, position=(0,0), lda=1.55, sin_theta=0,layer=1,
    MMILength=75,MMIW=9,MMISeparate=3,taperL=10,
    taperW=1.2):
   
    MMI1x2_test=gdspy.Cell("MMI2x2_test"+str(uuid.uuid4() ))
    
    
    GC=grating(period=period, number_of_teeth=number_of_teeth, fill_frac=fill_frac, width=width, position=position, direction='+y', lda=lda,
                     sin_theta=np.sin(np.pi * -8 / 180), focus_distance=21.5,focus_width= wGwidth,tolerance=0.001,layer=LayerGratings)
    GCcell=gdspy.Cell('GCcell'+str(uuid.uuid4() )).add(GC)


    MMI1x2_test.add(gdspy.CellArray(GCcell,4,1,(GC_pich,0),(0,0),))
  
    shifterS=GC_pich-MMISeparate
    wg1 = gdspy.Path(wGwidth, (position[0]+GC_pich,position[1]))
    wg1.segment(0,direction='-y',layer=LayerWaveguides)
    sbendPath(wgsbend=wg1,L=-100,H=shifterS/2,layer=LayerWaveguides)
    
    wg2 = gdspy.Path(wGwidth, (position[0]+GC_pich*2,position[1]))
    wg2.segment(0,direction='-y',layer=LayerWaveguides)
    sbendPath(wgsbend=wg2,L=-100,H=-shifterS/2,layer=LayerWaveguides)
    
    # wg1.turn(GC_pich/2,angle=np.pi,layer=LayerWaveguides,number_of_points=500)
    # wg1.segment(100,direction='+y',layer=LayerWaveguides)
    MMICell,ports2=MMI1x2(x0=wg1.x+MMISeparate/2,y0=wg1.y-(MMILength/2+taperL),MMIW=MMIW,taperW=taperW,MMISeparate=MMISeparate,MMILength=MMILength,w0=wGwidth,layer=LayerWaveguides)

    
    


    wg3 = gdspy.Path(wGwidth, (position[0]+GC_pich*1.5,wg1.y-MMILength-2*taperL))
    wg3.segment(0,direction='-y',layer=LayerWaveguides)
    sbendPath(wgsbend=wg3,L=-100,H=-shifterS/2,layer=LayerWaveguides)
    wg3.turn(GC_pich/2,-np.pi,layer=LayerWaveguides)
    wg3.segment(wg3.y-position[1],direction='-y',layer=LayerWaveguides)
    

    MMI1x2_test.add([wg1, wg2,wg3])




    MMI1x2_test.add(gdspy.CellReference(MMICell,(0,0)))

    return MMI1x2_test


def rotateShift(fromCell,toCell,position=(0,0)):
    [[x_min, y_min], [x_max, y_max]]=fromCell.get_bounding_box()
    print([[x_min, y_min], [x_max, y_max]])
    # toCell.add(gdspy.CellArray(fromCell, columns=1, rows=1, spacing=(1,1), rotation=180, origin=((x_max-x_min)+position[0],(y_max-y_min)+position[1])))
    toCell.add(gdspy.CellArray(fromCell, columns=1, rows=1, spacing=(1,1), rotation=180, origin=((x_max)+position[0],(y_max)+position[1])))


############################### Main Routine

top_cell = gdspy.Cell("topcell")

GC1 = gdspy.Cell("gc1")



# grating coupler test
# period_array=np.linspace(0.8,0.9,11)
# FF_array=np.linspace(0.3,0.4,11)

# for k in range(int(len(period_array)/2)):
#     for j in range(len(FF_array)):
#         GC1.add(gdspy.CellReference(GC_test(period=period_array[k*2],fill_frac=FF_array[j],position=(k*600,j*350)), (0, +0)))
#         GC1.add(gdspy.CellReference(GC_test(period=period_array[k*2+1],fill_frac=FF_array[j],position=(k*600+128*2,j*350)), (0, +0)))


# [[x_min, y_min], [x_max, y_max]]=GC1.get_bounding_box()
# print([[x_min, y_min], [x_max, y_max]])
# # top_cell.add(gdspy.CellReference(GC1, (0,3000)))
# top_cell.add(gdspy.CellArray(GC1, columns=1, rows=1, spacing=(1,1), rotation=180, origin=((x_max-x_min)+0,(y_max-y_min)+3000)))

# rotateShift(GC1,top_cell,position=(0,3000))

GC2 = gdspy.Cell("gc2")

# grating coupler test
period_array=np.linspace(1.1,1.2,11)
FF_array=np.linspace(0.35,0.45,11)


for k in range(int(len(period_array)/2)):
    for j in range(len(FF_array)):
        GC2.add(gdspy.CellArray(GC_test(period=period_array[k*2],fill_frac=FF_array[j],
            position=(k*600,j*350), **ld_NWG), columns=1, rows=1, spacing=(1,1), rotation=0,origin=(0, +0)))
      
        # GC2.add(gdspy.CellArray(GC_test(period=period_array[k*2+1],fill_frac=FF_array[j],position=(k*600+128*2,j*350)), columns=1, rows=1, spacing=(1,1), rotation=0, origin=(0, +0)))


top_cell.add(gdspy.CellReference(GC2, (8000,3000)))



MMIL_array=np.linspace(60,80,21)
MMItw_array=np.linspace(1.2,1.4,2)

MMITW_array=np.linspace(0.3,0.4,11)

MMIL_array1=np.linspace(25,45,21)
MMItw_array1=np.linspace(1.2,1.4,2)

MMI2x2Cell = gdspy.Cell("MMI2x2")
C  = -1

for k in range(int(len(MMIL_array))):
    C = C + 1
    R = -1
    for j in range(int(len(MMItw_array))):
        R = R + 1
        MMI2x2Cell.add(gdspy.CellReference(MMI2x2_test(period=1.15,fill_frac=0.41,MMIW=9,MMISeparate=3.15,MMILength=MMIL_array[k],taperW=MMItw_array[j],position=(k*600,(j)*700), **ld_NWG , C = C , R = R), (0, 0)))
        #MMI2x2Cell.add(gdspy.CellReference(MMI2x2_test(period=1.15,fill_frac=0.41,MMIW=6,MMISeparate=2.15,MMILength=MMIL_array1[k],taperW=MMItw_array1[j],position=(k*600,(j+2)*700), **ld_NWG , C = C , R = R), (0, 0)))

      
# top_cell.add(gdspy.CellReference(MMI2x2Cell, (0,0)))
rotateShift(MMI2x2Cell,top_cell,position=(0,0))



# MMIL_array=np.linspace(45,65,21)
# MMItw_array=np.linspace(1.2,1.4,2)

# MMIL_array1=np.linspace(25,45,21)
# MMItw_array1=np.linspace(1.2,1.4,2)

#MMI1x2Cell = gdspy.Cell("MMI1x2")

# for k in range(int(len(MMIL_array))):
#     for j in range(int(len(MMItw_array))):
#         MMI1x2Cell.add(gdspy.CellReference(MMI1x2_test(period=0.8,fill_frac=0.33,MMISeparate=4.7,MMIW=9,MMILength=MMIL_array[k],taperW=MMItw_array[j],position=(k*600,j*700)), (0, -0)))
#         MMI1x2Cell.add(gdspy.CellReference(MMI1x2_test(period=0.8,fill_frac=0.33,MMISeparate=3.1,MMIW=6,MMILength=MMIL_array1[k],taperW=MMItw_array1[j],position=(k*600,(j+2)*700)), (0, -0)))

# top_cell.add(gdspy.CellReference(MMI1x2Cell, (0,-4000)))
#rotateShift(MMI1x2Cell,top_cell,position=(0,-4000))



gdsii = gdspy.GdsLibrary()


## ------------------------------------------------------------------ ##
##  OUTPUT                                                            ##
## ------------------------------------------------------------------ ##

## Output the layout to a GDSII file (default to all created cells).
gdspy.write_gds(exportname+'.gds', unit=1.0e-6, precision=1.0e-9)
faltten_cell=top_cell.flatten()
gdspy.write_gds(exportname+'_flattened.gds', cells=[faltten_cell], unit=1.0e-6, precision=1.0e-9)
print('Using gdspy module version ' + gdspy.__version__)


# #Cell area
# textarea = 'Area = %d um^2' % (top_cell.area()) 
# exptime=(top_cell.area()*0.00008961209);
# exptime1=(top_cell.area()*0.000256);
# print(textarea + ' ZEP exposure time :'+ str(round(exptime)) +' min, HSQ exposure time:'+str(round(exptime1))+' min')
  

## ------------------------------------------------------------------ ##
##  VIEWER                                                            ##
## ------------------------------------------------------------------ ##

## View the layout using a GUI.  Full description of the controls can
## be found in the online help at http://gdspy.sourceforge.net/
#gdspy.LayoutViewer() 

# gdspy.LayoutViewer()








