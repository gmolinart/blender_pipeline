import bpy
from cgl.plugins.blender import lumbermill as lm

class CorrectFileName(bpy.types.Operator):
    """
    Saves the file with the system defualt proper name
    """
    bl_idname = 'object.correct_file_name'
    bl_label = 'CorrectFileName'

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    path_object = lm.scene_object()
    lm.save_file_as(path_object.copy(set_proper_filename=True).path_root)
    print('filename fixed')

