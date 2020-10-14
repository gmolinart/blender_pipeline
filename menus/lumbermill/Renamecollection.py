import bpy
from cgl.plugins.blender import lumbermill as lm

class Renamecollection(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.renamecollection'
    bl_label = 'Renamecollection'

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def rename_collection(current_scene= ''):

    if current_scene.scope == 'assets':
        rename = current_scene.asset
    else:
        rename = current_scene.filename_base

    if bpy.context.active_object:

        object = bpy.context.selected_objects[0]
        object.users_collection[0].name = rename
    else:
        if len(bpy.data.collections) == 1:


            try:
                bpy.data.collections[0].name = rename

            except KeyError:
                print('couldnt rename collection')

def run():
    """
    renames The collection inside of blender from the asset name 
    :return:
    """
   rename_collection(lm.scene_object())

