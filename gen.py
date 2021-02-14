import sys
from xml.etree import ElementTree as ET
import json

with open('recipes.json') as f:
  data = json.load(f)

#print(data['recipes'][0])

svg = ET.Element('svg', attrib={'viewBox':'0 0 500 500'})

recipe = data['recipes'][0]

for i, step in enumerate(recipe['steps']):
    #print(step)
    #print(len(recipe['steps']))
    circle = ET.Element('circle', attrib={'cx': '10','cy': str(10 + i*20),'r': '5','fill': 'Green'})
    svg.append(circle)
    text = ET.Element('text', attrib={'x': '25', 'y':str(11 + i*20), 'font-size':'10pt'})
    text.text = step['instruction']
    svg.append(text)

ET.ElementTree(svg).write(sys.stdout, encoding='unicode', method='html')