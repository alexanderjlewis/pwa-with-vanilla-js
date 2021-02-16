import sys
from xml.etree import ElementTree as ET

def generate(render_recipe):
    svg = ET.Element('svg', attrib={'width':'100%', 'height':'100vh'})

    node_spacing_y = 60
    node_r = 13
    main_start_x = 30
    main_start_y = 40
    text_offset_x = 25
    text_offset_y = -15
    next_node_y = main_start_y
    prev_lines = 0

    if render_recipe:
        for i, step in enumerate(render_recipe['steps']):

            if i > 0:
                next_node_y += node_spacing_y + ((prev_lines - 1) * 19)

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
            circle = ET.Element('circle', attrib={'cx': str(main_start_x),'cy':str(next_node_y),'r': str(node_r), 'fill':'white','stroke':'#929292'})
            svg.append(circle)

            #second circle is for the fill
            circle = ET.Element('circle', attrib={'cx': str(main_start_x),'cy':str(next_node_y),'r': str(node_r - 2), 'fill':'url(#grd' + str(i) + ')'})
            svg.append(circle)

            text =  ET.Element('text', attrib={'x': str(main_start_x + text_offset_x), 'y':str(next_node_y + text_offset_y)})
            for line in step['instruction']:
                tspan =  ET.Element('tspan', attrib={'x':str(main_start_x + text_offset_x),'dy':'19'})
                tspan.text = line
                text.append(tspan)
            svg.append(text)
            
            prev_lines = len(step['instruction'])
        
    line_end = ' '.join(['M', str(main_start_x), str(main_start_y), 'L', str(main_start_x), str(next_node_y)])
    line = ET.Element('path', attrib={'d':line_end, 'stroke':'#D7DADA', 'stroke-width':'6'})
    svg.insert(0,line)
    svg.attrib['height'] = str(next_node_y + 60)
    return ET.tostring(svg, encoding='unicode', method='html')