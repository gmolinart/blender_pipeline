import bpy
from cgl.plugins.blender import alchemy as alc

class SwitchContext(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.switch_context'
    bl_label = 'Switch Context'



    def execute(self, context):
        run()
        return {'FINISHED'}


def switch_context():
    import os

    scene = alc.scene_object()

    if scene.context == 'source':

        newpath = scene.copy(context='render')

    else:
        newpath = scene.copy(context='source')

    if os.path.isdir(newpath.copy(filename='').path_root):

        alc.open_file(newpath.path_root)




    else:
        alc.confirm_prompt(message='ERROR no such directory')


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    switch_context()


