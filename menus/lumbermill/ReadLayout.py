import bpy
import json
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils

class ReadLayout(bpy.types.Operator):
    """
    reads in the current scene layout.
    """
    bl_idname = 'object.read_layout'
    bl_label = 'Read Layout'

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    utils.read_layout()