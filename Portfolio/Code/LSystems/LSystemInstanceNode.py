# LSystemInstanceNode.py
#   Produces random locations to be used with the Maya instancer node.

import sys
import LSystem

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
kPluginNodeTypeName = "LSystemInstanceNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
LSystemInstanceNodeId = OpenMaya.MTypeId(0x8718)

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
def nodeInitializer():
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
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginNodeTypeName) )

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( LSystemInstanceNode() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, LSystemInstanceNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( LSystemInstanceNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
