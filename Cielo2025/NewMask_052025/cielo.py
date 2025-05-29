import numpy as np
import gdspy


from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath

# layers definition
ld_LN = {"layer": 32, "datatype": 0}
ld_Metal = {"layer": 29, "datatype": 0}
ld_SU8 = {"layer": 50, "datatype": 0}

## Global variables
cell_width=2100
cell_height=20010
shift_x=400
shift_center_n=10
dicing_line_width=350
dicing_wafer_offset=1500
### 
# Create cell aray - (x,y) position of the cells
cells=np.zeros((shift_center_n*2*2,2))





# Load Main Mask
lib = gdspy.GdsLibrary()

wafer_radius=0.5*3*2.54*10000-100
fp = FontProperties(family="serif", style="normal")

lib.read_gds('cielo_template_v.2025.01.GDS')
top_cell=lib.cells['TOP']
num_cell = lib.cells['WG$numbers']
dicing_cell = lib.cells['Dicing']
cieloLogo = lib.cells['CIELO']
ELOPLogo = lib.cells['ELOP']
BIULogo = lib.cells['BIU']





def render_text(text, size=None, position=(0, 0), font_prop=None, tolerance=0.1):
    path = TextPath(position, text, size=size, prop=font_prop)
    polys = []
    xmax = position[0]
    for points, code in path.iter_segments():
        if code == path.MOVETO:
            c = gdspy.Curve(*points, tolerance=tolerance)
        elif code == path.LINETO:
            c.L(*points)
        elif code == path.CURVE3:
            c.Q(*points)
        elif code == path.CURVE4:
            c.C(*points)
        elif code == path.CLOSEPOLY:
            poly = c.get_points()
            if poly.size > 0:
                if poly[:, 0].min() < xmax:
                    i = len(polys) - 1
                    while i >= 0:
                        if gdspy.inside(
                            poly[:1], [polys[i]], precision=0.1 * tolerance
                        )[0]:
                            p = polys.pop(i)
                            poly = gdspy.boolean(
                                [p],
                                [poly],
                                "xor",
                                precision=0.1 * tolerance,
                                max_points=0,
                            ).polygons[0]
                            break
                        elif gdspy.inside(
                            polys[i][:1], [poly], precision=0.1 * tolerance
                        )[0]:
                            p = polys.pop(i)
                            poly = gdspy.boolean(
                                [p],
                                [poly],
                                "xor",
                                precision=0.1 * tolerance,
                                max_points=0,
                            ).polygons[0]
                        i -= 1
                xmax = max(xmax, poly[:, 0].max())
                polys.append(poly)
    return polys


def Create_wafer_map():
    ####
    # Add dicing mark to Dicing Cell
 
    ## x lines
    ii=0
    for n in range(-shift_center_n,shift_center_n):
        dicing_x=n*cell_width+shift_x
        dicing_y=np.sqrt((wafer_radius-dicing_wafer_offset)**2-dicing_x**2)
        path1 = gdspy.FlexPath(width=dicing_line_width ,points= ((dicing_x,dicing_y),(dicing_x,-dicing_y)) , gdsii_path =True,**ld_SU8)    
        dicing_cell.add([path1])
        cells[ii+shift_center_n*2,0]=dicing_x
        cells[ii+shift_center_n*2,1]=-cell_height/2
        cells[ii,0]=dicing_x
        cells[ii,1]=-cell_height*3/2
        ii+=1
    # last right line
    dicing_x=(n+1)*cell_width+shift_x
    dicing_y=np.sqrt((wafer_radius-dicing_wafer_offset)**2-dicing_x**2)
    path1 = gdspy.FlexPath(width=dicing_line_width ,points= ((dicing_x,dicing_y),(dicing_x,-dicing_y)) , gdsii_path =True,**ld_SU8)    
    dicing_cell.add([path1])




    ## y lines
    for n in [-3,-1,3]:
        dicing_y=n*cell_height/2
        dicing_x=np.sqrt((wafer_radius-dicing_wafer_offset)**2-dicing_y**2)
        path1 = gdspy.FlexPath(width=dicing_line_width ,points= ((-dicing_x,dicing_y),(dicing_x,dicing_y)) , gdsii_path =True,**ld_SU8)    
        dicing_cell.add([path1])  

    ## add dicing mark - metal layer 
    dice_mark_cell= lib.new_cell('dice mark')
    path1 = gdspy.FlexPath(width=20 ,points= ((0,115),(0,0),(115,0)) , gdsii_path =True,**ld_Metal)    
    dice_mark_cell.add(path1)
    for n in range(0,np.shape(cells)[0]):
        cell_height_true=cell_height*(1+ (n>19) )
        dicing_cell.add(gdspy.CellReference(dice_mark_cell, (cells[n,0]+dicing_line_width/2+30,cells[n,1]+dicing_line_width/2+30)))
        dicing_cell.add(gdspy.CellReference(dice_mark_cell,  (cells[n,0]+  cell_width - (dicing_line_width/2+30),
            cells[n,1] +dicing_line_width/2+30), rotation = 90))
        dicing_cell.add(gdspy.CellReference(dice_mark_cell,  (cells[n,0]+(dicing_line_width/2+30),
            cells[n,1]+ cell_height_true -(dicing_line_width/2+30)), rotation = 270))
        dicing_cell.add(gdspy.CellReference(dice_mark_cell,  (cells[n,0]+  cell_width - (dicing_line_width/2+30),
            cells[n,1]+ cell_height_true -(dicing_line_width/2+30)), rotation =180))

        x,y=cells[n,0]+dicing_line_width/2+300,cells[n,1]+dicing_line_width/2+1500
        arc = gdspy.Round((x,y),radius=150,inner_radius=150-7,number_of_points =100,**ld_LN)
        arc1 = gdspy.Round((x,y),radius=150,inner_radius=150-7,number_of_points =100,**ld_Metal)
        # # text = gdspy.Text(str(n),150, (x-100,y-100), **ld_Metal)
        # text1 = gdspy.Text(str(n),150, (x-100,y-100), **ld_LN)
        text = gdspy.PolygonSet(render_text(str(n).zfill(2),size=200,position=(x-100-27,y-100+30) , font_prop=fp),**ld_Metal )
        text1 = gdspy.PolygonSet(render_text(str(n).zfill(2),size=200,position=(x-100-27,y-100+30) , font_prop=fp),**ld_LN )

        num_cell.add([arc,text,arc1,text1])

        
    # Logos
        if (n+1) in[1,2,5,6,7,8,9,10,11,12,30,31,32,33,34,35]:
            dicing_cell.add(gdspy.CellReference(cieloLogo,  (cells[n,0]+400,
                cells[n,1]+3000),magnification=4,rotation =90))
            dicing_cell.add(gdspy.CellReference(cieloLogo,  (cells[n,0]+400,
                cells[n,1]+cell_height_true-1500),magnification=4,rotation =90))

        if (n+1) in[3,4,21,22,23,24,25,26,27,28,29,36,37,38]:
            dicing_cell.add(gdspy.CellReference(ELOPLogo,  (cells[n,0]+400,
                cells[n,1]+3000),magnification=4,rotation =90))
            dicing_cell.add(gdspy.CellReference(ELOPLogo,  (cells[n,0]+400,
                cells[n,1]+cell_height_true-1500),magnification=4,rotation =90))

        dicing_cell.add(gdspy.CellReference(BIULogo,  (cells[n,0]+550,
            cells[n,1]+3900),magnification=0.03,rotation =90))
















# global constants
Width_WG = 5
diss_to_metal = 4.75
Metal_width = 15

gap = 700

arrow_diss_down = 100
arrow_mid_height = 355
arrow_diss_sides = 100
arrow_top_height = 150
diss_arrow_from_wg = 200

tri_width = 75
tri_height = 160
tri_diss_from_wg = 50

sign_width = 20
sign_height = 130
sign_bottom = 130
sign_diss_from_wg = 720

holes_width = 280
holes_height = 1300
diss_holes_wg = 51
pads_w=280
pads_l=1300



# S bend path
def sbendPath(wgsbend,L=100,H=50,info = ld_LN):
# the formula for cosine-shaped s-bend is: y(x) = H/2 * [1- cos(xpi/L)]
# the formula for sine-shaped s-bend is: y(x) = xH/L - H/(2pi) * sin(x2*pi/L)
    def sbend(t):
        x = H/2 * (1- np.cos(t*np.pi))
        y =L*t
        
        return (x,y)
    
    def dtsbend(t):
        dx_dt = H/2*np.pi*np.sin(t*np.pi)
        dy_dt = L

        return (dx_dt,dy_dt)

    wgsbend.parametric(sbend ,dtsbend , number_of_evaluations=100,**info)  
    return wgsbend   
 
def sbendPathM(wgsbend,L=100,H=50,info = ld_LN):

    def sbend(t):
        x = H/2 * (np.cos(t*np.pi))
        y = L*t
        
        return (x,y)
    
    def dtsbend(t):
        dx_dt =  -H/2*np.pi*np.sin(t*np.pi)
        dy_dt = L

        return (dx_dt,dy_dt )

    wgsbend.parametric(sbend ,dtsbend , number_of_evaluations=100,**info)  
    return wgsbend    
    
# deg tor radian
def a2r(ang):  # angle to radian
    return np.pi/180*ang

# draw straigh waveguide with phase shifters
def cielo_wg (cell,wg_length = 1580 , el_length = 426 , el_gap = 6 , el_width = 10498  , Width_WG = Width_WG , x = 0 , y = 0):
    # draw wg
    path1 = gdspy.Path(width=Width_WG ,initial_point=(x,y))    
    path1.segment(wg_length,"+y" ,**ld_LN )
    # draw electrodes
    path2 = gdspy.Path(width=el_width ,initial_point=(x +  (el_gap+el_width)/2,y+(wg_length-el_length)/2))
    path2.segment(el_length,"+y" ,**ld_Metal )
    path3 = gdspy.Path(width=el_width ,initial_point=(x -  (el_gap+el_width)/2,y+(wg_length-el_length)/2))
    path3.segment(el_length,"+y" ,**ld_Metal )
    path2.fillet(el_width*0.25)
    path3.fillet(el_width*0.25)   
    
    # added triangles marks at begening and end
    points = [(x - tri_diss_from_wg , y + 500),(x - tri_diss_from_wg , y + 500 + tri_height),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)

    points = [(x - tri_diss_from_wg , y + 500 +  tri_height),(x - tri_diss_from_wg , y + 500 + tri_height*2),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)

    points = [(x- tri_diss_from_wg , y + 19000),(x  - tri_diss_from_wg , y + 19000 + tri_height),(x  - tri_diss_from_wg - tri_width , y + 19000 + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)

    points = [(x - tri_diss_from_wg , y + 19000 +  tri_height),(x  - tri_diss_from_wg , y + 19000 + tri_height*2),(x  - tri_diss_from_wg - tri_width , y + 19000 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)


 # draw 2 pads in SU8
    if pads_w < el_width:
        pads_xr,pads_yr=x +  (el_gap+el_width)/2 , y+(wg_length-pads_l)/2                                              
        pads_xl,pads_yl=x -  (el_gap+el_width)/2 , y+(wg_length-pads_l)/2+pads_l*2
    else:             # contact widths thinner that electrodes => draw metalic contacts                                     
        pads_xr,pads_yr=x +  (el_gap+el_width+pads_w)/2 , y+(wg_length-pads_l)/2                                              
        pads_xl,pads_yl=x -  (el_gap+el_width+pads_w)/2 , y+(wg_length-pads_l)/2+pads_l*2
        path6 = gdspy.Path(width=pads_w-10 ,initial_point=(pads_xr,pads_yr+5))    
        path6.segment(pads_l-10,"+y" ,**ld_Metal)
        path7 = gdspy.Path(width=pads_w-10 ,initial_point=(pads_xl,pads_yl+5))    
        path7.segment(pads_l-10,"+y" ,**ld_Metal )
        path7.fillet(pads_w*0.25)
        path6.fillet(pads_w*0.25)
        cell.add([path6,path7])
   
    path4 = gdspy.Path(width=pads_w ,initial_point=(pads_xr,pads_yr))    
    path4.segment(pads_l,"+y" ,**ld_SU8 )
    path5 = gdspy.Path(width=pads_w ,initial_point=(pads_xl,pads_yl))    
    path5.segment(pads_l,"+y" ,**ld_SU8 )
 
    path4.fillet(pads_w*0.25)
    path5.fillet(pads_w*0.25)
    
    cell.add([path1,path2,path3,path4,path5])
    y+=1000
    #create the arrow sign
    points = [( x - diss_arrow_from_wg , y + 500 ),(x - diss_arrow_from_wg - arrow_diss_down , y + 500)
              ,(x - diss_arrow_from_wg - arrow_diss_down , y + 500 + arrow_mid_height)
              ,(x - diss_arrow_from_wg - arrow_diss_down - arrow_diss_sides , y + 500 + arrow_mid_height)
              ,( x - diss_arrow_from_wg - arrow_diss_down/2 , y + 500 + arrow_mid_height + arrow_top_height)
              ,(x - diss_arrow_from_wg + arrow_diss_sides , y + 500 + arrow_mid_height)
              ,(x - diss_arrow_from_wg , y + 500 + arrow_mid_height)]
    arrow = gdspy.Polygon(points,**ld_LN)
    arrowM = gdspy.Polygon(points,**ld_Metal)
    cell.add(arrow)
    cell.add(arrowM)


