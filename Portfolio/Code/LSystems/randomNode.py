# randomNode.py
#   Produces random locations to be used with the Maya instancer node.

import sys
import random

import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

# Useful functions for declaring attributes as inputs or outputs.
def MAKE_INPUT(attr):
    attr.setKeyable(True)
    attr.setStorable(True)
    attr.setReadable(True)
    attr.setWritable(True)
def MAKE_OUTPUT(attr):
    attr.setKeyable(False)
    attr.setStorable(False)
    attr.setReadable(True)
    attr.setWritable(False)

# Define the name of the node
kPluginNodeTypeName = "randomNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
randomNodeId = OpenMaya.MTypeId(0x8704)

# Node definition
class randomNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # TODO:: declare the input and output class variables
    #         i.e. inNumPoints = OpenMaya.MObject()
    inNumPoints = OpenMaya.MObject()
    inXMax = OpenMaya.MObject()
    inYMax = OpenMaya.MObject()
    inZMax = OpenMaya.MObject()
    inXMin = OpenMaya.MObject()
    inYMin = OpenMaya.MObject()
    inZMin = OpenMaya.MObject()
    inMax = OpenMaya.MObject()
    inMin = OpenMaya.MObject()
    outPoints = OpenMaya.MObject()
    
    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    # compute
    def compute(self,plug,data):
        # TODO:: create the main functionality of the node. Your node should 
        #         take in three floats for max position (X,Y,Z), three floats 
        #         for min position (X,Y,Z), and the number of random points to
        #         be generated. Your node should output an MFnArrayAttrsData 
        #         object containing the random points. Consult the homework
        #         sheet for how to deal with creating the MFnArrayAttrsData.
        if (plug == randomNode.outPoints):
            pointsData = data.outputValue(randomNode.outPoints)
            pointsAAD = OpenMaya.MFnArrayAttrsData()
            pointsObject = pointsAAD.create()

            positionArray = pointsAAD.vectorArray("position")
            idArray = pointsAAD.doubleArray("id")


            for i in range(data.inputValue(randomNode.inNumPoints).asInt()):
                x = random.uniform(data.inputValue(randomNode.inXMin).asFloat(),
                                   data.inputValue(randomNode.inXMax).asFloat())
                y = random.uniform(data.inputValue(randomNode.inYMin).asFloat(),
                                   data.inputValue(randomNode.inYMax).asFloat())
                z = random.uniform(data.inputValue(randomNode.inZMin).asFloat(),
                                   data.inputValue(randomNode.inZMax).asFloat())
                positionArray.append(OpenMaya.MVector(x, y, z))
                idArray.append(i)

            pointsData.setMObject(pointsObject)
            data.setClean(plug)

    
# initializer
def nodeInitializer():
    # TODO:: initialize the input and output attributes. Be sure to use the
    #         MAKE_INPUT and MAKE_OUTPUT functions.

    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    randomNode.inNumPoints = nAttr.create('inNumPoints', 'n', OpenMaya.MFnNumericData.kInt, 0)
    MAKE_INPUT(nAttr)

    randomNode.inXMax = nAttr.create('inXMax', 'xa', OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.inYMax = nAttr.create('inYMax', 'ya', OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.inZMax = nAttr.create('inZMax', 'za', OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)

    randomNode.inMax = nAttr.create('inMax', 'ma', randomNode.inXMax, randomNode.inYMax, randomNode.inZMax)
    MAKE_INPUT(nAttr)

    randomNode.inXMin = nAttr.create('inXMin', 'xi', OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.inYMin = nAttr.create('inYMin', 'yi', OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.inZMin = nAttr.create('inZMin', 'zi', OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)

    randomNode.inMin = nAttr.create('inMin', 'mi', randomNode.inXMin, randomNode.inYMin, randomNode.inZMin)
    MAKE_INPUT(nAttr)

    randomNode.outPoints = tAttr.create('outPoints', 'op', OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)

    try:
        # TODO:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)
        randomNode.addAttribute(randomNode.inNumPoints)
        randomNode.addAttribute(randomNode.inMax)

        randomNode.addAttribute(randomNode.inMin)
        randomNode.addAttribute(randomNode.outPoints)

        randomNode.attributeAffects(randomNode.inNumPoints, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.inMax, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.inMin, randomNode.outPoints)

        print "Initialization!\n"

    except:
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginNodeTypeName) )

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( randomNode() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, randomNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( randomNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
