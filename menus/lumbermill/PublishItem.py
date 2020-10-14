import bpy
from  cgl.plugins.blender import lumbermill as lm

class PublishItem(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.publish_item'
    bl_label = 'Publish Item'

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
    scene = lm.scene_object()

    if scene.context == 'source':
        if scene.resolution == 'high':
            lm.launch_preflight()


        else:
            lm.confirm_prompt(message="This is a low resolution version , please publish high file")

    else:
        lm.confirm_prompt(message="files in the render context shouldn't be published please switch to source file")

