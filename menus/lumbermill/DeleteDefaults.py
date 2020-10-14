import bpy
# from cgl.plugins.blender import lumbermill as lm

class DeleteDefaults(bpy.types.Operator):
    """
    Deletes default elements in scene
    """
    bl_idname = 'object.delete_defaults'
    bl_label = 'DeleteDefaults'

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
    for object in bpy.data.objects:
        if 'DEFAULT' in object.name:
            bpy.data.objects.remove(object)
    print('Defaults deleted')

