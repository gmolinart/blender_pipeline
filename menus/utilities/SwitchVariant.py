import bpy
# from cgl.plugins.blender import alchemy as alc

class SwitchVariant(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.switch_variant'
    bl_label = 'Switch Variant'

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
    print('Hello World!: button_template')

