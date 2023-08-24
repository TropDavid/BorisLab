import numpy as np
import gdspy

# layers definition
ld_LN = {"layer": 32, "datatype": 0}
ld_Metal = {"layer": 29, "datatype": 0}
ld_SU8 = {"layer": 50, "datatype": 0}

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


    return()
# draw opened Y - spliter new contact
def cielo_sbend (cell,B_length = 1580 , Brad_length = 426 , Brad = 6 , A_length = 10498 , S_length = 6833 , S_height = 210 
                 , S_heigth_top = 190 , Width_WG = Width_WG , x = 0 , y = 0 , Metal_width = Metal_width , diss_to_metal = diss_to_metal):
    
    path4 = gdspy.Path(width = Width_WG ,initial_point = (x +  gap,y))
    path4.segment(B_length + Brad_length + S_length + A_length + 501 + 173  ,"+y" ,**ld_LN )
    
    points = [(x - tri_diss_from_wg , y + 500),(x - tri_diss_from_wg , y + 500 + tri_height),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x - tri_diss_from_wg , y + 500 +  tri_height),(x - tri_diss_from_wg , y + 500 + tri_height*2),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x + gap - tri_diss_from_wg , y + 500),(x + gap - tri_diss_from_wg , y + 500 + tri_height),(x + gap - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x + gap - tri_diss_from_wg , y + 500 +  tri_height),(x + gap - tri_diss_from_wg , y + 500 + tri_height*2),(x + gap - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    #the start of the WG
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = B_length , direction ="+y" , **ld_LN)
    path1.segment(length = Brad_length , direction ="+y" , final_width = Width_WG + Brad , **ld_LN)
    
    
    x = path1.x
    y = path1.y
    
    rect = gdspy.Rectangle(( x + Brad/2 + Width_WG/2 , y ), ( x - Brad/2 - Width_WG /2 ,y + 1  ),**ld_LN)
    circle = gdspy.Round((x, y + 1 ), 0.5 ,initial_angle = np.pi , final_angle = 2*np.pi ,**ld_LN ,tolerance = 0.00001 , number_of_points = 199)
    stam = gdspy.boolean(rect,circle,"not",**ld_LN)
    cell.add(stam)
    
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
    
    
    #creating the right arm with the openings to the contacts
    path2 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x + Brad/2,path1.y + 0.5 ))
    path2 = sbendPath( wgsbend = path2 , L = S_length , H = S_heigth_top , info = ld_LN)
    
    rec = gdspy.Rectangle((path2.x - diss_holes_wg - Width_WG/2 - diss_to_metal , path2.y + 1000 - holes_height /2)
                          ,(path2.x - diss_holes_wg - holes_width - Width_WG/2 - diss_to_metal , path2.y + 1000 + holes_height /2), **ld_SU8)
    rect = rec.fillet(50)
    cell.add(rect)
    
    rec = gdspy.Rectangle((path2.x - diss_holes_wg - Width_WG/2 - diss_to_metal + 15 , path2.y + 1000 - holes_height /2 - 15)
                          ,(path2.x - diss_holes_wg - holes_width - Width_WG/2 - diss_to_metal  - 15, path2.y + 1000 + holes_height /2 + 15 ), **ld_Metal)
    rect = rec.fillet(50)
    cell.add(rect)
    
    
    
    x2 = path2.x
    y2 = path2.y
    
    
    
    path2.segment(length = A_length + 673 , direction ="+y" , **ld_LN)
    
    rec = gdspy.Rectangle((path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg , path2.y - 1000 - holes_height /2 +15)
                          ,(path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg + holes_width , path2.y - 1000 + holes_height /2 - 15), **ld_SU8)
    rect = rec.fillet(50)
    cell.add(rect)
    
    rec = gdspy.Rectangle((path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg - 15 , path2.y - 1000 - holes_height /2)
                          ,(path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg + holes_width + 15 , path2.y - 1000 + holes_height /2), **ld_Metal)
    rect = rec.fillet(50)
    cell.add(rect)
    
    rec = gdspy.Rectangle((path2.x + Width_WG/2 + diss_to_metal + 15 , path2.y - 1000)
                          , (path2.x + Width_WG/2 + diss_to_metal + 15 + diss_holes_wg - 15, path2.y - 1000 + 20)
                          ,**ld_Metal)
    cell.add(rec)
    
    
    #creating the left arm
    path3 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x - Brad/2 , path1.y + 0.5 ))
    path3.x = path3.x - S_height/2
    path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_LN)
    x3 = path3.x
    path3.segment(length = A_length + 673 , direction ="+y" , **ld_LN)
    
    rec = gdspy.Rectangle((x2 - Width_WG/2 - diss_to_metal - 15 , y2 + 1000) 
                          ,(x3 + Width_WG/2 + diss_to_metal + 15 , y2 + 1000 + 20)
                          , **ld_Metal)
    cell.add(rec)
    
    
    #creating the contact
    mid = gdspy.offset([path3,path2] , diss_to_metal , join_first = True ,**ld_SU8)
    rect = gdspy.Rectangle((x - 600 , y + S_length/2), (x + 600 , y + S_length + A_length), **ld_Metal)
    stam = gdspy.boolean(rect,mid,"not",**ld_Metal)
    
    mid = gdspy.offset([path3,path2] , diss_to_metal + Metal_width  , join_first = True ,**ld_SU8)
    rect = gdspy.Rectangle((x - 600 , y + S_length/2), (x + 600 , y + S_length + A_length), **ld_Metal)
    stam2 = gdspy.boolean(rect,mid,"not",**ld_Metal)
    
    stam = gdspy.boolean(stam,stam2,"not",**ld_Metal)
    
    place = stam.get_bounding_box()
    rightX = place[1,0]
    rightY = place[1,1]
    #leftX = place[0,0]
    
   
    
    path7=gdspy.Path(Metal_width ,(rightX - Metal_width/2 - (S_height + S_heigth_top + diss_to_metal*2 + Metal_width*2)/2 , rightY + 100))
    path7.segment((S_height + S_heigth_top + diss_to_metal*2 + Metal_width*2)/2 - 100  ,"+x",**ld_Metal)
    path7.turn(100,a2r(-90),**ld_Metal)
   
    
    path8=gdspy.Path(Metal_width ,(rightX - Metal_width/2 - (S_height + S_heigth_top + diss_to_metal*2 + Metal_width*2)/2 , rightY + 100))
    path8.segment((S_height + S_heigth_top + diss_to_metal*2 + Metal_width*2)/2 - 100  ,"+x",**ld_Metal)
    path8.turn(100,a2r(-90),**ld_Metal)
    path8.mirror((-10 , rightY)
                 ,((-10, rightY - 20)))
    
    
    
   
    # sign at the top
    x = path3.x
    y = path3.y - 523
    
    points = [(x - tri_diss_from_wg , y ),(x - tri_diss_from_wg , y + tri_height),(x - tri_diss_from_wg - tri_width , y  + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x - tri_diss_from_wg , y  +  tri_height),(x - tri_diss_from_wg , y  + tri_height*2),(x - tri_diss_from_wg - tri_width , y  + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    x = path2.x
    
    points = [(x  - tri_diss_from_wg , y ),(x  - tri_diss_from_wg , y  + tri_height),(x  - tri_diss_from_wg - tri_width , y  + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x  - tri_diss_from_wg , y  +  tri_height),(x  - tri_diss_from_wg , y  + tri_height*2),(x  - tri_diss_from_wg - tri_width , y  + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    x = path4.x
    
    points = [(x  - tri_diss_from_wg , y ),(x  - tri_diss_from_wg , y  + tri_height),(x  - tri_diss_from_wg - tri_width , y  + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x  - tri_diss_from_wg , y  +  tri_height),(x  - tri_diss_from_wg , y  + tri_height*2),(x  - tri_diss_from_wg - tri_width , y  + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)

    cell.add([path1,path2,path3,path4,path7,path8,stam])
  
    return([path2.x , path2.y , path3.x , path3.y])

def cielo_sbend_old (top_cell,B_length = 1580 , Brad_length = 426 , Brad = 6 , A_length = 10498 , S_length = 6833 , S_height = 210 
                     , S_heigth_top = 190 , Width_WG = Width_WG , x = 0 , y = 0, Metal_width = Metal_width , diss_to_metal = diss_to_metal):
    
    path4 = gdspy.Path(width = Width_WG ,initial_point = (x +  gap,y))
    path4.segment(B_length + Brad_length + S_length + A_length + 501 + 173  ,"+y" ,**ld_LN )
    
    
    """
    #sign at the begining
    points = [(x - sign_diss_from_wg , y + 50)
              ,(x - sign_diss_from_wg - sign_bottom , y + 50)
              ,(x - sign_diss_from_wg - sign_bottom , y + 50 + sign_height)
              ,(x - sign_diss_from_wg - sign_bottom + sign_width , y + 50 + sign_height)
              ,(x - sign_diss_from_wg - sign_bottom + 20 , y + 50 + sign_width)
              ,(x - sign_diss_from_wg , y + 50 + sign_width)]
    
   
    
    
    signM = gdspy.Polygon(points,**ld_METAL2)
    top_cell.add(signM)
    
    """
    
    
    points = [(x - tri_diss_from_wg , y + 500),(x - tri_diss_from_wg , y + 500 + tri_height),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    top_cell.add(tri)
    
    points = [(x - tri_diss_from_wg , y + 500 +  tri_height),(x - tri_diss_from_wg , y + 500 + tri_height*2),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    top_cell.add(tri)
    
    points = [(x + gap - tri_diss_from_wg , y + 500),(x + gap - tri_diss_from_wg , y + 500 + tri_height),(x + gap - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    top_cell.add(tri)
    
    points = [(x + gap - tri_diss_from_wg , y + 500 +  tri_height),(x + gap - tri_diss_from_wg , y + 500 + tri_height*2),(x + gap - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    top_cell.add(tri)
    
    #the start of the WG
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = B_length , direction ="+y" , **ld_LN)
    path1.segment(length = Brad_length , direction ="+y" , final_width = Width_WG + Brad , **ld_LN)
    
    
    x = path1.x
    y = path1.y
    
    rect = gdspy.Rectangle(( x + Brad/2 + Width_WG/2 , y ), ( x - Brad/2 - Width_WG /2 ,y + 1  ),**ld_LN)
    circle = gdspy.Round((x, y + 1 ), 0.5 ,initial_angle = np.pi , final_angle = 2*np.pi ,**ld_LN ,tolerance = 0.00001 , number_of_points = 199)
    stam = gdspy.boolean(rect,circle,"not",**ld_LN)
    top_cell.add(stam)
    
    #create the arrow sign
    points = [( x - diss_arrow_from_wg , y + 500 ),(x - diss_arrow_from_wg - arrow_diss_down , y + 500)
              ,(x - diss_arrow_from_wg - arrow_diss_down , y + 500 + arrow_mid_height)
              ,(x - diss_arrow_from_wg - arrow_diss_down - arrow_diss_sides , y + 500 + arrow_mid_height)
              ,( x - diss_arrow_from_wg - arrow_diss_down/2 , y + 500 + arrow_mid_height + arrow_top_height)
              ,(x - diss_arrow_from_wg + arrow_diss_sides , y + 500 + arrow_mid_height)
              ,(x - diss_arrow_from_wg , y + 500 + arrow_mid_height)]
    arrow = gdspy.Polygon(points,**ld_LN)
    arrowM = gdspy.Polygon(points,**ld_Metal)
    top_cell.add(arrow)
    top_cell.add(arrowM)
    
    
    #creating the right arm with the openings to the contacts
    path2 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x + Brad/2,path1.y + 0.5 ))
    path2 = sbendPath( wgsbend = path2 , L = S_length , H = S_heigth_top , info = ld_LN)
    
    rec = gdspy.Rectangle((path2.x - diss_holes_wg - Width_WG/2 - diss_to_metal , path2.y + 1000 - holes_height /2)
                          ,(path2.x - diss_holes_wg - holes_width - Width_WG/2 - diss_to_metal , path2.y + 1000 + holes_height /2), **ld_SU8)
    rect = rec.fillet(50)
    top_cell.add(rect)
    
    rec = gdspy.Rectangle((path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg , path2.y + 3000 - holes_height /2)
                          ,(path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg + holes_width , path2.y + 3000 + holes_height /2), **ld_SU8)
    rect = rec.fillet(50)
    top_cell.add(rect)
    
    path2.segment(length = A_length + 673 , direction ="+y" , **ld_LN)
    
    
    #creating the left arm
    path3 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x - Brad/2 , path1.y + 0.5 ))
    path3.x = path3.x - S_height/2
    path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_LN)
    path3.segment(length = A_length + 673 , direction ="+y" , **ld_LN)
    
    
    #creating the contact
    mid = gdspy.offset([path3,path2] , diss_to_metal , join_first = True ,**ld_SU8)
    rect = gdspy.Rectangle((x - Metal_width - S_height , y + S_length/2), (x + Metal_width + S_heigth_top , y + S_length + A_length), **ld_Metal)
    stam = gdspy.boolean(rect,mid,"not",**ld_Metal)
    
    path5=gdspy.Path(50,(0,y+S_length/2-100))
    path5.segment(350,"+x",**ld_Metal)
    path5.turn(100,a2r(90),final_width=100,**ld_Metal)
    
    path6 = gdspy.Path(50,(0,y+S_length/2-100))
    path6.segment(350,"+x",**ld_Metal)
    path6.turn(100,a2r(90),final_width=100,**ld_Metal)
    path6.mirror((0,y+S_length/2+25),(0,y+S_length/2-25))
    
    
    path7=gdspy.Path(50,(0,path3.y-573))
    path7.segment(350,"+x",**ld_Metal)
    path7.turn(100,a2r(-90),final_width=100,**ld_Metal)
    
    path8 = gdspy.Path(50,(0,path3.y-573))
    path8.segment(350,"+x",**ld_Metal)
    path8.turn(100,a2r(-90),final_width=100,**ld_Metal)
    path8.mirror((0,path3.y-500+25),(0,path3.y-500-25))
    
    
    
    
    
   
    # sign at the top
    x = path3.x
    y = path3.y - 523
    
    points = [(x - tri_diss_from_wg , y ),(x - tri_diss_from_wg , y + tri_height),(x - tri_diss_from_wg - tri_width , y  + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    top_cell.add(tri)
    
    points = [(x - tri_diss_from_wg , y  +  tri_height),(x - tri_diss_from_wg , y  + tri_height*2),(x - tri_diss_from_wg - tri_width , y  + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    top_cell.add(tri)
    
    x = path2.x
    
    points = [(x  - tri_diss_from_wg , y ),(x  - tri_diss_from_wg , y  + tri_height),(x  - tri_diss_from_wg - tri_width , y  + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    top_cell.add(tri)
    
    points = [(x  - tri_diss_from_wg , y  +  tri_height),(x  - tri_diss_from_wg , y  + tri_height*2),(x  - tri_diss_from_wg - tri_width , y  + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    top_cell.add(tri)
    
    x = path4.x
    
    points = [(x  - tri_diss_from_wg , y ),(x  - tri_diss_from_wg , y  + tri_height),(x  - tri_diss_from_wg - tri_width , y  + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    top_cell.add(tri)
    
    points = [(x  - tri_diss_from_wg , y  +  tri_height),(x  - tri_diss_from_wg , y  + tri_height*2),(x  - tri_diss_from_wg - tri_width , y  + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    top_cell.add(tri)
    
    
    
    
    
    
    
    
    
    
    
    top_cell.add(path1)
    top_cell.add(path2)
    top_cell.add(path3)
    top_cell.add(path4)
    top_cell.add(path5)
    top_cell.add(path6)
    top_cell.add(path7)
    top_cell.add(path8)
    top_cell.add(stam)

    
    return([path2.x , path2.y , path3.x , path3.y])



# draw close Y - spliter - MZ-modulator new contact
def cielo_close_sbend (cell,B_length = 200 , Brad_length = 427 , Brad = 6 , A_length = 5089 , S_length = 6833 , S_height = 210 , S_height_top = 190 
    
                       , Width_WG = Width_WG , x = 0 , y = 0,Metal_width = Metal_width , diss_to_metal = diss_to_metal):

    path4 = gdspy.Path(width = Width_WG ,initial_point = (x + gap,y))
    path4.segment(B_length*2 + Brad_length*2 + S_length*2 + A_length + 2 ,"+y" ,**ld_LN )
    
    points = [(x - tri_diss_from_wg , y + 500),(x - tri_diss_from_wg , y + 500 + tri_height),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x - tri_diss_from_wg , y + 500 +  tri_height),(x - tri_diss_from_wg , y + 500 + tri_height*2),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x + gap - tri_diss_from_wg , y + 500),(x + gap - tri_diss_from_wg , y + 500 + tri_height),(x + gap - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x + gap - tri_diss_from_wg , y + 500 +  tri_height),(x + gap - tri_diss_from_wg , y + 500 + tri_height*2),(x + gap - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = B_length , direction ="+y" , **ld_LN)
    path1.segment(length = Brad_length , direction ="+y" , final_width = Width_WG + Brad , **ld_LN)
    
    
    
    
    x = path1.x
    y = path1.y
    
    rect = gdspy.Rectangle(( x + Brad/2 + Width_WG/2 , y ), ( x - Brad/2 - Width_WG /2 ,y + 1  ),**ld_LN)
    circle = gdspy.Round((x, y + 0.5 ), 0.5 ,initial_angle = np.pi , final_angle = 2*np.pi ,**ld_LN ,tolerance = 0.00001 , number_of_points = 199)
    stam = gdspy.boolean(rect,circle,"not",**ld_LN)
    cell.add(stam)
    
    
    #create the arrow sign
    points = [( x - diss_arrow_from_wg , y + 1350 ),(x - diss_arrow_from_wg - arrow_diss_down , y + 1350)
              ,(x - diss_arrow_from_wg - arrow_diss_down , y + 1350 + arrow_mid_height)
              ,(x - diss_arrow_from_wg - arrow_diss_down - arrow_diss_sides , y + 1350 + arrow_mid_height)
              ,( x - diss_arrow_from_wg - arrow_diss_down/2 , y + 1350 + arrow_mid_height + arrow_top_height)
              ,(x - diss_arrow_from_wg + arrow_diss_sides , y + 1350 + arrow_mid_height)
              ,(x - diss_arrow_from_wg , y + 1350 + arrow_mid_height)]
    arrow = gdspy.Polygon(points,**ld_LN)
    arrowM = gdspy.Polygon(points,**ld_Metal)
    cell.add(arrow)
    cell.add(arrowM)
    
    
    
    
    path2 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x + Brad/2,path1.y + 0.5 ))
    path2 = sbendPath( wgsbend = path2 , L = S_length , H = S_height_top , info = ld_LN)
    
    path2 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x + Brad/2,path1.y + 0.5 ))
    path2 = sbendPath( wgsbend = path2 , L = S_length , H = S_height_top , info = ld_LN)
    
    rec = gdspy.Rectangle((path2.x - diss_holes_wg - Width_WG/2 - diss_to_metal , path2.y + 1000 - holes_height /2)
                          ,(path2.x - diss_holes_wg - holes_width - Width_WG/2 - diss_to_metal , path2.y + 1000 + holes_height /2), **ld_SU8)
    rect = rec.fillet(50)
    cell.add(rect)
    
    rec = gdspy.Rectangle((path2.x - diss_holes_wg - Width_WG/2 - diss_to_metal + 15 , path2.y + 1000 - holes_height /2 - 15)
                          ,(path2.x - diss_holes_wg - holes_width - Width_WG/2 - diss_to_metal  - 15, path2.y + 1000 + holes_height /2 + 15 ), **ld_Metal)
    rect = rec.fillet(50)
    cell.add(rect)
    
    x2 = path2.x
    y2 = path2.y
    
    path2.segment(length = A_length , direction ="+y" , **ld_LN)
    path2.x = path2.x - S_height_top/2
    path2 = sbendPathM( wgsbend = path2 , L = S_length , H = S_height_top , info = ld_LN)
    
    rec = gdspy.Rectangle((path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg + 100 , path2.y - S_length/2 - holes_height /2 + 15 + 500)
                          ,(path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg + holes_width + 100 , path2.y - S_length/2 + holes_height /2 - 15 + 500), **ld_SU8)
    rect = rec.fillet(50)
    cell.add(rect)
    
    rec = gdspy.Rectangle((path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg - 15 + 100 , path2.y - S_length/2 - holes_height /2 + 500)
                          ,(path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg + holes_width + 15 + 100 ,path2.y - S_length/2 + holes_height /2 + 500), **ld_Metal)
    rect = rec.fillet(50)
    cell.add(rect)
    
    
    
    
    path3 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x - Brad/2 , path1.y + 0.5 ))
    path3.x = path3.x - S_height/2
    path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_LN)
    x3 = path3.x
    path3.segment(length = A_length , direction ="+y" , **ld_LN)
    path3 = sbendPath( wgsbend = path3 , L = S_length , H = S_height , info = ld_LN)
    
    rec = gdspy.Rectangle((x2 - Width_WG/2 - diss_to_metal - 15 , y2 + 1000) 
                          ,(x3 + Width_WG/2 + diss_to_metal + 15 , y2 + 1000 + 20)
                          , **ld_Metal)
    cell.add(rec)
    
    
    rect = gdspy.Rectangle(( path2.x + Width_WG/2 , path2.y ), ( path3.x - Width_WG /2 ,path3.y + 1  ),**ld_LN)
    circle = gdspy.Round((0, path3.y), 0.5 ,initial_angle = 0 , final_angle = np.pi ,**ld_LN ,tolerance = 0.00001 , number_of_points = 199)
    stam = gdspy.boolean(rect,circle,"not",**ld_LN)
    cell.add(stam)
    
    mid = gdspy.offset([path3,path2] , diss_to_metal , join_first = True ,**ld_SU8)
    rect = gdspy.Rectangle((x - 600 , y + S_length/2), (x + 600 , y + S_length + A_length + S_length/2), **ld_Metal)
    stam = gdspy.boolean(rect,mid,"not",**ld_Metal)
    
    mid = gdspy.offset([path3,path2] , diss_to_metal + Metal_width  , join_first = True ,**ld_SU8)
    rect = gdspy.Rectangle((x - 600 , y + S_length/2), (x + 600 , y + S_length + A_length + S_length/2), **ld_Metal)
    stam2 = gdspy.boolean(rect,mid,"not",**ld_Metal)
    
    stam = gdspy.boolean(stam,stam2,"not",**ld_Metal)
    
    
    
    
    place = stam.get_bounding_box()
    rightX = place[1,0]
    rightY = place[1,1]
    #leftX = place[0,0]
    
    print(place[0,0])
    
    path7=gdspy.Path(Metal_width - 1 ,(rightX  - (S_height*np.cos(a2r(S_height/2)) + S_height_top*(1-np.cos(a2r(S_height/2))) + diss_to_metal*2 + Metal_width*2)/2 - 100 - Width_WG/2 , rightY + 100))
    path7.segment((S_height*np.cos(a2r(S_height/2)) + S_height_top*(1-np.cos(a2r(S_height/2))) + diss_to_metal*2 + Metal_width*2)/2 - 100  ,"+x",**ld_Metal)
    path7.turn(100,a2r(-90),**ld_Metal)
   
    
    path8=gdspy.Path(Metal_width - 1 ,(rightX  - (S_height*np.cos(a2r(S_height/2)) + S_height_top*(1-np.cos(a2r(S_height/2))) + diss_to_metal*2 + Metal_width*2)/2 - 100 - Width_WG/2 , rightY + 100))
    path8.segment((S_height*np.cos(a2r(S_height/2)) + S_height_top*(1-np.cos(a2r(S_height/2))) + diss_to_metal*2 + Metal_width*2)/2 - 80  ,"+x",**ld_Metal)
    path8.turn(100,a2r(-90),**ld_Metal)
    path8.mirror((5, rightY)
                 ,((5, rightY - 20)))
    
    
    
    rec = gdspy.Rectangle(( (rightX  - (S_height*np.cos(a2r(S_height/2)) + S_height_top*(1-np.cos(a2r(S_height/2))) + diss_to_metal*2 + Metal_width*2)/2 + Width_WG/2 + diss_to_metal + 12 , path2.y - S_length/2 - holes_height/2 + 550))
                          , ((rightX  - (S_height*np.cos(a2r(S_height/2)) + S_height_top*(1-np.cos(a2r(S_height/2))) + diss_to_metal*2 + Metal_width*2)/2 + Width_WG/2 + diss_to_metal + 12 + diss_holes_wg - 15, path2.y - S_length/2 - holes_height/2 + 550 + 20))
                          ,**ld_Metal)
    cell.add(rec)
    
    path5 = gdspy.Path(Width_WG + Brad ,(0,path3.y + 1))
    path5.segment(Brad_length , "+y" , final_width = Width_WG ,**ld_LN)
    path5.segment(B_length , "+y" ,**ld_LN)
    
    x = path5.x
    y = path5.y
    
    
    points = [(x - tri_diss_from_wg , y - 800),(x - tri_diss_from_wg , y - 800 + tri_height),(x - tri_diss_from_wg - tri_width , y - 800 + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x - tri_diss_from_wg , y - 800 +  tri_height),(x - tri_diss_from_wg , y - 800 + tri_height*2),(x - tri_diss_from_wg - tri_width , y - 800 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    cell.add([path1,path2,path3,path4,path5,path7,path8,stam])
    return([path2.x , path2.y , path3.x , path3.y])

# draw close Y - spliter _ MZ-modulator old contact
def cielo_close_sbend_old (cell,B_length = 1580 , Brad_length = 426 , Brad = 6 , A_length = 10498 , S_length = 6833 
                           , S_height = 210 , S_heigth_top = 190 , Width_WG = Width_WG , x = 0 , y = 0 , Metal_width = Metal_width , diss_to_metal = diss_to_metal):
    
    path4 = gdspy.Path(width = Width_WG ,initial_point = (x +  gap,y))
    path4.segment(B_length + Brad_length + S_length + A_length + 501 + 173  ,"+y" ,**ld_LN )
    
    
    """
    #sign at the begining
    points = [(x - sign_diss_from_wg , y + 50)
              ,(x - sign_diss_from_wg - sign_bottom , y + 50)
              ,(x - sign_diss_from_wg - sign_bottom , y + 50 + sign_height)
              ,(x - sign_diss_from_wg - sign_bottom + sign_width , y + 50 + sign_height)
              ,(x - sign_diss_from_wg - sign_bottom + 20 , y + 50 + sign_width)
              ,(x - sign_diss_from_wg , y + 50 + sign_width)]
    
   
    
    
    signM = gdspy.Polygon(points,**ld_METAL2)
    top_cell.add(signM)
    
    """
    
    
    points = [(x - tri_diss_from_wg , y + 500),(x - tri_diss_from_wg , y + 500 + tri_height),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x - tri_diss_from_wg , y + 500 +  tri_height),(x - tri_diss_from_wg , y + 500 + tri_height*2),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x + gap - tri_diss_from_wg , y + 500),(x + gap - tri_diss_from_wg , y + 500 + tri_height),(x + gap - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x + gap - tri_diss_from_wg , y + 500 +  tri_height),(x + gap - tri_diss_from_wg , y + 500 + tri_height*2),(x + gap - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    #the start of the WG
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = B_length , direction ="+y" , **ld_LN)
    path1.segment(length = Brad_length , direction ="+y" , final_width = Width_WG + Brad , **ld_LN)
    
    
    x = path1.x
    y = path1.y
    
    rect = gdspy.Rectangle(( x + Brad/2 + Width_WG/2 , y ), ( x - Brad/2 - Width_WG /2 ,y + 1  ),**ld_LN)
    circle = gdspy.Round((x, y + 1 ), 0.5 ,initial_angle = np.pi , final_angle = 2*np.pi ,**ld_LN ,tolerance = 0.00001 , number_of_points = 199)
    stam = gdspy.boolean(rect,circle,"not",**ld_LN)
    cell.add(stam)
    
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
    
    
    #creating the right arm with the openings to the contacts
    path2 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x + Brad/2,path1.y + 0.5 ))
    path2 = sbendPath( wgsbend = path2 , L = S_length , H = S_heigth_top , info = ld_LN)
    
    rec = gdspy.Rectangle((path2.x - diss_holes_wg - Width_WG/2 - diss_to_metal , path2.y + 1000 - holes_height /2)
                          ,(path2.x - diss_holes_wg - holes_width - Width_WG/2 - diss_to_metal , path2.y + 1000 + holes_height /2), **ld_SU8)
    rect = rec.fillet(50)
    cell.add(rect)
    
    rec = gdspy.Rectangle((path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg , path2.y + 3000 - holes_height /2)
                          ,(path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg + holes_width , path2.y + 3000 + holes_height /2), **ld_SU8)
    rect = rec.fillet(50)
    cell.add(rect)
    
    path2.segment(length = A_length + 673 , direction ="+y" , **ld_LN)
    
    
    #creating the left arm
    path3 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x - Brad/2 , path1.y + 0.5 ))
    path3.x = path3.x - S_height/2
    path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_LN)
    path3.segment(length = A_length + 673 , direction ="+y" , **ld_LN)
    
    
    #creating the contact
    mid = gdspy.offset([path3,path2] , diss_to_metal , join_first = True ,**ld_SU8)
    rect = gdspy.Rectangle((x - Metal_width - S_height , y + S_length/2), (x + Metal_width + S_heigth_top , y + S_length + A_length), **ld_Metal)
    stam = gdspy.boolean(rect,mid,"not",**ld_Metal)
    
    path5=gdspy.Path(50,(0,y+S_length/2-100))
    path5.segment(350,"+x",**ld_Metal)
    path5.turn(100,a2r(90),final_width=100,**ld_Metal)
    
    path6 = gdspy.Path(50,(0,y+S_length/2-100))
    path6.segment(350,"+x",**ld_Metal)
    path6.turn(100,a2r(90),final_width=100,**ld_Metal)
    path6.mirror((0,y+S_length/2+25),(0,y+S_length/2-25))
    
    
    path7=gdspy.Path(50,(0,path3.y-573))
    path7.segment(350,"+x",**ld_Metal)
    path7.turn(100,a2r(-90),final_width=100,**ld_Metal)
    
    path8 = gdspy.Path(50,(0,path3.y-573))
    path8.segment(350,"+x",**ld_Metal)
    path8.turn(100,a2r(-90),final_width=100,**ld_Metal)
    path8.mirror((0,path3.y-500+25),(0,path3.y-500-25))
    
    
    
    
    
   
    # sign at the top
    x = path3.x
    y = path3.y - 523
    
    points = [(x - tri_diss_from_wg , y ),(x - tri_diss_from_wg , y + tri_height),(x - tri_diss_from_wg - tri_width , y  + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x - tri_diss_from_wg , y  +  tri_height),(x - tri_diss_from_wg , y  + tri_height*2),(x - tri_diss_from_wg - tri_width , y  + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    x = path2.x
    
    points = [(x  - tri_diss_from_wg , y ),(x  - tri_diss_from_wg , y  + tri_height),(x  - tri_diss_from_wg - tri_width , y  + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x  - tri_diss_from_wg , y  +  tri_height),(x  - tri_diss_from_wg , y  + tri_height*2),(x  - tri_diss_from_wg - tri_width , y  + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    x = path4.x
    
    points = [(x  - tri_diss_from_wg , y ),(x  - tri_diss_from_wg , y  + tri_height),(x  - tri_diss_from_wg - tri_width , y  + tri_height)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    points = [(x  - tri_diss_from_wg , y  +  tri_height),(x  - tri_diss_from_wg , y  + tri_height*2),(x  - tri_diss_from_wg - tri_width , y  + tri_height*2)]
    tri = gdspy.Polygon(points , **ld_Metal)
    cell.add(tri)
    
    
    
    
    
    
    
    
    
    
    
    cell.add(path1)
    cell.add(path2)
    cell.add(path3)
    cell.add(path4)
    cell.add(path5)
    cell.add(path6)
    cell.add(path7)
    cell.add(path8)
    cell.add(stam)

    
    return([path2.x , path2.y , path3.x , path3.y])


# draw 1x4 tree new contact
def cielo_1x4internal (cell,B_length = 1750 , Brad_length = 426 , Brad = 6 , A_length = 12220 , S_length = 6833 , S_height = 210 , S_heigth_top = 190 
           , Width_WG = Width_WG ,Metal_width = Metal_width  , x = 0 , y = 0  , sign_at_top = 0 , holes_width = holes_width , diss_holes_wg = diss_holes_wg , C = 1):
    
   points = [(x - tri_diss_from_wg , y + 500),(x - tri_diss_from_wg , y + 500 + tri_height),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
   tri = gdspy.Polygon(points , **ld_Metal)
   cell.add(tri)
   
   points = [(x - tri_diss_from_wg , y + 500 +  tri_height),(x - tri_diss_from_wg , y + 500 + tri_height*2),(x - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
   tri = gdspy.Polygon(points , **ld_Metal)
   cell.add(tri)
   
   points = [(x + gap - tri_diss_from_wg , y + 500),(x + gap - tri_diss_from_wg , y + 500 + tri_height),(x + gap - tri_diss_from_wg - tri_width , y + 500 + tri_height)]
   tri = gdspy.Polygon(points , **ld_Metal)
   cell.add(tri)
   
   points = [(x + gap - tri_diss_from_wg , y + 500 +  tri_height),(x + gap - tri_diss_from_wg , y + 500 + tri_height*2),(x + gap - tri_diss_from_wg - tri_width , y + 500 + tri_height*2)]
   tri = gdspy.Polygon(points , **ld_Metal)
   cell.add(tri)
   
   #the start of the WG
   path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
   path1.segment(length = B_length , direction ="+y" , **ld_LN)
   path1.segment(length = Brad_length , direction ="+y" , final_width = Width_WG + Brad , **ld_LN)
   
   
   x = path1.x
   y = path1.y
   
   rect = gdspy.Rectangle(( x + Brad/2 + Width_WG/2 , y ), ( x - Brad/2 - Width_WG /2 ,y + 1  ),**ld_LN)
   circle = gdspy.Round((x, y + 1 ), 0.5 ,initial_angle = np.pi , final_angle = 2*np.pi ,**ld_LN ,tolerance = 0.00001 , number_of_points = 199)
   stam = gdspy.boolean(rect,circle,"not",**ld_LN)
   cell.add(stam)
   
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
   
   
   #creating the right arm with the openings to the contacts
   path2 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x + Brad/2,path1.y + 0.5 ))
   path2 = sbendPath( wgsbend = path2 , L = S_length , H = S_heigth_top , info = ld_LN)
   
   if (C == 1):
       rec = gdspy.Rectangle((path2.x - diss_holes_wg - Width_WG/2 - diss_to_metal , path2.y + 1000 - holes_height /2)
                             ,(path2.x - diss_holes_wg - holes_width - Width_WG/2 - diss_to_metal , path2.y + 1000 + holes_height /2), **ld_SU8)
       rect = rec.fillet(50)
       cell.add(rect)
       
       rec = gdspy.Rectangle((path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg , path2.y + 3000 - holes_height /2)
                             ,(path2.x + Width_WG/2 + diss_to_metal + diss_holes_wg + holes_width , path2.y + 3000 + holes_height /2), **ld_SU8)
       rect = rec.fillet(50)
       cell.add(rect)
   
   path2.segment(length = A_length + 673 , direction ="+y" , **ld_LN)
   
   
   #creating the left arm
   path3 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x - Brad/2 , path1.y + 0.5 ))
   path3.x = path3.x - S_height/2
   path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_LN)
   path3.segment(length = A_length + 673 , direction ="+y" , **ld_LN)
   
   
   #creating the contact
   if(C == 1):
       mid = gdspy.offset([path3,path2] , diss_to_metal , join_first = True ,**ld_SU8)
       rect = gdspy.Rectangle((x - Metal_width - S_height , y + S_length/2), (x + Metal_width + S_heigth_top , y + S_length + A_length), **ld_Metal)
       stam = gdspy.boolean(rect,mid,"not",**ld_Metal)
       
       path5=gdspy.Path(50,(0,y+S_length/2-100))
       path5.segment(450,"+x",**ld_Metal)
       path5.turn(100,a2r(90),final_width=100,**ld_Metal)
       
       path6 = gdspy.Path(50,(0,y+S_length/2-100))
       path6.segment(450,"+x",**ld_Metal)
       path6.turn(100,a2r(90),final_width=100,**ld_Metal)
       path6.mirror((0,y+S_length/2+25),(0,y+S_length/2-25))
       
       
       path7=gdspy.Path(50,(0,path3.y-573))
       path7.segment(450,"+x",**ld_Metal)
       path7.turn(100,a2r(-90),final_width=100,**ld_Metal)
       
       path8 = gdspy.Path(50,(0,path3.y-573))
       path8.segment(450,"+x",**ld_Metal)
       path8.turn(100,a2r(-90),final_width=100,**ld_Metal)
       path8.mirror((0,path3.y-500+25),(0,path3.y-500-25))
   
   
   # sign at the top
   x = path3.x
   y = path3.y - 523
   
   points = [(x - tri_diss_from_wg , y ),(x - tri_diss_from_wg , y + tri_height),(x - tri_diss_from_wg - tri_width , y  + tri_height)]
   tri = gdspy.Polygon(points , **ld_Metal)
   cell.add(tri)
   
   points = [(x - tri_diss_from_wg , y  +  tri_height),(x - tri_diss_from_wg , y  + tri_height*2),(x - tri_diss_from_wg - tri_width , y  + tri_height*2)]
   tri = gdspy.Polygon(points , **ld_Metal)
   cell.add(tri)
   
   x = path2.x
   
   points = [(x  - tri_diss_from_wg , y ),(x  - tri_diss_from_wg , y  + tri_height),(x  - tri_diss_from_wg - tri_width , y  + tri_height)]
   tri = gdspy.Polygon(points , **ld_Metal)
   cell.add(tri)
   
   points = [(x  - tri_diss_from_wg , y  +  tri_height),(x  - tri_diss_from_wg , y  + tri_height*2),(x  - tri_diss_from_wg - tri_width , y  + tri_height*2)]
   tri = gdspy.Polygon(points , **ld_Metal)
   cell.add(tri)
   
   
   cell.add(path1)
   cell.add(path2)
   cell.add(path3)
   
   cell.add(path5)
   cell.add(path6)
   cell.add(path7)
   cell.add(path8)
   cell.add(stam)

   
   return([path2.x , path2.y , path3.x , path3.y])

def cielo_1x4 (cell,B_length = 1050 , Brad_length = 426 , Brad = 6 , A_length = 12220 , S_length = 6833 , S_height = 210 , S_heigth_top = 190 
           , Width_WG = Width_WG ,M_width = Metal_width  , x = 0 , y = 0  , sign_at_top = 0 , holes_width = holes_width , diss_holes_wg = diss_holes_wg , C = 1):

    # first
    [x1 , y1 , x0 , y0] = cielo_1x4internal(cell ,S_height = 320 , S_heigth_top = 280 , Metal_width = 200 ,C = C)

    #seond Top
    [x11 , y11 , x10 ,y10 ] = cielo_1x4internal (cell, x = x1 , y = y1 , S_height = 110 , S_heigth_top = 90 , Metal_width = 100 , holes_width = 140 , diss_holes_wg = 24 , C = C)

    #second Bottom
    [x01 , y01 , x00 ,y00 ] = cielo_1x4internal (cell, x = x0 , y = y0, S_height = 110 , S_heigth_top = 90 , Metal_width = 100  , holes_width = 140  , diss_holes_wg = 24 , C = C)




# draw 1x8 tree without contact


def cielo_1x8internal (cell,B_length = 1750 , Brad_length = 426 , Brad = 6 , A_length = 12220 , S_length = 6833 , S_height = 210 , S_heigth_top = 190 
           , Width_WG = Width_WG ,M_width = Metal_width  , x = 0 , y = 0):
    """
    path4 = gdspy.Path(width = Width_WG ,initial_point = (x + S_height + gap,y))
    path4.segment(B_length + Brad_length + S_length + A_length + 1  ,"+y" ,**ld_LN )
    """
    path1 = gdspy.Path( width = Width_WG ,initial_point = (x,y))
    path1.segment(length = B_length , direction ="+y" , **ld_LN)
    path1.segment(length = Brad_length , direction ="+y" , final_width = Width_WG + Brad , **ld_LN)
    
    
    x = path1.x
    y = path1.y
    
    rect = gdspy.Rectangle(( x + Brad/2 + Width_WG/2 , y ), ( x - Brad/2 - Width_WG /2 ,y + 1  ),**ld_LN)
    circle = gdspy.Round((x, y + 1 ), 0.5 ,initial_angle = np.pi , final_angle = 2*np.pi ,**ld_LN ,tolerance = 0.00001 , number_of_points = 199)
    stam = gdspy.boolean(rect,circle,"not",**ld_LN)
    cell.add(stam)
    
    
    
    path2 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x + Brad/2,path1.y + 0.5 ))
    path2 = sbendPath( wgsbend = path2 , L = S_length , H = S_heigth_top , info = ld_LN)
    path2.segment(length = A_length , direction ="+y" , **ld_LN)
    
    
    path3 = gdspy.Path( width = Width_WG ,initial_point = ( path1.x - Brad/2 , path1.y + 0.5 ))
    path3.x = path3.x - S_height/2
    path3 = sbendPathM( wgsbend = path3 , L = S_length , H = S_height , info = ld_LN)
    path3.segment(length = A_length , direction ="+y" , **ld_LN)
    
    
    
    mid = gdspy.offset([path3,path2] , diss_to_metal , join_first = True ,**ld_SU8)
    rect = gdspy.Rectangle((x - M_width/2 , y + S_length/5), (x + M_width/2 , y + S_length + A_length), **ld_Metal)
    stam = gdspy.boolean(rect,mid,"not",**ld_Metal)
    
    
    
    
    
    cell.add(path1)
    cell.add(path2)
    cell.add(path3)
    #cell.add(path4)
    cell.add(stam)

    
    return([path2.x , path2.y , path3.x , path3.y])

def cielo_1x8 (cell,B_length = 1750 , Brad_length = 426 , Brad = 6 , A_length = 12220 , S_length = 6833 , S_height = 210 , S_heigth_top = 190 
           , Width_WG = Width_WG ,M_width = Metal_width  , x = 0 , y = 0):

    # first
    [x1 , y1 , x0 , y0] = cielo_1x8internal(cell,S_height =  400 , M_width = 3000)

    #seond Top
    [x11 , y11 , x10 ,y10 ] = cielo_1x8internal (cell, x = x1 , y = y1 , S_height =  90 , M_width = 500)

    #second Bottom
    [x01 , y01 , x00 ,y00 ] = cielo_1x8internal (cell, x = x0 , y = y0 , S_height =  90 , M_width = 500)


    #third highest
    [x111 , y111 , x110 ,y110 ] = cielo_1x8internal (cell, x = x11 , y = y11 )

    #third Mid Top
    [x101 , y101 , x100 ,y100 ] = cielo_1x8internal (cell, x = x10 , y = y10 )

    #third Mid Bottom
    [x011 , y011 , x010 ,y010 ] = cielo_1x8internal (cell, x = x01 , y = y01 )

    #third Lowest
    [x001 , y001 , x000 ,y000 ] = cielo_1x8internal (cell, x = x00 , y = y00 )

