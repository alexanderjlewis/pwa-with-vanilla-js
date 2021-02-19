import sys
from xml.etree import ElementTree as ET

def generate(render_recipe):
    svg = ET.Element('svg', attrib={'width':'100%'})

    main_node_spacing_y = 60
    ingredient_node_spacing_y = 30
    
    main_node_r = 13
    ingredient_square_side = 16

    main_path_x = 240
    ingredient_path_x = 130

    main_start_y = 40
    text_offset_x = 25
    text_offset_y = -15
    next_node_y = main_start_y
    prev_lines = 0

    if render_recipe:
        for i, step in enumerate(render_recipe['steps']):

            if i > 0:
                next_node_y += main_node_spacing_y + ((prev_lines - 1) * 19)

            if step['ingredients']:
                temp_y = next_node_y - 8
                for j, ingredient in enumerate(step['ingredients']):
                    square = ET.Element('rect', attrib={'id':'node_' + str(i) + '_square_' + str(j),'onclick':'changecolor(this)', 'x':str(ingredient_path_x - 8),'y':str(next_node_y - 8),'width':str(ingredient_square_side),'height':str(ingredient_square_side),'fill':'#3D4242','stroke':'#3D4242'})
                    svg.append(square)
                    text = ET.Element('text', attrib={'x': str(ingredient_path_x - 16), 'y':str(next_node_y + 5),'text-anchor':'end','font-size':'smaller'})
                    text.text = ingredient['name']
                    svg.append(text)
                    text = ET.Element('text', attrib={'x': str(ingredient_path_x + 16), 'y':str(next_node_y + 5),'text-anchor':'start','font-size':'smaller'})
                    text.text = ingredient['quantity']
                    svg.append(text)
                    
                    next_node_y += ingredient_node_spacing_y
                
                next_node_y += 30
                s_path = ' '.join(['M', str(main_path_x), str(next_node_y), 'v-10 a20,20 1 0 0 -20,-20 ','H', str(ingredient_path_x + 20) ,' a20,20 0 0 1 -20,-20 V',str(temp_y)])
                s = ET.Element('path', attrib={'d':s_path, 'stroke':'#D7DADA', 'stroke-width':'6', 'fill':'none'})
                svg.insert(0,s)


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

            #first cirlce is the outline
            circle = ET.Element('circle', attrib={'cx': str(main_path_x),'cy':str(next_node_y),'r': str(main_node_r), 'fill':'white','stroke':'#929292'})
            svg.append(circle)

            #second circle is for the fill
            circle = ET.Element('circle', attrib={'cx': str(main_path_x),'cy':str(next_node_y),'r': str(main_node_r - 2), 'fill':'url(#grd' + str(i) + ')'})
            svg.append(circle)

            text = ET.Element('text', attrib={'x': str(main_path_x + text_offset_x), 'y':str(next_node_y + text_offset_y)})
            for line in step['instruction']:
                tspan =  ET.Element('tspan', attrib={'x':str(main_path_x + text_offset_x),'dy':'19'})
                tspan.text = line
                text.append(tspan)
            svg.append(text)
            prev_lines = len(step['instruction'])
            
            #text = ET.Element('text', attrib={'x': str(main_path_x + text_offset_x), 'y':str(next_node_y + text_offset_y)})

            #text = ET.Element('text', attrib={'x': str(main_path_x - text_offset_x), 'y':str(next_node_y + text_offset_y), 'text-anchor':'end'})
            #text.text = step['time']
            #svg.append(text)
        
    #oval = ET.Element('path', attrib={'d':'M287,300 v100 a13,13 1 0 0 13,13 a13,13 1 0 0 13,-13 v-100 a-13,13 1 0 0 -13,-13 a13,13 1 0 0 -13,13', 'fill':'white','stroke':'#929292'})
    #svg.append(oval)

    line_end = ' '.join(['M', str(main_path_x), str(main_start_y), 'L', str(main_path_x), str(next_node_y)])
    line = ET.Element('path', attrib={'d':line_end, 'stroke':'#D7DADA', 'stroke-width':'6'})
    svg.insert(0,line)
    #svg.attrib['height'] = '1000'
    svg.attrib['viewBox'] = '0 0 660 ' + str(next_node_y + 60)
    return ET.tostring(svg, encoding='unicode', method='html')