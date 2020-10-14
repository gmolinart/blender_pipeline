import bpy
# from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils
class RenameMaterials(bpy.types.Operator):
    """
    renames material base of the current object
    """
    bl_idname = 'object.rename_materials'
    bl_label = 'Rename Materials'


    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
    """
    :return:
    """
    for object in bpy.context.selected_objects:
        utils.rename_materials(selection=object.name)

