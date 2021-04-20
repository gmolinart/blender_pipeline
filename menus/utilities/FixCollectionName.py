import bpy

from cgl.plugins.blender import alchemy as alc
from cgl.plugins.blender.utils import rename_collection


class FixCollectionName(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.fix_collection_name'
    bl_label = 'Fix Collection Name'

    def execute(self, context):
        run()
        return {'FINISHED'}




def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    rename_collection()
