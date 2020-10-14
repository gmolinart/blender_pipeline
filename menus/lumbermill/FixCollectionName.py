import bpy
from cgl.plugins.blender import lumbermill as lm

class FixCollectionName(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.fix_collection_name'
    bl_label = 'Fix Collection Name'

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    filepath = bpy.data.filepath
    path_object = lm.LumberObject(filepath)

    if bpy.context.object:

        object = bpy.context.object
        object.users_collection[0].name = path_object.asset
        print('Hello World!: button_template')
    else:

        if path_object.asset in bpy.data.collections:
            print('collection exist ')
        else:
            bpy.data.collections['Collection'].name = path_object.asset
