import bpy
# from cgl.plugins.blender import lumbermill as lm

class DeleteDefaults(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.delete_defaults'
    bl_label = 'Delete Defaults'



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

    for collection in bpy.data.collections:
        if 'DEFAULT' in collection.name:
            bpy.data.collections.remove(collection)





    print('Defaults deleted')

