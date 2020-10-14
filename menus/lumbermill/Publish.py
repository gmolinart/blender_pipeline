import bpy
from cgl.plugins.blender import lumbermill as lm

class Publish(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.publish'
    bl_label = 'Publish'

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
    print('publish button pressed')

    scene = lm.scene_object()

    if scene.context == 'source':
        if scene.resolution == 'high':
            lm.launch_preflight()


        else:
            lm.confirm_prompt(message="This is a low resolution version , please edit source file")

    else:
        lm.confirm_prompt(message="files in the render context shouldn't be versioned up, please edit source file")


