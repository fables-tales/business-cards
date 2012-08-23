import Image, ImageDraw
import random
import operator
from collections import defaultdict
import matplotlib.delaunay as triang
import argparse

def edge_color(edg):
    '''Returns a valid edge coloring of the given graph in the mathematical sense. No two edges that are connected by a node share the same color.'''
    
    #generate adjacency list
    adj_list = defaultdict(list)
    for i in range(0, len(edg)):
        adj_list[edg[i][0]].append(i)
        adj_list[edg[i][1]].append(i)
   
    #color edges
    edg_colors = [-1]*(len(edg)+1)
    for i in range(0, len(edg)):
        #hack here to work around Python's lack of a do-while loop
        stable_color = False
        #loop until we find a 'stable' color
        while not stable_color:
            #assume that this pass results in a stable color
            stable_color = True
            #incirment our color
            edg_colors[i] += 1
            # check against adjacent edges
            for edge_id in adj_list[edg[i][0]]:
                if (edg_colors[edge_id] == edg_colors[i]) and (edge_id <> i):
                    stable_color = False
            for edge_id in adj_list[edg[i][1]]:
                if (edg_colors[edge_id] == edg_colors[i])  and (edge_id <> i):
                    stable_color = False
    
    #done
    return edg_colors
        
    
def generate_hipster_color():
    '''Generates a pesudorandom physical color with certian properties.'''
    minimum_value = 41
    maximum_value = 240
    average_value = 162
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
    
    #return color
    return (alpha, beta, gamma)
    
    
if __name__ == "__main__":
    width = 1039*4
    height = 697*4
    arc_radius = 20
    default_color = (205, 240, 41)
    
    #parse command line arguments
    parser = argparse.ArgumentParser(description='Generate a graph for the back of a business card.')
    parser.add_argument('--color-edges', '-c', help='Individually color the edges', action='store_true')
    args = parser.parse_args()
    
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

    #compute the delunay triangulation
    cens,edg,tri,neig = triang.delaunay([x for x,y in points],
                                        [y for x,y in points])
    if args.color_edges:
        #perform edge coloring
        edg_colors = edge_color(edg)
        
        #remember the physical colors we've used
        physical_colors = defaultdict(generate_hipster_color)
                                        
    #draw the delunay triangulation lines
    for i in range(0, len(edg)):
        start,end = edg[i]
        x = points[start][0]
        y = points[start][1]
        x2 = points[end][0]
        y2 = points[end][1]
        if args.color_edges:
            draw.line((x,y,x2,y2), fill=physical_colors[edg_colors[i]], width=4)
        else:
            draw.line((x,y,x2,y2), fill=default_color, width=4)

    #draw the points
    for x, y in points:
        draw.ellipse((x-arc_radius, y-arc_radius, x+arc_radius, y+arc_radius),
                     fill=default_color)

    #apply antialiasing
    im.thumbnail((width/4, height/4), Image.ANTIALIAS)
    #save
    im.save("back.png", "PNG")
