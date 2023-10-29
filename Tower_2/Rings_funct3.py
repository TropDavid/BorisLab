# Tower test Silicon nitride chip.
# Based on Tower SIN PDK PH18
#
# Confidential - do not distribute
# 28/05/2023 - David TroP, Boris Desiatov - BIU. ISRAEL

import gdspy
import numpy as np
import uuid
lib = gdspy.GdsLibrary()

ld_NWG = {"layer": 174, "datatype": 0}
ld_Silox = {"layer": 9, "datatype": 0}
ld_taperMark = {"layer": 118, "datatype": 120}
ld_GC = {"layer": 118, "datatype": 121}
ld_SUS = {"layer": 195, "datatype": 0}
ld_VG1 = {"layer": 192, "datatype": 0}
ld_TNR = {"layer": 26, "datatype": 0}
ld_VIA1 = {"layer": 17, "datatype": 0}
ld_VIA2 = {"layer": 27, "datatype": 0}
ld_METAL2 = {"layer": 18, "datatype": 0}
ld_METAL3 = {"layer": 28, "datatype": 0}
ld_ABLB = {"layer": 118, "datatype": 53}
ld_PHMMI = {"layer": 118, "datatype": 164}

ld_dataExtend = {"layer": 118, "datatype": 134}



chip_length = 5000 #microns
Chip_Height = 5000 #microns
Spacing_length_at_start = 206
Spacing_Height_at_start = 206
Taper_length = 200
Taper_Width = 0.15
SUS_spacing = 0
SUS_width=70
VG_spacing=-5
VG_width=78
chip_X0, chip_Y0= -chip_length/2,-Chip_Height/2

my_length = chip_length - Spacing_length_at_start - Taper_length
my_height = Chip_Height - Spacing_Height_at_start

Width_WG = np.array([1,0.7])
gap = np.array([0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6]) + 0.05

Spacing_Ring_Waveguide = 20
height_in_S = 10
Rad = np.array([50,100])
Spacing_between_Straight = 30

ringHeaterWidth=3
ringHeaterSpacing=3

## Vias size
via1Size=0.26
via1Spacing=0.26
via2Size=0.5
via2Spacing=0.5
# Metal
metal1Width=10
metalLineWidth=10
padSize=100
padSpacing=150
MetalLineOffset=70

def a2r(ang):  # angle to radian
    return np.pi/180*ang

top_cell =lib.new_cell('TOP')

# define a bunch of 9 microring resoantors
def Ring( cellname='cell' ,Width_Waveguide=0.5, gap_array=[10,20] ,Radius=0.3, Basic_Straight_step=0 ):
    Ringcell = lib.new_cell(cellname)

    for i in range(0,9):

        path1 = gdspy.Path(Taper_Width , (-my_length/2 , my_height/2 - Spacing_between_Straight*(i)  ))

        path3 = gdspy.Path(3 , (-my_length/2 , my_height/2 - Spacing_between_Straight*(i) ))
        path3.segment(length=Taper_length,direction= "+x" ,** ld_taperMark)

        path1.segment(length=Taper_length,direction= "+x",final_width= Width_Waveguide ,** ld_NWG)
        path1.segment(Basic_Straight_step*(i+1),"+x",** ld_NWG)
        x = path1.x
        y = path1.y
        path1.segment(Radius,"+x",** ld_NWG)
        path1.segment(Spacing_Ring_Waveguide,"+x",** ld_NWG)
        path1.turn(Radius,"l",** ld_NWG)
        path1.segment(height_in_S,"+y",** ld_NWG)
        path1.turn(Radius,"r",** ld_NWG)
        path1.segment(my_length - Basic_Straight_step*(i+1) - 3*Radius - Spacing_Ring_Waveguide,"+x",** ld_NWG)
        xT = path1.x
        yT = path1.y
        path1.segment(length=Taper_length,direction= "+x",final_width= Taper_Width,** ld_NWG)

        path2 = gdspy.Path(Width_Waveguide,(x,y+gap_array[i]+Width_Waveguide))
        path2.turn(Radius,"ll",** ld_NWG)
        path2.turn(Radius,"ll",** ld_NWG)

        path4 = gdspy.Path(3,(xT,yT))
        path4.segment(length=Taper_length,direction= "+x" ,** ld_taperMark)


        Ringcell.add(path1)
        Ringcell.add(path2)
        Ringcell.add(path3)
        Ringcell.add(path4)
        
        Heatercell = lib.new_cell(cellname+"heater"+str(i))

        # draw heater 
        # Titanium Heater
        heaterRadius=Radius - (ringHeaterSpacing/2 + ringHeaterWidth/2)
        angle=270+30
        path5 = gdspy.Path( ringHeaterWidth ,(x + heaterRadius * (np.cos(a2r(angle))) , y+gap_array[i]+Width_Waveguide+ringHeaterSpacing + heaterRadius* (1+np.sin(a2r(angle)))  ))
        path5.arc(radius= heaterRadius  ,  initial_angle= a2r(angle) , final_angle=5*np.pi -a2r(angle),** ld_TNR)
        # TNR pads
        path5.turn(radius= 5  ,angle=1*np.pi/2-a2r(270-angle) ,final_width=6,** ld_TNR)
        path5.segment(final_width=metal1Width,direction="+y", length=4 ,** ld_TNR)
        saveXVias,saveYVias,=path5.x,path5.y
        path5.segment(final_width=metal1Width,direction="+y", length=metal1Width ,** ld_TNR)
        path6=gdspy.copy(path5)
        points=path5.get_bounding_box()
        path6.mirror(p1=((points[1,0]+points[0,0])/2 ,points[0,1]), p2= ((points[1,0]+points[0,0])/2 ,points[1,1])) 
        Heatercell.add(gdspy.boolean(path5,path6,"or",** ld_TNR))
        # Via 1 to metal 2,
        via1cell = lib.new_cell("via1"+str(uuid.uuid4()))
        via1 = gdspy.Rectangle((- via1Size/2 , - via1Size/2), (via1Size/2, via1Size/2), **ld_VIA1)
        via1cell.add(via1)
        Heatercell.add(gdspy.CellArray(ref_cell=via1cell, columns=round(metal1Width/(2*via1Size))-2, rows=round(metal1Width/(2*via1Size))-2, spacing=[ via1Spacing*2, via1Spacing*2], origin=(saveXVias-metal1Width/2+ via1Size*3,saveYVias+ via1Size*3)))
        # Metal 2,
        metal2 = gdspy.Path( metal1Width ,(saveXVias,saveYVias))
        metal2.segment(metal1Width,direction='+y', **ld_METAL2)
        Heatercell.add(metal2)
        # Via 2 between metal 2 and metal 3,
        via2cell = lib.new_cell("via2"+str(uuid.uuid4()))
        via2 = gdspy.Rectangle((- via2Size/2 , - via2Size/2), (via2Size/2, via2Size/2), **ld_VIA2)
        via2cell.add(via2)
        Heatercell.add(gdspy.CellArray(ref_cell=via2cell, columns=round(metal1Width/(2*via2Size))-2, rows=round(metal1Width/(2*via2Size))-2, spacing=[ via2Spacing*2, via2Spacing*2], origin=(saveXVias-metal1Width/2+ via2Size*3,saveYVias+ via2Size*3)))

        # Metal 3 and contacts pads
        metal3 = gdspy.Path( metal1Width ,(saveXVias,saveYVias))
        metal3.segment(metal1Width,direction='+y', **ld_METAL3)
        metalLine=gdspy.Path( metalLineWidth ,(metal3.x,metal3.y))
        metalLine.segment(MetalLineOffset+padSize ,direction='+y', **ld_METAL3)
        metalLine.segment(MetalLineOffset ,direction='-x', **ld_METAL3)

        # Heatercell.add(gdspy.boolean(metal3,metalLine,'or',**ld_METAL3))
        #pad
        metalPad=gdspy.Path( padSize ,(metalLine.x,metalLine.y-metalLineWidth/2))
        metalPad.segment(padSize ,direction='+y', **ld_METAL3)
        Heatercell.add(gdspy.boolean(metalPad,gdspy.boolean(metal3,metalLine,'or',**ld_METAL3) ,'or',**ld_METAL3)  )
        # ABLB layer on pads
        metalPad=gdspy.Path( padSize ,(metalLine.x,metalLine.y-metalLineWidth/2))
        metalPad.segment(padSize ,direction='+y', **ld_ABLB)
        Heatercell.add(metalPad)
        # silox opening on metal pads
        siloxPad = gdspy.offset(metalPad, -5, join_first=True, ** ld_Silox)
        Heatercell.add(siloxPad)


        Ringcell.add(gdspy.CellReference(Heatercell))
        # mirror HACK
        Ringcell.add(gdspy.CellReference(Heatercell,x_reflection = True,rotation =180,origin = ((-my_length/2+Taper_length+Basic_Straight_step)*2+Basic_Straight_step*(i)*2,0)))



    return Ringcell



for k  in range(0,2):
    
    Width_Waveguide = Width_WG[k]
    
    for j in range(0,2):
        print(j)
        Radius = Rad[j]
        Basic_Straight_step = 4*Radius + Spacing_Ring_Waveguide + Spacing_Ring_Waveguide
        if Radius==50:
             Basic_Straight_step = 6*Radius + Spacing_Ring_Waveguide + Spacing_Ring_Waveguide

        diss_in_bunches  = 50 + 2*Radius + 8*Spacing_between_Straight 
    
        diss_for_k = 50+diss_in_bunches + 0*Rad[0] +0*Rad[1] + 16*Spacing_between_Straight
        
        cellname=Ring(cellname="ring"+str(k)+str(j),Width_Waveguide=Width_Waveguide,gap_array=gap,Radius=Radius,Basic_Straight_step=Basic_Straight_step)      
        top_cell.add(gdspy.CellReference(cellname, (-200,-350 -diss_in_bunches*j - diss_for_k * k)))


## draw RaceTrack

RaceTrackcell = lib.new_cell('RacecTrack')


Coupling_r=15
Coupling_length=20


racetrack_length=100


for i in range(0,9):
    path1 = gdspy.Path(Taper_Width , (-my_length/2 , my_height/2 - Spacing_between_Straight*(i) ))

    path3 = gdspy.Path(3 , (-my_length/2 , my_height/2 - Spacing_between_Straight*(i) ))
    path3.segment(length=Taper_length,direction= "+x" ,** ld_taperMark)

    path1.segment(length=Taper_length,direction= "+x",final_width= Width_Waveguide ,** ld_NWG)
    path1.segment(Basic_Straight_step*(i+1),"+x",** ld_NWG)
    path1.turn(Radius,angle=a2r(Coupling_r) ,** ld_NWG)
    path1.turn(Radius,angle=a2r(-Coupling_r) ,** ld_NWG)
    path1.segment(Coupling_length/2,"+x",** ld_NWG)
    x = path1.x
    y = path1.y
    path1.segment(Coupling_length/2,"+x",** ld_NWG)
    path1.turn(Radius,angle=a2r(-Coupling_r) ,** ld_NWG)
    path1.turn(Radius,angle=a2r(Coupling_r) ,** ld_NWG)
    path1.segment(Radius,"+x",** ld_NWG)
    path1.segment(Spacing_Ring_Waveguide,"+x",** ld_NWG)
    path1.turn(Radius,"l",** ld_NWG)
    path1.segment(height_in_S,"+y",** ld_NWG)
    path1.turn(Radius,"r",** ld_NWG)
    path1.segment(my_length - Basic_Straight_step*(i+1) - 3*Radius - Spacing_Ring_Waveguide - 124   ,"+x",** ld_NWG)
    xT = path1.x
    yT = path1.y
    path1.segment(length=Taper_length,direction= "+x",final_width= Taper_Width,** ld_NWG)

    
    path2 = gdspy.Path(Width_Waveguide,(x+racetrack_length/2,y+gap[i]+ 0.05 + Width_Waveguide))
    path2.turn(Radius,"ll",** ld_NWG)
    path2.segment(racetrack_length,"-x",** ld_NWG)
    path2.turn(Radius,"ll",** ld_NWG)
    path2.segment(racetrack_length,"+x",** ld_NWG)
    RaceTrackcell.add(path2)
    
    
    path4 = gdspy.Path(3,(xT,yT))
    path4.segment(length=Taper_length,direction= "+x" ,** ld_taperMark)


    RaceTrackcell.add(path1)
    RaceTrackcell.add(path2)
    RaceTrackcell.add(path3)
    RaceTrackcell.add(path4)







    
#draw chip boundaries
chip= gdspy.Rectangle((chip_X0, chip_Y0), (chip_length+chip_X0,Chip_Height+chip_Y0 ), **ld_dataExtend)
top_cell.add(chip)

borderL= gdspy.Rectangle((chip_X0, chip_Y0-SUS_width),(chip_X0-SUS_spacing - SUS_width, Chip_Height+chip_Y0+SUS_width), **ld_SUS)
borderR= gdspy.Rectangle((chip_length+chip_X0, chip_Y0-SUS_width),(chip_length+chip_X0+SUS_spacing + SUS_width, Chip_Height+chip_Y0+SUS_width), **ld_SUS)

VGL= gdspy.Rectangle((chip_X0-VG_spacing , chip_Y0-VG_width),(chip_X0 - VG_width, Chip_Height+chip_Y0+VG_width), **ld_VG1)
VGR= gdspy.Rectangle((chip_length+chip_X0+VG_spacing , chip_Y0-VG_width),
    (chip_length+chip_X0+VG_width, Chip_Height+chip_Y0+VG_width), **ld_VG1)

top_cell.add([ borderR,borderL,VGL,VGR ])


# add spiral
lib.read_gds('spiral_test_02_flattened.gds')
spiral=lib.extract('spiral')
top_cell.add(gdspy.CellReference(spiral, (-2497.00000, -10298.00000)))

# add MZI
lib.read_gds('MZI_MMI.gds')
MMI=lib.extract('MZI_MMI')
top_cell.add(gdspy.CellReference(MMI, (2097.00000, -500)))
# add GC
lib.read_gds('GC_01.gds')
GC=lib.extract('GC')
top_cell.add(gdspy.CellReference(GC, (-2450.00000, -1700.00000)))


top_cell.add(gdspy.CellReference(RaceTrackcell, (-200,-2750+350)))

exportname="tower_chip"
# lib.write_gds('Rings.gds')
    
lib.write_gds(exportname+'.gds')
# faltten_cell=top_cell.flatten()
# lib.write_gds(exportname+'_flattened.gds', cells=[faltten_cell])    
    
    

    
    
    
    


 
