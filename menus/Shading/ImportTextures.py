import bpy
# from cgl.plugins.blender import alchemy as alc

class ImportTextures(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.import_textures'
    bl_label = 'Import Textures'

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
    from cgl.plugins.blender import alchemy as alc
    alc.import_task('tex')

