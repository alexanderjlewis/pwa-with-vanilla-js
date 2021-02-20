import sys
from xml.etree import ElementTree as ET


def generate(render_recipe):
    
    # static cofig vars
    main_node_spacing_y = 60
    ingredient_node_spacing_y = 30

    main_node_r = 13
    ingredient_square_side = 16

    main_path_x = 240
    ingredient_path_x = 140
    secondary_path_x = 300

    main_start_y = 40
    text_offset_x = 25

    # dynamic vars
    svg = ET.Element('svg', attrib={'width':'100%'})
    next_node_y = main_start_y
    prev_lines = 0
    i = 0
        
    #adds xml that can be tied into for a hatch fill pattern
    def add_hatch():
        pattern = ET.Element('pattern', attrib={'id':'diagonalHatch', 'patternUnits':'userSpaceOnUse', 'width':'4', 'height':'4'})
        pattern_path = ET.Element('path', attrib={'d':'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2','style':'stroke:black; stroke-width:1'})
        pattern.append(pattern_path)
        svg.append(pattern)
    add_hatch()

    def draw_step(next_node_y,prev_lines,step,secondary):
            
        def draw_square():
            square = ET.Element('rect', attrib={'id':'node_' + str(i) + '_square_' + str(j),'onclick':'changecolor(this)', 'x':str(ingredient_path_x - 8),'y':str(next_node_y - 8),'width':str(ingredient_square_side),'height':str(ingredient_square_side),'fill':'#3D4242','stroke':'#3D4242'})
            svg.append(square)
            text = ET.Element('text', attrib={'x': str(ingredient_path_x - 16), 'y':str(next_node_y + 5),'text-anchor':'end','font-size':'smaller'})
            text.text = ingredient['name']
            svg.append(text)
            text = ET.Element('text', attrib={'x': str(ingredient_path_x + 16), 'y':str(next_node_y + 5),'text-anchor':'start','font-size':'smaller'})
            text.text = ingredient['quantity']
            svg.append(text)

        #adds xml that can be tied into for the %age fill
        def add_gradient():
            grad = ET.Element('linearGradient', attrib={'id':('grd'+str(i)), 'x1':'0.5', 'y1':'1', 'x2':'0.5', 'y2':'0'})
            offset1 = ET.Element('stop', attrib={'offset':'0%', 'stop-opacity':'1', 'stop-color':'#474747'})
            offset2 = ET.Element('stop', attrib={'offset':str(step['completion']) + '%', 'stop-opacity':'1', 'stop-color':'#474747'})
            offset3 = ET.Element('stop', attrib={'offset':str(step['completion']) + '%', 'stop-opacity':'1', 'stop-color':'white'})
            offset4 = ET.Element('stop', attrib={'offset':'100%', 'stop-opacity':'1', 'stop-color':'white'})
            grad.append(offset1)
            grad.append(offset2)
            grad.append(offset3)
            grad.append(offset4)
            svg.append(grad)
            return i

        def draw_circle():
            #first cirlce is the outline
            circle = ET.Element('circle', attrib={'cx': str(main_path_x),'cy':str(next_node_y),'r': str(main_node_r), 'fill':'white','stroke':'#929292'})
            svg.append(circle)

            #second circle is for the fill
            circle = ET.Element('circle', attrib={'cx': str(main_path_x),'cy':str(next_node_y),'r': str(main_node_r - 2), 'fill':'url(#grd' + str(add_gradient()) + ')'})
            svg.append(circle)

            text = ET.Element('text', attrib={'x': str(main_path_x + text_offset_x), 'y':str(next_node_y - 19)})
            for line in step['instruction']:
                tspan =  ET.Element('tspan', attrib={'x':str(main_path_x + text_offset_x),'dy':'19','alignment-baseline':'middle'})
                tspan.text = line
                text.append(tspan)
            svg.append(text)
            prev_lines = len(step['instruction'])
            
            text = ET.Element('text', attrib={'x': str(main_path_x - text_offset_x), 'y':str(next_node_y), 'text-anchor':'end', 'alignment-baseline':'middle'})
            text.text = step['time']
            svg.append(text)

        def draw_oval():
            s_path = 'M{0},{1} v{2} a13,13 1 0 0 13,13 a13,13 1 0 0 13,-13 v-{2} a-13,13 1 0 0 -13,-13 a13,13 1 0 0 -13,13'.format(main_path_x - 13, next_node_y, step['long_step']*20)
            oval = ET.Element('path', attrib={'d':s_path, 'fill':'white','stroke':'#929292'})
            svg.append(oval)
            
            s_path = 'M{0},{1} v{2} a11,11 1 0 0 11,11 a11,11 1 0 0 11,-11 v-{2} a-11,11 1 0 0 -11,-11 a11,11 1 0 0 -11,11'.format(main_path_x - 11,next_node_y,step['long_step']*20)
            oval = ET.Element('path', attrib={'d':s_path, 'fill':'url(#diagonalHatch)'})
            svg.append(oval)

            centring_text_offset = (len(step['instruction']) * 19 / 2) + 19/2
            text = ET.Element('text', attrib={'x': str(main_path_x + text_offset_x), 'y':str(next_node_y + (step['long_step']*20)/2 - centring_text_offset)})
            for line in step['instruction']:
                tspan =  ET.Element('tspan', attrib={'x':str(main_path_x + text_offset_x),'dy':'19','alignment-baseline':'middle'})
                tspan.text = line
                text.append(tspan)
            svg.append(text)
                    
            text = ET.Element('text', attrib={'x': str(main_path_x - text_offset_x), 'y':str(next_node_y + (step['long_step']*20)/2), 'text-anchor':'end', 'alignment-baseline':'middle'})
            text.text = step['time']
            svg.append(text)        
        
        def draw_circle_secondary():
            #first cirlce is the outline
            circle = ET.Element('circle', attrib={'cx': str(secondary_path_x),'cy':str(next_node_y),'r': str(main_node_r), 'fill':'white','stroke':'#929292'})
            svg.append(circle)

            #second circle is for the fill
            circle = ET.Element('circle', attrib={'cx': str(secondary_path_x),'cy':str(next_node_y),'r': str(main_node_r - 2), 'fill':'url(#grd' + str(add_gradient()) + ')'})
            svg.append(circle)

            text = ET.Element('text', attrib={'x': str(secondary_path_x + text_offset_x), 'y':str(next_node_y - 19)})
            for line in step['instruction']:
                tspan =  ET.Element('tspan', attrib={'x':str(secondary_path_x + text_offset_x),'dy':'19','alignment-baseline':'middle'})
                tspan.text = line
                text.append(tspan)
            svg.append(text)
            prev_lines = len(step['instruction'])
            
            text = ET.Element('text', attrib={'x': str(secondary_path_x - text_offset_x), 'y':str(next_node_y), 'text-anchor':'end', 'alignment-baseline':'middle'})
            text.text = step['time']
            svg.append(text)

        def draw_oval_secondary():
            s_path = 'M{0},{1} v{2} a13,13 1 0 0 13,13 a13,13 1 0 0 13,-13 v-{2} a-13,13 1 0 0 -13,-13 a13,13 1 0 0 -13,13'.format(main_path_x - 13, next_node_y, step['long_step']*20)
            oval = ET.Element('path', attrib={'d':s_path, 'fill':'white','stroke':'#929292'})
            svg.append(oval)
            
            s_path = 'M{0},{1} v{2} a11,11 1 0 0 11,11 a11,11 1 0 0 11,-11 v-{2} a-11,11 1 0 0 -11,-11 a11,11 1 0 0 -11,11'.format(main_path_x - 11,next_node_y,step['long_step']*20)
            oval = ET.Element('path', attrib={'d':s_path, 'fill':'url(#diagonalHatch)'})
            svg.append(oval)

            centring_text_offset = (len(step['instruction']) * 19 / 2) + 19/2
            text = ET.Element('text', attrib={'x': str(main_path_x + text_offset_x), 'y':str(next_node_y + (step['long_step']*20)/2 - centring_text_offset)})
            for line in step['instruction']:
                tspan =  ET.Element('tspan', attrib={'x':str(main_path_x + text_offset_x),'dy':'19','alignment-baseline':'middle'})
                tspan.text = line
                text.append(tspan)
            svg.append(text)
                    
            text = ET.Element('text', attrib={'x': str(main_path_x - text_offset_x), 'y':str(next_node_y + (step['long_step']*20)/2), 'text-anchor':'end', 'alignment-baseline':'middle'})
            text.text = step['time']
            svg.append(text)        
        
        # for every step after the first one, we need to increment the y position for the next node
        if i > 0:
            next_node_y += main_node_spacing_y + ((prev_lines - 1) * 19)

        # if the node has ingredients, we rended them first
        if step['ingredients']:
            temp_y = next_node_y - 8

            #for each ingredient, add a square node with appropriate text
            for j, ingredient in enumerate(step['ingredients']):
                draw_square()
                next_node_y += ingredient_node_spacing_y
            
            #once all the ingredient nodes are drawn, insert the path behind them with the vertical and 's' parts.
            next_node_y += 30
            if secondary:
                s_path = 'M{0} {1} v-10 a20,20 1 0 0 -20,-20 H{2} a20,20 0 0 1 -20,-20 V{3}'.format(secondary_path_x,next_node_y,ingredient_path_x + 20,temp_y)
            else:
                s_path = 'M{0} {1} v-10 a20,20 1 0 0 -20,-20 H{2} a20,20 0 0 1 -20,-20 V{3}'.format(main_path_x,next_node_y,ingredient_path_x + 20,temp_y)
            s_path = ET.Element('path', attrib={'d':s_path, 'stroke':'#D7DADA', 'stroke-width':'6', 'fill':'none'})
            svg.insert(0,s_path) #need to insert this at the start so that it is behind the nodes

        # determine if node will be a long step (oval) or standard (circle) and render
        prev_lines = len(step['instruction'])
        if step['long_step']:
            if secondary:
                draw_oval_secondary()
            else:
                draw_oval()
            
            # this still needs work - should depend on height of oval....
            if prev_lines <= 6:
                prev_lines = 1
                next_node_y += step['long_step']*20
        else:
            if secondary:
                draw_circle_secondary()
            else:
                draw_circle()     

        return next_node_y,prev_lines  

    if render_recipe and render_recipe['steps']:
        
        #draw the first node
        step  = render_recipe['steps'][i]
        next_node_y,prev_lines = draw_step(next_node_y,prev_lines,step,False)
        
        while True:
            
            # determine what needs to happen for the next step - accomodate for branch paths
            if len(step['after']) == 1:
                i = step['after'][0]
                
                #draw the node
                step  = render_recipe['steps'][i]
                next_node_y,prev_lines = draw_step(next_node_y,prev_lines,step,False)
           
            elif len(step['after']) == 2: #this means a branch has happened
                a,b = step['after']

                temp_y = next_node_y
                next_node_y += 10

                i = a
                while True: #draw the main leg
                    #draw the node
                    step = render_recipe['steps'][i]
                    next_node_y,prev_lines = draw_step(next_node_y,prev_lines,step,False)
                    
                    i = step['after'][0]
                    step  = render_recipe['steps'][i]

                    if len(step['before']) == 2:
                        break

                i = b
                while True: #draw the second leg
                    #draw the node
                    step  = render_recipe['steps'][i]
                    next_node_y,prev_lines = draw_step(next_node_y,prev_lines,step,True)
                    
                    i = step['after'][0]
                    step  = render_recipe['steps'][i]

                    if len(step['before']) == 2:
                        break

                #draw the top 's' to join the secondary branch
                s_path = 'M{0} {1} v10 a20,20 1 0 0 20,20 H{2} a20,20 0 0 1 20,20 V{3} a20,20 0 0 1 -20,20 H{4} a20,20 1 0 0 -20,20 v10'.format(main_path_x,temp_y,secondary_path_x-20,next_node_y+10,main_path_x+20)
                s_path = ET.Element('path', attrib={'d':s_path, 'stroke':'#add8e6', 'stroke-width':'6', 'fill':'none'})
                svg.insert(0,s_path) #need to insert this at the start so that it is behind the nodes

                next_node_y += 20

            else:
                break

        line_end = ' '.join(['M', str(main_path_x), str(main_start_y), 'L', str(main_path_x), str(next_node_y)])
        line = ET.Element('path', attrib={'d':line_end, 'stroke':'#D7DADA', 'stroke-width':'6'})
        svg.insert(1,line)
        svg.attrib['height'] = '1500'
        #svg.attrib['viewBox'] = '0 0 660 ' + str(next_node_y + 60)
    return ET.tostring(svg, encoding='unicode', method='html')