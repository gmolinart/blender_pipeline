import bpy
from cgl.plugins.blender import lumbermill as lm


class UnlinkAsset(bpy.types.Operator):
    """
    Unlinks selected Object
    """
    bl_idname = 'object.unlink_asset'
    bl_label = 'Unlink Asset'

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

    for object in bpy.context.selected_objects:

        try:

            libname = object.data.library

        except AttributeError:
            libname = object.instance_collection

        if 'proxy' in bpy.context.object.name:
            name = bpy.context.object.name.split('_')[0]
        else:
            name = bpy.context.object.name

        obj = bpy.data.objects[name]
        bpy.data.batch_remove(ids=(libname, obj))

if __name__ == "__main__":
    run()