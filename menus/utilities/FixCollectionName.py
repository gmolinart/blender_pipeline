import bpy

from cgl.plugins.blender import alchemy as alc


class FixCollectionName(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.fix_collection_name'
    bl_label = 'Fix Collection Name'

    def execute(self, context):
        run()
        return {'FINISHED'}


def rename_collection(current_scene = None):

    if current_scene == None:
        current_scene = alc.scene_object()

    if current_scene.scope == 'assets':
        name = current_scene.asset
    else:
        name = current_scene.filename_base


    obj = bpy.context.object

    if obj:
        if current_scene.asset in bpy.data.collections:
            print('collection exist ')
        object = bpy.context.object
        object.users_collection[0].name = name

    else:
        if current_scene.asset in bpy.data.collections:
            print('collection exist')

        else:
            bpy.data.collections['Collection'].name = name



def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    rename_collection()
