import bpy
from cgl.plugins.blender import lumbermill as lm

class ShowInFolder(bpy.types.Operator):
    """
    Opens current file in explorer
    """
    bl_idname = 'object.show_in_folder'
    bl_label = 'Show In Folder'

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    print('Hello World!: button_template')
    scene = lm.scene_object()
    scene.show_in_folder()

