import sys
from xml.etree import ElementTree as ET
import textwrap


class graph_renderer():

    def __init__(self, render_recipe):
        # dynamic vars
        self.svg = ET.Element('svg', attrib={'width':'100%', 'height':'2000', 'version':"1.1", 'xmlns':"http://www.w3.org/2000/svg"})
        self.current_y = 50 #some padding for top of chart
        self.element_objs = []
        self.render_recipe = render_recipe

        # create hatched section
        self.add_defs()

        #create objects for each element
        in_split = False
        for step_id in self.render_recipe['step_layout']:

            if step_id == 'S':
                element = element_renderer(id = step_id, is_node = False)        
                if in_split:
                    element.end_split = True
                    in_split = False
                else:
                    element.start_split = True
                    in_split = True
                element.process_data()
 
            else:
                element = element_renderer(id = step_id)        

                if step_id == 'Start': #first node in drawing
                    element.first_node = True
                elif step_id == 'Finish': #last node in drawing
                    element.last_node = True
                
                if in_split:
                    element.in_split = True

                element.data = self.render_recipe['steps'][str(step_id)]
                element.process_data()

            self.element_objs.append(element)                

    def render(self):

        for obj in self.element_objs:
            print(obj.id,obj.is_node,obj.height)
            if obj.is_node:
                obj.draw(self.current_y)
                self.svg.append(obj.svg)
                self.current_y += obj.height
            else:
                self.current_y += obj.height

    def get_graph(self):
        return ET.tostring(self.svg, encoding='unicode', method='html')

    def add_defs(self):
            defs = ET.Element('defs')
            
            #add hatched pattern for long nodes
            pattern = ET.Element('pattern', attrib={'id':'diagonalHatch', 'patternUnits':'userSpaceOnUse', 'width':'4', 'height':'4'})
            pattern_path = ET.Element('path', attrib={'d':'M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2','style':'stroke:black; stroke-width:.7'})
            pattern.append(pattern_path)
            defs.append(pattern)

            #add gradient for each node
            for step in self.render_recipe['steps']:
                step_id = step
                step_completion = str(self.render_recipe['steps'][step]['completion'])

                gradient = ET.Element('linearGradient', attrib={'id':('grd_' + str(step_id)), 'x1':'0.5', 'y1':'1', 'x2':'0.5', 'y2':'0'})
                offset1 = ET.Element('stop', attrib={'offset':'0%', 'stop-opacity':'1', 'stop-color':'#474747'})
                offset2 = ET.Element('stop', attrib={'offset':step_completion + '%', 'stop-opacity':'1', 'stop-color':'#474747'})
                offset3 = ET.Element('stop', attrib={'offset':step_completion + '%', 'stop-opacity':'1', 'stop-color':'white'})
                offset4 = ET.Element('stop', attrib={'offset':'100%', 'stop-opacity':'1', 'stop-color':'white'})
                gradient.append(offset1)
                gradient.append(offset2)
                gradient.append(offset3)
                gradient.append(offset4)
                defs.append(gradient)

            self.svg.append(defs) 
   
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

class element_renderer():
    #main node variables
    main_node_spacing_y = 25
    main_node_radius = 13
    long_step_inc = 20
    main_start_y = 40
    text_offset_x = 25
    node_text_char_width = 40
    node_text_line_spacing_y = 19
    node_extra_info_text_line_spacing_y = 30

    #ingredient node variables
    ingredient_node_spacing_y = 14 #this is the gap between bottom of one node and top of next one
    ingredient_square_side = 16

    #path horizontal poisiotns
    main_path_x = 240
    ingredient_path_x = 150
    secondary_path_x = 300

    #secondary path       
    secondary_text_offset_x = 86
    secondary_s_height = 50 #20 for each radius, + 10 at start.

    def __init__(self,id,is_node = True):
        self.id = id
        self.is_node = is_node
        self.start_split = False
        self.end_split = False
        self.in_split = False
        self.main_path = True
        self.ingredients = 0
        self.lines_text = 1
        self.extra_info = False
        self.data = {}
        self.height = 0
        self.first_node = False
        self.last_node = False
        self.long_node = False
        self.y_pos = 0

        self.svg = ET.Element('svg', attrib={'width':'100%'})

    def process_data(self):     
        if self.is_node:
            #process factors
            if self.data['secondary']:
                self.main_path = False

            self.lines_text = len(textwrap.wrap(self.data['instruction'], self.node_text_char_width, break_long_words=False))
            if self.data.get('extra_info'):
                self.extra_info = True

            self.ingredients = len(self.data['ingredients'])

            if self.data['long_step']:
                self.long_node = True

            #calculate node height
            temp_text_height = 0
            temp_node_height = 0

            # work out how tall the node will be
            if self.long_node: #if it's a long step we have to add a rectangular area in the middle of the top/bottom semi circles. If this is 'short' step this is zero hight so the two semi circles form a circle node.
                temp_node_height += self.data['long_step'] * self.long_step_inc
            temp_node_height += self.main_node_radius * 2 #add the top/bottom semi circles

            # work out how tall the text will be
            if self.lines_text > 0:
                temp_text_height += self.lines_text * self.node_text_line_spacing_y
                # need to include an additional offset to account for the first line of text being centre aligned with the centre of a round node (of the radius on top of a long node)
                temp_text_height += self.main_node_radius - (self.node_text_line_spacing_y / 2)
            
            if self.extra_info == True:
                temp_text_height += self.node_extra_info_text_line_spacing_y

            # now compare the text/node height to see which prevails
            self.height += max(temp_node_height, temp_text_height)

            if self.ingredients > 0:
                self.height += ((self.ingredients - 1) * self.ingredient_node_spacing_y) + self.ingredient_square_side #this is the height that all the ingredients take up
                self.height += 50 #this is the height of the 's' shaped path that connects the ingredients to the node
            
            if not self.first_node: #add some space before the node.
                self.height += self.main_node_spacing_y

        else:
            #this isn't a node - it's a conector 'S' from primary to secondary
            self.height += self.secondary_s_height

    def draw(self,svg_y_pos):

        self.svg.set('y',str(svg_y_pos))
        
        if not self.first_node:
            self.y_pos += self.main_node_spacing_y

        if self.ingredients > 0:
            ingredients_start_y_pos = self.y_pos

            #for each ingredient, add a square node with appropriate text
            for i in range(self.ingredients):
                self.svg.append(self.draw_ingredient(i))
                self.y_pos += self.ingredient_node_spacing_y #add gap after the node

            #draw the line that sits behind the ingredient nodes
            self.svg.insert(0,self.draw_ingredients_line(ingredients_start_y_pos)) #need to insert this at the start so that the line is alawys behind the nodes

        #self.y_pos += self.main_node_radius #node is drawn for centre of radius so need to offset

        if self.long_node:
            #self.svg.append(self.draw_long_node())
            pass
        else:
            self.svg.append(self.draw_node())




        self.height = self.y_pos

        rect = ET.Element('rect', attrib={'width':'20','height':str(self.height),'stroke':'pink'})
        self.svg.append(rect)

        '''
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
                self.draw_circle(text_secondary)'''

    def draw_ingredient(self,i):
        ingredient = self.data['ingredients'][i]
        
        group = ET.Element('g',attrib={})
        square = ET.Element('rect', attrib={'x':str(self.ingredient_path_x - 8),'y':str(self.y_pos),'width':str(self.ingredient_square_side),'height':str(self.ingredient_square_side),'fill':'#3D4242','stroke':'#3D4242'})
        group.append(square)
        text = ET.Element('text', attrib={'x': str(self.ingredient_path_x - 16), 'y':str(self.y_pos + (self.ingredient_square_side / 2)),'text-anchor':'end','font-size':'smaller','alignment-baseline':'middle'})
        text.text = ingredient['name']
        group.append(text)
        text = ET.Element('text', attrib={'x': str(self.ingredient_path_x + 16), 'y':str(self.y_pos + (self.ingredient_square_side / 2)),'text-anchor':'start','font-size':'smaller','font-style':'italic','alignment-baseline':'middle'})
        text.text = str(ingredient['quantity']) + ' ' + str(ingredient['unit'])
        group.append(text)

        # increment y_pos for height of ingredient node
        self.y_pos += self.ingredient_square_side
        
        return group

    def draw_ingredients_line(self,ingredients_start_y_pos):
        top_pos = ingredients_start_y_pos + 5 #offset by 5 so line is not visible above top node
        if self.main_path:
            s_path = 'M{0} {1} V{2} a20,20 0 0 0 20,20 H{3} a20,20 0 0 1 20,20 v5'.format(self.ingredient_path_x,top_pos,self.y_pos,self.main_path_x-20)
            s_path = ET.Element('path', attrib={'d':s_path, 'stroke':'#D7DADA', 'stroke-width':'6', 'fill':'none'})
        else:
            s_path = 'M{0} {1} V{2} a20,20 0 0 0 20,20 H{3} a20,20 0 0 1 20,20 v5'.format(self.ingredient_path_x,top_pos,self.y_pos,self.secondary_path_x-20)
            s_path = ET.Element('path', attrib={'d':s_path, 'stroke':'#add8e6', 'stroke-width':'6', 'fill':'none'})
        
        self.y_pos += 45 #this is the height of the 'S' at the bottom of the ingredient path

        return s_path

    def draw_node(self):
       
        # apply offset because node is drawn from centre, not top of radius
        self.y_pos += self.main_node_radius

        group = ET.Element('g')
       
        if self.main_path:
            x_position = self.main_path_x
        else:
            x_position = self.secondary_path_x

        if self.long_node:  
            #first oval outline  
            s_path = 'M{0},{1} v{2} a{4},{4} 1 0 0 {4},{4} a{4},{4} 1 0 0 {4},-{4} v-{2} a-{4},{4} 1 0 0 -{4},-{4} a{4},{4} 1 0 0 -{4},{4}'.format(x_position - 13, self.y_pos, self.step['long_step'] * self.long_step_inc, self.main_node_radius)
            oval = ET.Element('path', attrib={'d':s_path, 'fill':'white','stroke':'#929292'})
            group.append(oval)
            
            #then the fill
            s_path = 'M{0},{1} v{2} {4},{4} 1 0 0 {4},{4} a{4},{4} 1 0 0 {4},-{4} v-{2} a-{4},{4} 1 0 0 -{4},-{4} a{4},{4} 1 0 0 -{4},{4}'.format(x_position - 11, self.y_pos, self.step['long_step'] * self.long_step_inc, self.main_node_radius - 2)
            oval = ET.Element('path', attrib={'d':s_path, 'fill':'url(#diagonalHatch)'})
            group.append(oval)

        else:
            #first cirlce is the outline
            circle = ET.Element('circle', attrib={'cx': str(x_position),'cy':str(self.y_pos),'r': str(self.main_node_radius), 'fill':'white','stroke':'#929292'})
            group.append(circle)

            #second circle is for the fill
            circle = ET.Element('circle', attrib={'cx': str(x_position),'cy':str(self.y_pos),'r': str(self.main_node_radius - 2), 'fill':'url(#grd_' + str(self.id) + ')'})
            group.append(circle)
        
        return group

    def draw_node_text(self):

        text = ET.Element('text', attrib={'x': str(self.main_path_x + self.t_offset), 'y':str(self.y_pos - 19)})
        lines = textwrap.wrap(self.step['instruction'], self.text_width, break_long_words=False)

        for line in lines:
            tspan =  ET.Element('tspan', attrib={'x':str(self.main_path_x + self.t_offset),'dy':'19','alignment-baseline':'middle'})
            tspan.text = line
            text.append(tspan)
        
        if self.step.get('extra_info'):
            tspan =  ET.Element('tspan', attrib={'x':str(self.main_path_x + self.t_offset),'dy':'30','alignment-baseline':'middle'})
            a = ET.Element('a', attrib={'tabindex':"0", 'class':"btn btn-link", "role":"button", 'data-toggle':"popover", "data-trigger":"focus", 'data-placement':"bottom", 'data-content':self.step['extra_info']})
            a.text = "Further Details..."
            tspan.append(a)
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

    def draw_long_node(self,text_secondary):

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

############## END OF CLASS ######################

def generate(render_recipe): 
    if render_recipe and render_recipe['step_layout']:
        
        obj_graph_renderer = graph_renderer(render_recipe = render_recipe)
        obj_graph_renderer.render()
        return obj_graph_renderer.get_graph()

    else:
        return False
