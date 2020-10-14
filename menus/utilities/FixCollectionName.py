import bpy

from cgl.plugins.blender import lumbermill as lm


class FixCollectionName(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.fix_collection_name'
    bl_label = 'Fix Collection Name'

    def execute(self, context):
        run()
        return {'FINISHED'}


def rename_collection(current_scene):
    if current_scene.scope == 'assets':
        rename = current_scene.asset
    else:
        rename = current_scene.filename_base

    try:
        if rename not in bpy.data.collections:

            selected_objects = bpy.context.object
            bpy.data.collections[selected_objects.users_collection[0].name].name = rename

    except:
        if rename not in bpy.data.collections:
            if len(bpy.data.collections) == 1:
                try:
                    bpy.data.collections[0].name = rename

                except KeyError:
                    print('couldnt rename collection')


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    current_scene = lm.scene_object()
    rename_collection(current_scene)
