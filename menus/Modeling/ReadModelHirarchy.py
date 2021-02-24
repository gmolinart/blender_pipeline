import bpy
from cgl.plugins.blender.alchemy.mdl import read_model_hirarchy

class ReadModelHirarchy(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.read_model_hirarchy'
    bl_label = 'Read Model Hirarchy'

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
    read_model_hirarchy()
