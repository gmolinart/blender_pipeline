import bpy
from cgl.plugins.blender import lumbermill as lm


class SetupRigTest(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.setup_rig_test'
    bl_label = 'SetupRigTest'

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
    bpy.ops.object.get_default_action()
    bpy.ops.object.get_default_camera()

    print('Hello World!: button_template')

