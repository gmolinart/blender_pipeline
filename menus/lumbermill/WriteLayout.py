import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils




class WriteLayout(bpy.types.Operator):
    """
    Writes out the current scene to a json file
    """
    bl_idname = 'object.write_layout'
    bl_label = 'Write Layout'


    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
    """
    Writes out the current scene to a json file
    :return:
    """
    utils.write_layout()
