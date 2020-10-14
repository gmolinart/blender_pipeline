import bpy
from cgl.plugins.blender import lumbermill as lm

class Review(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.review'
    bl_label = 'Review'

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    lm.review()

