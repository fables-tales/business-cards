import Image, ImageDraw
import random
import operator
import matplotlib.delaunay as triang


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


    #draw the delunay triangulation lines
    for start,end in edg:
        x = points[start][0]
        y = points[start][1]
        x2 = points[end][0]
        y2 = points[end][1]
        draw.line((x,y,x2,y2), fill=(205, 240, 41), width=4)


    #apply antialiasing
    im.thumbnail((width/4, height/4), Image.ANTIALIAS)
    #save
    im.save("back.png", "PNG")
