import bpy
from cgl.plugins.blender import alchemy as alc
from cgl.plugins.blender.tasks.light import get_default_lighting
class DefaultLightSetup(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.default_light_setup'
    bl_label = 'Default Light Setup'

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}



def run():
    get_default_lighting()
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
