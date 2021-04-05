import sys
from xml.etree import ElementTree as ET
import textwrap


class renderer():

    def __init__(self):
        # static cofig vars
        self.main_node_spacing_y = 50
        self.ingredient_node_spacing_y = 30

        self.main_node_r = 13
        self.ingredient_square_side = 16

        self.main_path_x = 240
        self.ingredient_path_x = 150
        self.secondary_path_x = 300

        self.main_start_y = 40
        self.text_offset_x = 25
        self.secondary_text_offset_x = 86

        self.text_width = 40

        # dynamic vars
        self.svg = ET.Element('svg', attrib={'width':'100%'})
        self.next_node_y = self.main_start_y
        self.prev_lines = 0
        self.i = 0
        self.ingred_counter = 0
        self.step = {}
        self.t_offset = 0
        
        # create hatched section
        self.add_hatch()
            
    #adds xml that can be tied into for a hatch fill pattern
    def add_hatch(self):
        pattern = ET.Element('pattern', attrib={'id':'diagonalHatch', 'patternUnits':'userSpaceOnUse', 'width':'4', 'height':'4'})
        pattern_path = ET.Element('path', attrib={'d':'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2','style':'stroke:black; stroke-width:.7'})
        pattern.append(pattern_path)
        self.svg.append(pattern) 

    def draw_square(self,j,ingredient):
        group = ET.Element('g',attrib={'id':'ingred' + str(self.ingred_counter)})
        square = ET.Element('rect', attrib={'id':'node_' + str(self.i) + '_square_' + str(j),'onclick':'changecolor(this)', 'x':str(self.ingredient_path_x - 8),'y':str(self.next_node_y - 8),'width':str(self.ingredient_square_side),'height':str(self.ingredient_square_side),'fill':'#3D4242','stroke':'#3D4242'})
        group.append(square)
        text = ET.Element('text', attrib={'x': str(self.ingredient_path_x - 16), 'y':str(self.next_node_y + 5),'text-anchor':'end','font-size':'smaller'})
        text.text = ingredient['name']
        group.append(text)
        text = ET.Element('text', attrib={'x': str(self.ingredient_path_x + 16), 'y':str(self.next_node_y + 5),'text-anchor':'start','font-size':'smaller','font-style':'italic','data_qty':str(ingredient['quantity']),'data_unit':ingredient['unit'],'data_ingred':ingredient['name'],'data_role':'chart_ingredient_qty','id':'chart_ingredient_qty_' + str(self.ingred_counter)})
        text.text = str(ingredient['quantity']) + ' ' + str(ingredient['unit'])
        group.append(text)
        self.svg.append(group)

    #adds xml that can be tied into for the %age fill
    def add_gradient(self):
        grad = ET.Element('linearGradient', attrib={'id':('grd'+str(self.i)), 'x1':'0.5', 'y1':'1', 'x2':'0.5', 'y2':'0'})
        offset1 = ET.Element('stop', attrib={'offset':'0%', 'stop-opacity':'1', 'stop-color':'#474747'})
        offset2 = ET.Element('stop', attrib={'offset':str(self.step['completion']) + '%', 'stop-opacity':'1', 'stop-color':'#474747'})
        offset3 = ET.Element('stop', attrib={'offset':str(self.step['completion']) + '%', 'stop-opacity':'1', 'stop-color':'white'})
        offset4 = ET.Element('stop', attrib={'offset':'100%', 'stop-opacity':'1', 'stop-color':'white'})
        grad.append(offset1)
        grad.append(offset2)
        grad.append(offset3)
        grad.append(offset4)
        self.svg.append(grad)
        return self.i

    def draw_circle(self,text_secondary):
        #first cirlce is the outline
        group = ET.Element('g')
        circle = ET.Element('circle', attrib={'cx': str(self.main_path_x),'cy':str(self.next_node_y),'r': str(self.main_node_r), 'fill':'white','stroke':'#929292'})
        group.append(circle)

        #second circle is for the fill
        circle = ET.Element('circle', attrib={'cx': str(self.main_path_x),'cy':str(self.next_node_y),'r': str(self.main_node_r - 2), 'fill':'url(#grd' + str(self.add_gradient()) + ')'})
        group.append(circle)

        text = ET.Element('text', attrib={'x': str(self.main_path_x + self.t_offset), 'y':str(self.next_node_y - 19)})
        lines = textwrap.wrap(self.step['instruction'], self.text_width, break_long_words=False)
        for line in lines:
            tspan =  ET.Element('tspan', attrib={'x':str(self.main_path_x + self.t_offset),'dy':'19','alignment-baseline':'middle'})
            tspan.text = line
            text.append(tspan)
        group.append(text)
        prev_lines = len(lines)
        
        text = ET.Element('text', attrib={'x': str(self.main_path_x - self.text_offset_x), 'y':str(self.next_node_y), 'text-anchor':'end', 'alignment-baseline':'middle'})
        text.text = self.step['time']
        group.append(text)
        
        self.svg.append(group)

        if text_secondary:
            path = 'M{0} {1} h{2}'.format(self.main_path_x,self.next_node_y,self.t_offset - 5)
            path = ET.Element('path', attrib={'d':path,'stroke':'#929292'})
            self.svg.insert(0,path)

    def draw_oval(self,text_secondary):
        group = ET.Element('g')
        
        s_path = 'M{0},{1} v{2} a13,13 1 0 0 13,13 a13,13 1 0 0 13,-13 v-{2} a-13,13 1 0 0 -13,-13 a13,13 1 0 0 -13,13'.format(self.main_path_x - 13, self.next_node_y, self.step['long_step']*20)
        oval = ET.Element('path', attrib={'d':s_path, 'fill':'white','stroke':'#929292'})
        group.append(oval)
        
        s_path = 'M{0},{1} v{2} a11,11 1 0 0 11,11 a11,11 1 0 0 11,-11 v-{2} a-11,11 1 0 0 -11,-11 a11,11 1 0 0 -11,11'.format(self.main_path_x - 11,self.next_node_y,self.step['long_step']*20)
        oval = ET.Element('path', attrib={'d':s_path, 'fill':'url(#diagonalHatch)'})
        group.append(oval)

        lines = textwrap.wrap(self.step['instruction'], self.text_width, break_long_words=False)
        centring_text_offset = (len(lines) * 19 / 2) + 19/2
        text = ET.Element('text', attrib={'x': str(self.main_path_x + self.t_offset), 'y':str(self.next_node_y + (self.step['long_step']*20)/2 - centring_text_offset)})            
        for line in lines:
            tspan =  ET.Element('tspan', attrib={'x':str(self.main_path_x + self.t_offset),'dy':'19','alignment-baseline':'middle'})
            tspan.text = line
            text.append(tspan)
        group.append(text)
                
        text = ET.Element('text', attrib={'x': str(self.main_path_x - self.text_offset_x), 'y':str(self.next_node_y + (self.step['long_step']*20)/2), 'text-anchor':'end', 'alignment-baseline':'middle'})
        text.text = self.step['time']
        group.append(text)  

        self.svg.append(group)

        if text_secondary:
            path = 'M{0} {1} h{2}'.format(self.main_path_x,self.next_node_y + (self.step['long_step']*20)/2,self.t_offset - 5)
            path = ET.Element('path', attrib={'d':path,'stroke':'#929292'})
            self.svg.insert(0,path)      

    def draw_circle_secondary(self):
        group = ET.Element('g')
        
        #first cirlce is the outline
        circle = ET.Element('circle', attrib={'cx': str(self.secondary_path_x),'cy':str(self.next_node_y),'r': str(self.main_node_r), 'fill':'white','stroke':'#929292'})
        group.append(circle)

        #second circle is for the fill
        circle = ET.Element('circle', attrib={'cx': str(self.secondary_path_x),'cy':str(self.next_node_y),'r': str(self.main_node_r - 2), 'fill':'url(#grd' + str(self.add_gradient()) + ')'})
        group.append(circle)

        text = ET.Element('text', attrib={'x': str(self.secondary_path_x + self.t_offset), 'y':str(self.next_node_y - 19)})
        lines = textwrap.wrap(self.step['instruction'], self.text_width, break_long_words=False)
        for line in lines:
            tspan =  ET.Element('tspan', attrib={'x':str(self.secondary_path_x + self.t_offset),'dy':'19','alignment-baseline':'middle'})
            tspan.text = line
            text.append(tspan)
        group.append(text)
        prev_lines = len(lines)
        
        text = ET.Element('text', attrib={'x': str(self.secondary_path_x - self.text_offset_x), 'y':str(self.next_node_y), 'text-anchor':'end', 'alignment-baseline':'middle'})
        text.text = self.step['time']
        group.append(text)

        self.svg.append(group)

    def draw_oval_secondary(self):
        group = ET.Element('g')
        
        s_path = 'M{0},{1} v{2} a13,13 1 0 0 13,13 a13,13 1 0 0 13,-13 v-{2} a-13,13 1 0 0 -13,-13 a13,13 1 0 0 -13,13'.format(self.secondary_path_x - 13, self.next_node_y, self.step['long_step']*20)
        oval = ET.Element('path', attrib={'d':s_path, 'fill':'white','stroke':'#929292'})
        group.append(oval)
        
        s_path = 'M{0},{1} v{2} a11,11 1 0 0 11,11 a11,11 1 0 0 11,-11 v-{2} a-11,11 1 0 0 -11,-11 a11,11 1 0 0 -11,11'.format(self.secondary_path_x - 11,self.next_node_y,self.step['long_step']*20)
        oval = ET.Element('path', attrib={'d':s_path, 'fill':'url(#diagonalHatch)'})
        group.append(oval)

        lines = textwrap.wrap(self.step['instruction'], self.text_width, break_long_words=False)
        centring_text_offset = (len(lines) * 19 / 2) + 19/2
        text = ET.Element('text', attrib={'x': str(self.secondary_path_x + self.t_offset), 'y':str(self.next_node_y + (self.step['long_step']*20)/2 - centring_text_offset)})
        for line in lines:
            tspan =  ET.Element('tspan', attrib={'x':str(self.secondary_path_x + self.t_offset),'dy':'19','alignment-baseline':'middle'})
            tspan.text = line
            text.append(tspan)
        group.append(text)
                
        text = ET.Element('text', attrib={'x': str(self.secondary_path_x - self.text_offset_x), 'y':str(self.next_node_y + (self.step['long_step']*20)/2), 'text-anchor':'end', 'alignment-baseline':'middle', 'fill':'#55595c'})
        text.text = self.step['time']
        group.append(text)

        self.svg.append(group)        

    def draw_s_top(self,temp_y):
        #draw the top 's' to join the secondary branch
        s_path = 'M{0} {1} v10 a20,20 1 0 0 20,20 H{2} a20,20 0 0 1 20,20 V{3} a20,20 0 0 1 -20,20 H{4} a20,20 1 0 0 -20,20 v10'.format(self.main_path_x,temp_y,self.secondary_path_x-20,self.next_node_y+10,self.main_path_x+20)
        s_path = ET.Element('path', attrib={'d':s_path, 'stroke':'#add8e6', 'stroke-width':'6', 'fill':'none'})
        self.svg.insert(0,s_path) #need to insert this at the start so that it is behind the nodes
        self.next_node_y += 10

    def draw_main_line(self):
        line_end = ' '.join(['M', str(self.main_path_x), str(self.main_start_y), 'L', str(self.main_path_x), str(self.next_node_y)])
        line = ET.Element('path', attrib={'d':line_end, 'stroke':'#D7DADA', 'stroke-width':'6'})        
        self.svg.insert(1,line)
        self.svg.attrib['viewBox'] = '0 0 690 ' + str(self.next_node_y + 60)

    def draw_step(self,step,i,secondary,text_secondary):
        self.step = step
        self.i = i

        if text_secondary:
            self.t_offset = self.secondary_text_offset_x
        else:
            self.t_offset = self.text_offset_x

        # for every step after the first one, we need to increment the y position for the next node
        if i > 0:
            self.next_node_y += self.main_node_spacing_y + ((self.prev_lines - 1) * 19)

        # if the node has ingredients, we rended them first
        if step['ingredients']:
            self.next_node_y -= 15
            
            temp_y = self.next_node_y - 8

            #for each ingredient, add a square node with appropriate text
            for j, ingredient in enumerate(step['ingredients']):
                self.draw_square(j,ingredient)
                self.ingred_counter += 1
                self.next_node_y += self.ingredient_node_spacing_y
            
            #once all the ingredient nodes are drawn, insert the path behind them with the vertical and 's' parts.
            self.next_node_y += 30
            if secondary:
                s_path = 'M{0} {1} v-10 a20,20 1 0 0 -20,-20 H{2} a20,20 0 0 1 -20,-20 V{3}'.format(self.secondary_path_x,self.next_node_y,self.ingredient_path_x + 20,temp_y)
                s_path = ET.Element('path', attrib={'d':s_path, 'stroke':'#add8e6', 'stroke-width':'6', 'fill':'none'})
            else:
                s_path = 'M{0} {1} v-10 a20,20 1 0 0 -20,-20 H{2} a20,20 0 0 1 -20,-20 V{3}'.format(self.main_path_x,self.next_node_y,self.ingredient_path_x + 20,temp_y)
                s_path = ET.Element('path', attrib={'d':s_path, 'stroke':'#D7DADA', 'stroke-width':'6', 'fill':'none'})
            self.svg.insert(0,s_path) #need to insert this at the start so that it is behind the nodes

        # determine if node will be a long step (oval) or standard (circle) and render
        self.prev_lines = len(textwrap.wrap(step['instruction'], self.text_width, break_long_words=False))
        if step['long_step']:
            if secondary:
                self.draw_oval_secondary()
            else:
                self.draw_oval(text_secondary)
            
            # this still needs work - should depend on height of oval....
            if self.prev_lines <= 6:
                self.prev_lines = 1
                self.next_node_y += step['long_step']*20
        else:
            if secondary:
                self.draw_circle_secondary()
            else:
                self.draw_circle(text_secondary)

############## END OF CLASS ######################

def generate(render_recipe): 
    if render_recipe and render_recipe['steps']:
        
        i = 0

        #draw the first node
        step  = render_recipe['steps'][i]

        chart = renderer()

        chart.draw_step(step,i,False,False)
        
        while True:
            
            # determine what needs to happen for the next step - accomodate for branch paths
            if len(step['after']) == 1:
                i = step['after'][0]
                
                #draw the node
                step  = render_recipe['steps'][i]
                if len(step['after']) == 2:
                    chart.draw_step(step,i,False,True)
                else:
                    chart.draw_step(step,i,False,False)
            
            elif len(step['after']) == 2: #this means a branch has happened
                
                a,b = step['after']

                temp_y = chart.next_node_y
                #next_node_y += 10

                i = a
                while True: #draw the main leg

                    #draw the node
                    step = render_recipe['steps'][i]
                    chart.draw_step(step,i,False,True)
                    i = step['after'][0]
                    step  = render_recipe['steps'][i]

                    if len(step['before']) == 2:
                        break

                i = b
                while True: #draw the second leg
                    #draw the node
                    step  = render_recipe['steps'][i]
                    chart.draw_step(step,i,True,False)
                    
                    i = step['after'][0]
                    step  = render_recipe['steps'][i]

                    if len(step['before']) == 2:
                        break
                
                chart.draw_s_top(temp_y)

                chart.draw_step(step,i,False,False)
                
            else:
                break

        chart.draw_main_line()
        svg = chart.svg
        
        return ET.tostring(svg, encoding='unicode', method='html')