import bpy
# from cgl.plugins.blender import lumbermill as lm

class UpdateShotShaders(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.update_shot_shaders'
    bl_label = 'Update Shot Shaders'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
    """
    updates teh shot shaders
    :return:
    """
