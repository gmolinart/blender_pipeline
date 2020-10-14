import bpy
from cgl.plugins.blender import lumbermill as lm

class BuildShot(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.build_shot'
    bl_label = 'Build Shot'


    def execute(self, context):
        run()
        return {'FINISHED'}



def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    buildShot(lm.scene_object().task)



