import bpy
from cgl.plugins.blender import alchemy as alc
from cgl.plugins.blender.main_window import CGLumberjack
class Launch(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.launch'
    bl_label = 'Launch'


    def execute(self, context):
        run()
        return {'FINISHED'}



def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    alc.launch()

