# LSystemInstanceNode.py
#   Produces random locations to be used with the Maya instancer node.

import sys
import LSystem
import random

import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import maya.mel as mel

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
kPluginNodeTypeName1 = "LSystemInstanceNode"
kPluginNodeTypeName2 = "randomNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
LSystemInstanceNodeId = OpenMaya.MTypeId(0x8718)
randomNodeId = OpenMaya.MTypeId(0x8704)

'''
======================================================================================================================
LSYSTEM NODE
======================================================================================================================
'''
# Node definition
class LSystemInstanceNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    angle = OpenMaya.MObject()
    step = OpenMaya.MObject()
    file = OpenMaya.MObject()
    iterations = OpenMaya.MObject()
    branches = OpenMaya.MObject()
    flowers = OpenMaya.MObject()
    lsystem = LSystem.LSystem()

    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    # compute
    def compute(self,plug,data):
        if (plug == LSystemInstanceNode.branches or plug == LSystemInstanceNode.flowers):
            # get parameters
            iterations = data.inputValue(LSystemInstanceNode.iterations).asInt()
            angle = data.inputValue(LSystemInstanceNode.angle).asFloat()
            step = data.inputValue(LSystemInstanceNode.step).asFloat()
            file = data.inputValue(LSystemInstanceNode.file).asString()

            # update lsystem
            if (angle != LSystemInstanceNode.lsystem.getDefaultAngle()):
                LSystemInstanceNode.lsystem.setDefaultAngle(angle)
            if (step != LSystemInstanceNode.lsystem.getDefaultStep()):
                LSystemInstanceNode.lsystem.setDefaultStep(step)

            LSystemInstanceNode.lsystem.loadProgram(file.encode())

            # instantiate branches output object
            branches = data.outputValue(LSystemInstanceNode.branches)
            branchesAAD = OpenMaya.MFnArrayAttrsData()
            branchesObject = branchesAAD.create()
            branchesPosArray = branchesAAD.vectorArray("position")
            branchesIdArray = branchesAAD.doubleArray("id")
            branchesScaleArray = branchesAAD.vectorArray("scale")
            branchesOrientArray = branchesAAD.vectorArray("aimDirection")

            # instantiate flowers output object
            flowers = data.outputValue(LSystemInstanceNode.flowers)
            flowersAAD = OpenMaya.MFnArrayAttrsData()
            flowersObject = flowersAAD.create()
            flowersPosArray = flowersAAD.vectorArray("position")
            flowersIdArray = flowersAAD.doubleArray("id")
            flowersScaleArray = flowersAAD.vectorArray("scale")

            # execute LSystem
            branchesVec = LSystem.VectorPyBranch()
            flowersVec = LSystem.VectorPyBranch()

            LSystemInstanceNode.lsystem.processPy(iterations, branchesVec, flowersVec)

            # branches output
            for branch in branchesVec:
                midX = (branch[0] + branch[3]) / 2
                midY = (branch[2] + branch[5]) / 2
                midZ = (branch[4] + branch[1]) / 2
                branchesPosArray.append(OpenMaya.MVector(midX, midY, midZ))
                vecX = branch[3] - branch[0]
                vecZ = branch[4] - branch[1]
                vecY = branch[5] - branch[2]
                vecBranch = OpenMaya.MVector(vecX, vecY, vecZ)
                radius = LSystemInstanceNode.lsystem.getDefaultStep() * 0.1
                branchesScaleArray.append(OpenMaya.MVector(vecBranch.length(), radius, radius))
                branchesOrientArray.append(OpenMaya.MVector(vecX, vecY, vecZ))

            # flowers output
            for flower in flowersVec:
                flowersPosArray.append(OpenMaya.MVector(flower[0], flower[2], flower[1]))
                scale = LSystemInstanceNode.lsystem.getDefaultStep() * 0.2
                flowersScaleArray.append(OpenMaya.MVector(scale, scale, scale))

            branches.setMObject(branchesObject)
            flowers.setMObject(flowersObject)

            data.setClean(plug)

# initializer
def nodeInitializerLSystem():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    LSystemInstanceNode.angle = nAttr.create('angle', 'a', OpenMaya.MFnNumericData.kFloat,
                                             LSystemInstanceNode.lsystem.getDefaultAngle())
    MAKE_INPUT(nAttr)

    LSystemInstanceNode.step = nAttr.create('step', 's', OpenMaya.MFnNumericData.kFloat,
                                            LSystemInstanceNode.lsystem.getDefaultStep())
    MAKE_INPUT(nAttr)

    LSystemInstanceNode.file = tAttr.create('file', 'g', OpenMaya.MFnData.kString)
    MAKE_INPUT(tAttr)

    LSystemInstanceNode.iterations = nAttr.create('iterations', 'i', OpenMaya.MFnNumericData.kInt, 1)
    MAKE_INPUT(nAttr)

    LSystemInstanceNode.branches = tAttr.create('branches', 'b', OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)

    LSystemInstanceNode.flowers = tAttr.create('flowers', 'f', OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)

    try: # add attributes and attribute affects
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.angle)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.step)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.file)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.iterations)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.branches)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.flowers)

        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.angle, LSystemInstanceNode.branches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.step, LSystemInstanceNode.branches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.file, LSystemInstanceNode.branches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.iterations, LSystemInstanceNode.branches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.angle, LSystemInstanceNode.flowers)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.step, LSystemInstanceNode.flowers)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.file, LSystemInstanceNode.flowers)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.iterations, LSystemInstanceNode.flowers)

        print "Initialization!\n"

    except:
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginNodeTypeName1) )

# creator
def nodeCreatorLSystem():
    return OpenMayaMPx.asMPxPtr( LSystemInstanceNode() )


'''
======================================================================================================================
RANDOM NODE
======================================================================================================================
'''

class randomNode(OpenMayaMPx.MPxNode):
    # Declare class variables
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
    def compute(self, plug, data):
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
def nodeInitializerRandom():
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
def nodeCreatorRandom():
    return OpenMayaMPx.asMPxPtr( randomNode() )


'''
======================================================================================================================
INITIALIZE
======================================================================================================================
'''

# initialize the script plug-in
def initializePlugin(mobject):
    # Create menu
    buildMenu = "if (`menu -exists LSystemInstance`) { deleteUI LSystemInstance; }; "
    buildMenu += "menu -parent MayaWindow -label \"LSystemInstance\" -tearOff true LSystemInstance; "
    mel.eval(buildMenu)

    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    # load randomNode commands
    try:
        mplugin.registerNode(kPluginNodeTypeName2, randomNodeId, nodeCreatorRandom, nodeInitializerRandom)

        # default randomNode network
        defaultRandom = "polySphere; hide; instancer; createNode randomNode; "
        defaultRandom += "connectAttr pSphere1.matrix instancer1.inputHierarchy[0]; "
        defaultRandom += "connectAttr randomNode1.outPoints instancer1.inputPoints; "
        cmds.menuItem(label="RandomNode Default",
                      parent="MayaWindow|LSystemInstance",
                      command=defaultRandom, sourceType="mel")

        # custom randomNode network
        customRandom = "$selection = `ls -selection`; "
        customRandom += "if(size($selection) != 1) { error \"Select one object\"; }; "
        customRandom += "hide; instancer; createNode randomNode; "
        customRandom += "connectAttr ($selection[0] + \".matrix\") instancer1.inputHierarchy[0]; "
        customRandom += "connectAttr randomNode1.outPoints instancer1.inputPoints; "
        cmds.menuItem(label="RandomNode Selection",
                      parent="MayaWindow|LSystemInstance",
                      command=customRandom,
                      sourceType="mel")

    except:
        sys.stderr.write("Failed to register node: %s\n" % kPluginNodeTypeName2)

    # load LSystem commands
    try:
        mplugin.registerNode(kPluginNodeTypeName1, LSystemInstanceNodeId, nodeCreatorLSystem, nodeInitializerLSystem)

        # default LSystem network
        defaultLSystem = "polyCube; instancer; createNode LSystemInstanceNode; "
        defaultLSystem += "connectAttr pCube1.matrix instancer1.inputHierarchy[0]; "
        defaultLSystem += "connectAttr LSystemInstanceNode1.branches instancer1.inputPoints; "
        defaultLSystem += "polySphere; instancer; "
        defaultLSystem += "connectAttr pSphere1.matrix instancer2.inputHierarchy[0]; "
        defaultLSystem += "connectAttr LSystemInstanceNode1.flowers instancer2.inputPoints; "
        defaultLSystem += "select -add pCube1; "
        defaultLSystem += "hide; "
        cmds.menuItem(label="LSystem Default",
                      parent="MayaWindow|LSystemInstance",
                      command=defaultLSystem, sourceType="mel")

        # custom LSystem network
        customLSystem = "$selection = `ls -selection`; hide; "
        customLSystem += "if(size($selection) != 2) { error \"Select two objects (branches, flowers)\"; }; "
        customLSystem += "instancer; createNode LSystemInstanceNode; "
        customLSystem += "connectAttr ($selection[0] + \".matrix\") instancer1.inputHierarchy[0]; "
        customLSystem += "connectAttr LSystemInstanceNode1.branches instancer1.inputPoints; "
        customLSystem += "instancer; "
        customLSystem += "connectAttr ($selection[1] + \".matrix\") instancer2.inputHierarchy[0]; "
        customLSystem += "connectAttr LSystemInstanceNode1.flowers instancer2.inputPoints; "
        cmds.menuItem(label="LSystem Custom",
                      parent="MayaWindow|LSystemInstance",
                      command=customLSystem,
                      sourceType="mel")
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName1 )




# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(randomNodeId)
    except:
        sys.stderr.write("Failed to unregister node: %s\n" % kPluginNodeTypeName2)

    try:
        mplugin.deregisterNode( LSystemInstanceNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName1 )



    buildMenu = "if (`menu -exists LSystemInstance`) { deleteUI LSystemInstance; }; "
    mel.eval(buildMenu)
