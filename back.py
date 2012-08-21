import Image, ImageDraw
import random
import operator
from collections import defaultdict
import matplotlib.delaunay as triang


def edge_colour(edg):
    '''Returns a valid edge colouring of the given graph in the mathematical sense. No two edges that are connected by a node share the same colour.'''
    
    #generate adjacency list
    adj_list = defaultdict(list)
    for i in range(0, len(edg)):
        adj_list[edg[i][0]].append(i)
        adj_list[edg[i][1]].append(i)
   
    #colour edges
    edg_colours = [-1]*(len(edg)+1)
    for i in range(0, len(edg)):
        #hack here to work around Python's lack of a do-while loop
        stable_colour = False
        #loop until we find a 'stable' colour
        while not stable_colour:
            #assume that this pass results in a stable colour
            stable_colour = True
            #incirment our colour
            edg_colours[i] += 1
            # check against adjacent edges
            for edge_id in adj_list[edg[i][0]]:
                if (edg_colours[edge_id] == edg_colours[i]) and (edge_id <> i):
                    stable_colour = False
            for edge_id in adj_list[edg[i][1]]:
                if (edg_colours[edge_id] == edg_colours[i])  and (edge_id <> i):
                    stable_colour = False
    
    #done
    return edg_colours
        
    
def generate_hipster_colour():
    '''Generates a pesudorandom physical colour with certian properties.'''
    minimum_value = 20
    maximum_value = 220
    average_value = 150
    nudge_step = 10
    
    #create two innital random values
    alpha = random.randint(minimum_value, maximum_value)
    beta = random.randint(minimum_value, maximum_value)
    
    #try to create thrid value
    gamma = average_value*3-alpha-beta
    
    #too low?
    while gamma < minimum_value:
        #nudge alpha and beta down
        alpha -= nudge_step
        beta -= nudge_step
        #recalculate gamma
        gamma = average_value*3-alpha-beta
        
    #too high?
    while gamma > maximum_value:
        #nudge alpha and beta down
        alpha += nudge_step
        beta += nudge_step
        #recalculate gamma
        gamma = average_value*3-alpha-beta
    
    #return colour
    return (alpha, beta, gamma)
    
    
if __name__ == "__main__":
    width = 1039*4
    height = 697*4
    arc_radius = 20

    rg = random.randint
    kpadding = height*0.15
    points = [(rg(0, int(width-kpadding)),
               rg(0, int(height-kpadding))
              ) for i in range(0,30)]


    im = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(im)

    draw.rectangle((0,0,width,height), fill=(70, 84, 87))


    top, bottom, left, right = 10000,0,10000,0

    #compute the border of the rectangle bounding all the points
    for x, y in points:
        if x < left:
            left = x
        if x > right:
            right = x
        if y < top:
            top = y
        if y > bottom:
            bottom = y

    #figure out the center x and center y of the rectangle
    rect_width = (right-left)
    center_x   = rect_width/2

    rect_height = (bottom-top)
    center_y    = rect_height/2

    #compute the amount to offset the points by
    offset_from_center_x = width/2-(center_x)-left
    offset_from_center_y = height/2-(center_y)-top

    #actually offset the points
    points = [(x + offset_from_center_x,
               y + offset_from_center_y)
              for x, y in points]

    #draw the points
    for x, y in points:
        draw.ellipse((x-arc_radius, y-arc_radius, x+arc_radius, y+arc_radius),
                     fill=(205, 240, 41))

    #compute the delunay triangulation
    cens,edg,tri,neig = triang.delaunay([x for x,y in points],
                                        [y for x,y in points])

    #perform edge colouring
    edg_colours = edge_colour(edg)
    
    #remember the physical colours we've used
    physical_colours = defaultdict(generate_hipster_colour)
                                        
    #draw the delunay triangulation lines
    for i in range(0, len(edg)):
        start,end = edg[i]
        x = points[start][0]
        y = points[start][1]
        x2 = points[end][0]
        y2 = points[end][1]
        draw.line((x,y,x2,y2), fill=physical_colours[edg_colours[i]], width=4)


    #apply antialiasing
    im.thumbnail((width/4, height/4), Image.ANTIALIAS)
    #save
    im.save("back.png", "PNG")
