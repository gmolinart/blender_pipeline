import bpy
from cgl.plugins.blender import alchemy as alc

class FixMeshName(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.fix_mesh_name'
    bl_label = 'Fix Mesh Name'

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

    selection = bpy.context.selected_objects

    if not selection :
        alc.confirm_prompt(message='please select an object')
    for obj in selection:
        obj.data.name = '{}_mesh'.format(obj.name)

    alc.confirm_prompt(message='Mesh data renamed!')
