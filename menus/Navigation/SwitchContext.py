import bpy
from cgl.plugins.blender import lumbermill as lm

class SwitchContext(bpy.types.Operator):
    """
    Switches from source to render and reverse
    """
    bl_idname = 'object.switch_context'
    bl_label = 'Switch Context'



    def execute(self, context):
        run()
        return {'FINISHED'}


def switch_context():
    import os

    scene = lm.scene_object()

    if scene.context == 'source':

        newpath = scene.copy(context='render')

    else:
        newpath = scene.copy(context='source')

    if os.path.isdir(newpath.copy(filename='').path_root):

        lm.open_file(newpath.path_root)




    else:
        lm.confirm_prompt(message='ERROR no such directory')


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    switch_context()


