import bpy
from cgl.plugins.blender import alchemy as alc
#from cgl.plugins.blender import utils
from cgl.plugins.blender.tasks.light import get_default_lighting
class Turntable(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.turntable'
    bl_label = 'Turntable'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}



def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:

    """
    if bpy.context.selected_objects:
        try:
            bpy.ops.object.delete_defaults()
            bpy.ops.object.delete_turntable()
        except AttributeError:
            print('no objects to delete')
        alc.create_turntable()
        get_default_lighting()

    else:
        alc.confirm_prompt(message='Please select geo')