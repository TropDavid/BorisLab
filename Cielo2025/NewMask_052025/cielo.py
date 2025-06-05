import numpy as np
import gdspy
import uuid


from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath

# layers definition
ld_LN = {"layer": 32, "datatype": 0}
ld_Metal = {"layer": 29, "datatype": 0}
ld_SU8 = {"layer": 50, "datatype": 0}
ld_METAL2 = {"layer": 29, "datatype": 0}
ld_NWG = {"layer": 32, "datatype": 0}
ld_Silox = {"layer": 50, "datatype": 0}

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


## create arrow
arrow_cell =lib.new_cell('ARROW')

def Arrow(cell,x=0,y=0):
    arrow_diss_down = 100
    arrow_mid_height = 355
    arrow_diss_sides = 50
    arrow_top_height = 250
    diss_arrow_from_wg = 200
    
    #create the arrow sign
    points = [( x - diss_arrow_from_wg , y + 500 ),(x - diss_arrow_from_wg - arrow_diss_down , y + 500)
              ,(x - diss_arrow_from_wg - arrow_diss_down , y + 500 + arrow_mid_height)
              ,(x - diss_arrow_from_wg - arrow_diss_down - arrow_diss_sides , y + 500 + arrow_mid_height)
              ,( x - diss_arrow_from_wg - arrow_diss_down/2 , y + 500 + arrow_mid_height + arrow_top_height)
              ,(x - diss_arrow_from_wg + arrow_diss_sides , y + 500 + arrow_mid_height)
              ,(x - diss_arrow_from_wg , y + 500 + arrow_mid_height)]
    arrowM = gdspy.Polygon(points,**ld_Metal)
    cell.add(arrowM)
    
Arrow(arrow_cell,0,0)


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

        x,y=cells[n,0]+dicing_line_width/2+200-40,cells[n,1]+dicing_line_width/2+1500
        arc = gdspy.Round((x,y),radius=150,inner_radius=150-7,number_of_points =100,**ld_LN)
        arc1 = gdspy.Round((x,y),radius=150,inner_radius=150-7,number_of_points =100,**ld_Metal)
        arc2 = gdspy.Round((x,y+cell_height_true-4500),radius=150,inner_radius=150-7,number_of_points =100,**ld_Metal)

        # # text = gdspy.Text(str(n),150, (x-100,y-100), **ld_Metal)
        # text1 = gdspy.Text(str(n),150, (x-100,y-100), **ld_LN)
        text = gdspy.PolygonSet(render_text(str(n+1).zfill(2),size=200,position=(x-100-27,y-100+30) , font_prop=fp),**ld_Metal )
        # text1 = gdspy.PolygonSet(render_text(str(n).zfill(2),size=200,position=(x-100-27,y-100+30) , font_prop=fp),**ld_LN )
        text2 = gdspy.PolygonSet(render_text(str(n+1).zfill(2),size=200,position=(x-100-27,y-100+30+cell_height_true-4500) , font_prop=fp),**ld_Metal )

        num_cell.add([arc,text,arc1,text2,arc2])
        if n <20:
            num_cell.add(gdspy.CellArray(arrow_cell,1,5,(0,4600),  (x+270,y-1500) ))
        else:
            num_cell.add(gdspy.CellArray(arrow_cell,1,4,(0,4600*2),  (x+270,y-1500) ))

    # Logos
        if (n+1) in[1,2,5,6,7,8,9,10,11,12]:
            dicing_cell.add(gdspy.CellReference(cieloLogo,  (cells[n,0]+400,
                cells[n,1]+3000),magnification=4,rotation =90))
            dicing_cell.add(gdspy.CellReference(cieloLogo,  (cells[n,0]+400,
                cells[n,1]+cell_height_true-1500),magnification=4,rotation =90))

        if (n+1) in[3,4,21,22]:
            dicing_cell.add(gdspy.CellReference(ELOPLogo,  (cells[n,0]+400,
                cells[n,1]+3000),magnification=4,rotation =90))
            dicing_cell.add(gdspy.CellReference(ELOPLogo,  (cells[n,0]+400,
                cells[n,1]+cell_height_true-1500),magnification=4,rotation =90))

        dicing_cell.add(gdspy.CellReference(BIULogo,  (cells[n,0]+500,
            cells[n,1]+1900),magnification=0.03,rotation =90))



Width_WG = 5
diss_bet_El = 17
diss_to_metal = (diss_bet_El - Width_WG)/2


length_WG = 20010
Metal_width = 20
Metal_length = 19000
holes_width = 280
holes_height = 1300
diss_holes_wg = 51

holes_widthS = 200
holes_heightS = 1300

pads_w=280
pads_l=1300


gap = 700

## create pad
pad_cell =lib.new_cell('PAD')
rec = gdspy.Rectangle((-holes_width/2 ,-holes_height/2)
                        ,(holes_width/2,holes_height/2), **ld_SU8)
rect = rec.fillet(50)
pad_cell.add(rect)
rect = gdspy.Rectangle((-holes_width/2-15 ,-holes_height/2-15), (holes_width/2+30,holes_height/2+15),**ld_Metal)
pad_cell.add(rect)


## create small pad sPAD
s_pad_cell =lib.new_cell('sPAD')
rec = gdspy.Rectangle((-holes_widthS/2 ,-holes_heightS/2)
                        ,(holes_widthS/2,holes_heightS/2), **ld_SU8)
rect = rec.fillet(50)
s_pad_cell.add(rect)
rect = gdspy.Rectangle((-holes_widthS/2-15 ,-holes_heightS/2-15), (holes_widthS/2+30,holes_heightS/2+15),**ld_Metal)
s_pad_cell.add(rect)



def sbendPath(wgsbend,L=100,H=50,info = ld_NWG):
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
 

def sbendPathM(wgsbend,L=100,H=50,info = ld_NWG):

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
    

def a2r(ang):  # angle to radian
    return np.pi/180*ang


def Tri(cell,x = 0,y = 0):
    
    tri_width = 75
    tri_height = 160
    tri_diss_from_wg = 50
    
    points = [(x - tri_diss_from_wg , y + 500),(x - tri_diss_from_wg , y + 500 + tri_height),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
    tri = gdspy.Polygon(points , **ld_METAL2)
    cell.add(tri)

    points = [(x - tri_diss_from_wg , y + 500 +  tri_height),(x - tri_diss_from_wg , y + 500 + tri_height*2),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_METAL2)
    cell.add(tri)

    
def PadLeft(cell,x,y):
    rec = gdspy.Rectangle((x - diss_holes_wg - Width_WG/2 - diss_to_metal , y + 1000 - holes_height /2)
                          ,(x - diss_holes_wg - holes_width - Width_WG/2 - diss_to_metal , y + 1000 + holes_height /2), **ld_SU8)
    rect = rec.fillet(50)
    cell.add(rect)
    

    
    rect = gdspy.Rectangle((x - Width_WG/2 - diss_to_metal , y + 1000 - holes_height/2 - 15), (x - diss_holes_wg - holes_width - Width_WG/2 - diss_to_metal  - 15 , y + 1000 + holes_height/2 + 15),**ld_Metal)
    cell.add(rect)

def PadRight(cell,x,y):
    # rec = gdspy.Rectangle((x + Width_WG/2 + diss_to_metal + diss_holes_wg ,y + 1000 - holes_height /2 +15)
    #                       ,(x + Width_WG/2 + diss_to_metal + diss_holes_wg + holes_width , y + 1000 + holes_height /2 - 15), **ld_SU8)
    # rect = rec.fillet(50)
    # cell.add(rect)
    
    rec = gdspy.Rectangle((x + Width_WG/2 + diss_to_metal + diss_holes_wg - 15 , y + 1000 - holes_height /2)
                          ,(x + Width_WG/2 + diss_to_metal + diss_holes_wg + holes_width , y + 1000 + holes_height /2), **ld_SU8)
    rect = rec.fillet(50)
    cell.add(rect)
    
    rect = gdspy.Rectangle((x + Width_WG/2 + diss_to_metal , y + 1000 - holes_height/2 - 15), (x + diss_holes_wg + holes_width + Width_WG/2 + diss_to_metal  + 15 , y + 1000 + holes_height/2 + 15),**ld_Metal)
    cell.add(rect)


def Straigh (cell,Width_WG = Width_WG,x = 0,y = 0,length_WG = length_WG , el_gap = 2,
             el_width=10 , El_length = Metal_length,y_pads_shift=0
             ):
    diss_to_metal = (el_gap - Width_WG)/2

    Tri(cell,x,y)
    # Tri(x,y + length_WG - 1000)
    
    #the start of the WG
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = length_WG , direction ="+y" , **ld_NWG)
    
    Tri(cell,path1.x,path1.y - 1500)
    el_width=el_width+el_gap/2
    mid = gdspy.offset(path1 , diss_to_metal , join_first = True ,**ld_Silox)
    rect = gdspy.Rectangle((x - el_width , y + 500), (x + el_width , y + 500 + El_length), **ld_METAL2)
    stam = gdspy.boolean(rect,mid,"not",**ld_METAL2)
    
    cell.add(gdspy.CellReference(pad_cell,(path1.x-holes_width/2-el_gap/2-30
                                           , path1.y/2+y_pads_shift)))

    cell.add(gdspy.CellReference(pad_cell,(path1.x+holes_width/2+el_gap/2+30
                                           , path1.y/2+y_pads_shift),rotation=180))
    text = gdspy.PolygonSet(render_text('wg='+str(Width_WG)+'\u03bcm, el_gap'+ str(el_gap)+'\u03bcm' ,size=100,position=(0,0) , font_prop=fp),**ld_Metal )
    txt_cell =lib.new_cell(str(uuid.uuid1()))
    txt_cell.add(text)
    cell.add(gdspy.CellReference(txt_cell,(x+150+60,y+800),rotation=90))
    cell.add(gdspy.CellReference(txt_cell,(x+150+60,y-1900+length_WG),rotation=90))

    cell.add(path1)
    cell.add(stam)

def y_split_block(cell,x,y,B_length,A_length,Brad_length,Brad,S_length,S_height,S_heigth_top):
#the start of the WG
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = B_length , direction ="+y" , **ld_LN)
    path1.segment(length = Brad_length , direction ="+y" , final_width = Width_WG + Brad , **ld_LN)    
    x = path1.x
    y = path1.y    
    # creating the half circle in the Branch of Y-splitter
    rect = gdspy.Rectangle((x + Brad/2 + Width_WG/2, y), (x - Brad/2 - Width_WG /2 ,y + 1  ),**ld_LN)
    circle = gdspy.Round((x, y + 1 ), 0.5 ,initial_angle = np.pi , final_angle = 2*np.pi ,**ld_LN ,tolerance = 0.00001 , number_of_points = 199)
    stam = gdspy.boolean(rect,circle,"not",**ld_LN)
    cell.add(stam)    
    #creating the right arm 
    path2 = gdspy.Path(width = Width_WG ,initial_point = (path1.x + Brad/2,path1.y + 0.5 ))
    path2 = sbendPath(wgsbend = path2 , L = S_length , H = S_heigth_top , info = ld_LN)
    y_o = path2.y
    path2.segment(length = A_length , direction ="+y" , **ld_LN)
    #creating the left arm
    path3 = gdspy.Path(width = Width_WG ,initial_point = ( path1.x - Brad/2 , path1.y + 0.5 ))
    path3.x = path3.x - S_height/2
    path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_LN)
    path3.segment(length = A_length , direction ="+y" , **ld_LN)
    cell.add([path1,path2,path3])

    return [path2,path3,y_o]


def Y_splitter (cell,B_length = 100 , Brad_length = 600 , Brad = 6 , A_length = 20010 - 700 - 4500  , S_length = 4500 , S_height = 204 
                    , S_heigth_top = 190 , Width_WG = Width_WG , x = 0 , y = 0 , el_width = Metal_width , el_gap=17 
                    ,y_pads_shift=1400, El_length = 14410,M=1):
        
    diss_to_metal = (el_gap - Width_WG)/2

    Tri(cell,x,y)
    # yspliter block
    [path2,path3,y_o]=y_split_block(cell,x,y,B_length,A_length,Brad_length,Brad,S_length,S_height,S_heigth_top)


    
    if(M==1):
    
        #pad to the right of the right arm
        cell.add(gdspy.CellReference(s_pad_cell,(path2.x-holes_widthS/2-el_gap/2-30
                                    , path2.y/2+y_pads_shift)))

        cell.add(gdspy.CellReference(s_pad_cell,(path2.x+holes_widthS/2+el_gap/2+30
                                        , path2.y/2+y_pads_shift),rotation=180))
    ##small peds to - left branch
        cell.add(gdspy.CellReference(s_pad_cell,(path3.x-holes_widthS/2-el_gap/2-30
                            , path3.y/2-y_pads_shift)))
        cell.add(gdspy.CellReference(s_pad_cell,(path3.x+holes_widthS/2+el_gap/2+30
                                        , path3.y/2-y_pads_shift),rotation=180))

        #creating the contact
        mid = gdspy.offset([path3,path2] , diss_to_metal , join_first = True ,**ld_SU8)
        rect = gdspy.Rectangle((x - 600 , y_o), (x + 600 , y_o + El_length), **ld_Metal)
        stam = gdspy.boolean(rect,mid,"not",**ld_Metal)
        
        mid = gdspy.offset([path3,path2] , diss_to_metal + el_width  , join_first = True ,**ld_SU8)
        rect = gdspy.Rectangle((x - 600 , y_o ), (x + 600 , y_o+El_length ), **ld_Metal)
        stam2 = gdspy.boolean(rect,mid,"not",**ld_Metal)
    
        stam = gdspy.boolean(stam,stam2,"not",**ld_Metal)
        cell.add(stam)


  
   
    # sign at the top
    Tri(cell,path3.x,path3.y - 1500)
    
    Tri(cell,path2.x,path2.y - 1500)

    ## add TEXT
    text = gdspy.PolygonSet(render_text('wg='+str(Width_WG)+'\u03bcm, el_gap'+ str(el_gap)+'\u03bcm' ,size=100,position=(0,0) , font_prop=fp),**ld_Metal )
    txt_cell =lib.new_cell(str(uuid.uuid1()))
    txt_cell.add(text)
    cell.add(gdspy.CellReference(txt_cell,(x+150+60,y+200),rotation=90))
    cell.add(gdspy.CellReference(txt_cell,(x+150+60-230,y+A_length+1200),rotation=90)) 


    return([path2.x , path2.y , path3.x , path3.y])

def MZ (cell,B_length = 100 , Brad_length = 400 , Brad = 6 , A_length = 20005 - 5002.5  , S_length = 4502.5 , S_height = 204  
                 , S_heigth_top = 190 ,Width_WG = Width_WG , x = 0 , y = 0 , el_width = Metal_width , el_gap=17 , El_length = 14000,left_right=0):

    diss_to_metal = (el_gap - Width_WG)/2

    Tri(cell,x,y)

    
    #the start of the WG
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = B_length , direction ="+y" , **ld_LN)
    path1.segment(length = Brad_length , direction ="+y" , final_width = Width_WG + Brad , **ld_LN)
    
    y_o =y-800
    x = path1.x
    y = path1.y
    
    # creating the half circle in the Branch of Y-splitter
    rect = gdspy.Rectangle((x + Brad/2 + Width_WG/2, y), (x - Brad/2 - Width_WG /2 ,y + 1  ),**ld_LN)
    circle = gdspy.Round((x, y + 1 ), 0.5 ,initial_angle = np.pi , final_angle = 2*np.pi ,**ld_LN ,tolerance = 0.00001 , number_of_points = 199)
    stam = gdspy.boolean(rect,circle,"not",**ld_LN)
    cell.add(stam)
    
    
    #creating the right arm 
    path2 = gdspy.Path(width = Width_WG ,initial_point = (path1.x + Brad/2,path1.y + 0.5 ))
    path2 = sbendPath(wgsbend = path2 , L = S_length , H = S_heigth_top , info = ld_LN)
    path2.segment(length = A_length , direction ="+y" , **ld_LN)
    

    #creating the left arm
    path3 = gdspy.Path(width = Width_WG ,initial_point = ( path1.x - Brad/2 , path1.y + 0.5 ))
    path3.x = path3.x - S_height/2
    path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_LN)
   
    x3 = path3.x
    path3.segment(length = A_length , direction ="+y" , **ld_LN)
    
    
    cell.add([path1,path2,path3,stam])
    
    #making turn Y splitter to complete the MZ
    path1m = gdspy.copy(path1).mirror(p1 = (path2.x,path2.y),p2 = (path3.x ,path2.y))
    path2m = gdspy.copy(path2).mirror(p1 = (path2.x - 5,path2.y),p2 = (path2.x+5 ,path2.y))
    path3m = gdspy.copy(path3).mirror(p1 = (path3.x - 5,path3.y),p2 = (path3.x + 5 ,path3.y))
    stam1 = gdspy.copy(stam).mirror(p1 = (path2.x,path2.y),p2 = (path3.x ,path2.y))
    
    
    if (left_right!=5):
        #creating the contact
        mid = gdspy.offset([path3,path2] , diss_to_metal , join_first = True ,**ld_SU8)
        mid2 = gdspy.offset([path3m,path2m] , diss_to_metal  , join_first = True ,**ld_SU8)
        rect = gdspy.Rectangle((x - 600 , y_o + B_length+Brad_length+S_length), (x + 600 , y_o + B_length+Brad_length+S_length + El_length*2), **ld_Metal)
        stam = gdspy.boolean(rect,mid,"not",**ld_Metal)
        stam = gdspy.boolean(stam,mid2,"not",**ld_Metal)
        
        
        mid = gdspy.offset([path3,path2] , diss_to_metal + el_width  , join_first = True ,**ld_SU8)
        mid2 = gdspy.offset([path3m,path2m] , diss_to_metal + el_width  , join_first = True ,**ld_SU8)
        rect = gdspy.Rectangle((x - 600 , y_o + B_length+Brad_length+S_length), (x + 600 , y_o + B_length+Brad_length+S_length + El_length*2), **ld_Metal)
        stam2 = gdspy.boolean(rect,mid,"not",**ld_Metal)
        stam2 = gdspy.boolean(stam2,mid2,"not",**ld_Metal)
        
        if (El_length==7500):
            temp_y_shift=-6000
        else:
            temp_y_shift=-0

        stam = gdspy.boolean(stam,stam2,"not",**ld_Metal)
        if (left_right!=1):
            PadRight(cell, x = path2.x, y = path2.y+temp_y_shift)
        PadLeft(cell,path2.x,path2.y+temp_y_shift)
        if (left_right!=2):

            PadLeft(cell,path3.x,path3.y+temp_y_shift)
        rec = gdspy.Rectangle((path2.x - Width_WG/2 - diss_to_metal - 15 , path2.y + 1000 - holes_height/2 - 50+temp_y_shift) 
                            ,(path3.x + Width_WG/2 + diss_to_metal + 15 , path2.y + 1000 + holes_height/2 + 50+temp_y_shift)
                            , **ld_Metal)
        cell.add(rec)



        ##### create the common electrode 
        # r
        y_to_pads=-temp_y_shift
        if (left_right!=1):
            rec = gdspy.Rectangle((x3-el_gap/2 , path2.y + 1000 - y_to_pads - holes_height/2 - 50) 
                                ,(x3-(-el_gap/2+194) , path2.y + 1000 - y_to_pads + holes_height/2 + 50)
                                , **ld_Metal)  
            cell.add(rec)
            rec = gdspy.Rectangle((x3-el_gap/2-15 , path2.y + 1000 - y_to_pads - holes_height/2 - 50+15) 
                                ,(x3-(-el_gap/2+194-15) , path2.y + 1000 - y_to_pads + holes_height/2 + 50-15)
                                , **ld_SU8)  
            rect = rec.fillet(50)

            cell.add(rect)
    else:
        # Single Electrode 
        mid = gdspy.offset([path3,path2] , diss_to_metal , join_first = True ,**ld_SU8)
        mid2 = gdspy.offset([path3m,path2m] , diss_to_metal  , join_first = True ,**ld_SU8)
        rect = gdspy.Rectangle((x - 205 , y_o + B_length+Brad_length+S_length), (x + 00 , y_o + B_length+Brad_length+S_length + El_length*2), **ld_Metal)
        stam = gdspy.boolean(rect,mid,"not",**ld_Metal)
        

        stam = gdspy.boolean(stam,mid2,"not",**ld_Metal)
        
        
        mid = gdspy.offset([path3,path2] , diss_to_metal + el_width  , join_first = True ,**ld_SU8)
        mid2 = gdspy.offset([path3m,path2m] , diss_to_metal + el_width  , join_first = True ,**ld_SU8)
        rect = gdspy.Rectangle((x - 600 , y_o + B_length+Brad_length+S_length), (x + 600 , y_o + B_length+Brad_length+S_length + El_length*2), **ld_Metal)
        stam2 = gdspy.boolean(rect,mid,"not",**ld_Metal)
        stam2 = gdspy.boolean(stam2,mid2,"not",**ld_Metal)
        stam = gdspy.boolean(stam,stam2,"not",**ld_Metal)
        # cell.add([stam])

    cell.add([path1m,path2m,path3m,stam,stam1])

    if (El_length==7500):
        temp_y_shift=-6000
    else:
        temp_y_shift=-0


    # end single electrode

       ## add TEXT
    text = gdspy.PolygonSet(render_text('wg='+str(Width_WG)+'\u03bcm, el_gap'+ str(el_gap)+'\u03bcm' ,size=100,position=(0,0) , font_prop=fp),**ld_Metal )
    txt_cell =lib.new_cell(str(uuid.uuid1()))
    txt_cell.add(text)
    cell.add(gdspy.CellReference(txt_cell,(x+150+60,y+200),rotation=90))
    cell.add(gdspy.CellReference(txt_cell,(x+150+60-230,y+A_length*2+1200),rotation=90)) 
    
    
    
    
    
    # To add Pads in the design
    

    
def Splitter1X4 (cell,B_length_Y = 100 , Brad_length_Y = 300 , Brad_Y = 6 , A_length_Y = 100  , S_length_Y = 1500 , S_height_Y = 200 
                , S_heigth_top_Y = 200 , Width_WG = Width_WG , x = 0 , y = 0 , el_width = Metal_width , el_gap = 17):

    [pathr,pathl,y_o]=y_split_block(cell,x,y,B_length_Y,A_length_Y,Brad_length_Y,Brad_Y,S_length_Y*2,S_height_Y*2,S_heigth_top_Y*2)

    Y_splitter(cell = cell , B_length=B_length_Y,Brad_length=Brad_length_Y
            ,Brad=Brad_Y,A_length= 40020 - pathr.y - B_length_Y - Brad_length_Y - S_length_Y*2 ,S_length=S_length_Y*2,
            S_height=S_height_Y,S_heigth_top=S_heigth_top_Y,Width_WG=Width_WG ,x=pathr.x ,y=pathr.y
            ,el_width=el_width,el_gap=el_gap,El_length=40020 - pathr.y - B_length_Y - Brad_length_Y - S_length_Y*2 - 100 ,M=1)
    
    Y_splitter(cell = cell , B_length=B_length_Y,Brad_length=Brad_length_Y
            ,Brad=Brad_Y,A_length=40020 - pathl.y - B_length_Y - Brad_length_Y - S_length_Y*2 ,S_length=S_length_Y*2,
            S_height=S_height_Y,S_heigth_top=S_heigth_top_Y,Width_WG=Width_WG ,x=pathl.x ,y=pathl.y
            ,el_width=el_width,el_gap=el_gap,El_length=40020 - pathl.y - B_length_Y - Brad_length_Y - S_length_Y*2 - 100,M=1)

