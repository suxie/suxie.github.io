#chocolate_chips.py

import maya.cmds as cmds
import pymel.core as pcore

import random
import functools
import math

#chocolate chip object
class Chip:    

    def __init__(self, cookie, size, count, layer_group):
        # determine size based on selected cookie object
        scaled = cookie * size
        
        # create cube and set as base, track its count
        p = pcore.polyCube(sx=1, sy=1, sz=1, h=scaled, w=scaled, d=scaled, name='chip#', n='chip{}'.format(count))[0]
        self.base = p
        self.count = count
        
        cmds.parent('chip{}'.format(count), layer_group)
        
        p0 = p.vtx[0]
        p1 = p.vtx[1]
        p2 = p.vtx[2]
        p3 = p.vtx[3]
        p4 = p.vtx[4]
        p5 = p.vtx[5]
        p6 = p.vtx[6]
        p7 = p.vtx[7]
        
        # randomly move vertices
        cmds.polyMoveVertex('chip{}.vtx[0]'.format(count), translate = [p0.getPosition().x + random.uniform(0, scaled / 4), 
            p0.getPosition().y + random.uniform(0, scaled / 8), p0.getPosition().z + random.uniform(0, scaled / 4)])
        
        cmds.polyMoveVertex('chip{}.vtx[1]'.format(count), translate = [p1.getPosition().x + random.uniform(0, scaled / 4), 
            p1.getPosition().y + random.uniform(0, scaled / 4), p1.getPosition().z + random.uniform(0, scaled / 4)])
        
        cmds.polyMoveVertex('chip{}.vtx[2]'.format(count), translate = [p2.getPosition().x + random.uniform(0, scaled / 4), 
            p2.getPosition().y + random.uniform(0, scaled / 4), p2.getPosition().z + random.uniform(0, scaled / 4)])
        
        cmds.polyMoveVertex('chip{}.vtx[3]'.format(count), translate = [p3.getPosition().x + random.uniform(0, scaled / 4), 
            p3.getPosition().y + random.uniform(0, scaled / 4), p3.getPosition().z + random.uniform(0, scaled / 4)])
        
        cmds.polyMoveVertex('chip{}.vtx[4]'.format(count), translate = [p4.getPosition().x + random.uniform(0, scaled / 4), 
            p4.getPosition().y + random.uniform(0, scaled / 4), p4.getPosition().z + random.uniform(0, scaled / 4)])
        
        cmds.polyMoveVertex('chip{}.vtx[5]'.format(count), translate = [p5.getPosition().x + random.uniform(0, scaled / 4), 
            p5.getPosition().y + random.uniform(0, scaled / 4), p5.getPosition().z + random.uniform(0, scaled / 4)])
        
        cmds.polyMoveVertex('chip{}.vtx[6]'.format(count), translate = [p6.getPosition().x + random.uniform(0, scaled / 4), 
            p6.getPosition().y + random.uniform(0, scaled / 4), p6.getPosition().z + random.uniform(0, scaled / 4)])
        
        cmds.polyMoveVertex('chip{}.vtx[7]'.format(count), translate = [p7.getPosition().x + random.uniform(0, scaled / 4), 
            p7.getPosition().y + random.uniform(0, scaled / 4), p7.getPosition().z + random.uniform(0, scaled / 4)])
        
        scaling = random.uniform(1.5, 2.0)
        scalingZ = random.uniform(1.0, 1.5)
    
        pcore.scale(scaling, scaling, scalingZ)

    # print out all positions of vertices on chip
    def __str__(self):
        p = self.base
        p0 = p.vtx[0]
        p1 = p.vtx[1]
        p2 = p.vtx[2]
        p3 = p.vtx[3]
        p4 = p.vtx[4]
        p5 = p.vtx[5]
        p6 = p.vtx[6]
        p7 = p.vtx[7]
        return "\nvertex0: {}\nvertex1: {}\nvertex2: {}\nvertex3: {}\nvertex4: {}\nvertex5: {}\nvertex6: {}\nvertex7: {}".format(p0.getPosition(), p1.getPosition(), 
            p2.getPosition(), p3.getPosition(), p4.getPosition(), p5.getPosition(), p6.getPosition(), p7.getPosition())
    
    # smooth shape
    def smooth(self, count):
        cmds.setAttr('chip{}.smoothLevel'.format(count), 5)
        cmds.setAttr('chip{}.displaySmoothMesh'.format(count), 2)
    
    # randomly place and rotate
    def change(self, bounds, count, cookie):
        x = random.uniform(bounds[0], bounds[3])
        y = random.uniform(bounds[1], bounds[4])
        z = random.uniform(bounds[2], bounds[5])
        offset_z = z - (bounds[5] + bounds[2]) / 2
        offset_x = x - (bounds[3] + bounds[0]) / 2
        
        z = z + offset_x * math.tan(offset_z / offset_x)
        
        pcore.move(x, y, z)
        
        xRot = random.uniform(100, 160)
        yRot = random.uniform(80, 130)
        zRot = random.uniform(130, 180)
        
        pcore.rotate(xRot, yRot, zRot)
        
        scalingFactor = random.uniform(0.9, 1.2)
        
        pcore.scale(scalingFactor, scalingFactor, scalingFactor)
        
        cmds.geometryConstraint(cookie + '_constr', 'chip{}'.format(count))

# user interface
def createUI (pWindowTitle, pApplyCallback):
    iter = 1
    windowID = 'cookie_generator'
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
     
    cmds.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True)
    
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 150), (2, 100), (3, 60)], 
        columnOffset=[(1, 'right', 1)])
    
    # user field: number of chips, default 20
    cmds.text(label='Number of Chips:')
    num_of_chips = cmds.intField(value=20)
    cmds.separator(h=20, style='none')
    
    # user field: size of chip, percent of diameter
    cmds.text(label='Chip Size:')
    chip_size = cmds.floatField(value=0.2)
    cmds.separator(h=10, style='none')
    
    # notice: be sure cookie object is selected before applying
    cmds.text(label='Select cookie object')
    cmds.text(label='before applying')
    cmds.separator(h=10, style='none')
    
    # padding
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    
    cmds.separator(h=10, style='none')
    
    # apply button
    cmds.button(label='Apply', command=functools.partial(pApplyCallback, 
        num_of_chips, chip_size, iter))
    
    iter += 1
    
    # simple cancel function: closes window and does nothing
    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
    
    # cancel button
    cmds.button(label='Cancel', command=cancelCallback)
    
    #open window
    cmds.showWindow()

# runs script from user give parameters
def applyCallback(num_of_chips_field, chip_size_field, iter, *pArgs):
   
   # get cookie from selection list
    selectionList = cmds.ls(orderedSelection = True)
    
    if (len(selectionList) < 1):
        raise ValueError('Please select bounding cookie object')
    
    cookie = selectionList[0]
        
    # grab user given parameters, initialize layer group
    num_of_chips = cmds.intField(num_of_chips_field, query=True, value=True)
    chip_size = cmds.floatField(chip_size_field, query=True, value=True)
    chips = cmds.group(empty=True, name='chips_grp#')
    
    count = 1
    
    # get bounds from cookie
    bounds = cmds.xform(cookie, q=1, os=1, bb=1)
    
    # calculate representative size variable
    x_diameter = abs(bounds[3] - bounds[0])
    y_diameter = abs(bounds[4] - bounds[1])
    z_diameter = abs(bounds[5] - bounds[2])
    size = (x_diameter + y_diameter + z_diameter) / 3
  	
  	# create instance object for bounds
    if (not(cmds.objExists(cookie + '_constr'))):
        cookie_constr = cmds.instance(cookie, name=cookie + '_constr')
        cmds.scale(x_diameter * 0.4, y_diameter * 0.5, z_diameter * 0.4, cookie + '_constr')
        cmds.hide(cookie + '_constr')
    
    bounds = cmds.xform(cookie + '_constr', q=1, os=1, bbi = 1)
    
    # create chips 
    for i in range(num_of_chips):
        chip = Chip(size, chip_size, count, chips)
        chip.smooth(count)
        chip.change(bounds, count, cookie)
        pcore.rename('chip{}'.format(count), 'chip_iter{}_chip{}'.format(iter, count)) 
        count+= 1
    
    # center pivots
    cmds.xform(chips, centerPivots = True)
            
createUI('Import_Cookies', applyCallback)