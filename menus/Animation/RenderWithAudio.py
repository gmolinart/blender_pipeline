import bpy
# from cgl.plugins.blender import lumbermill as lm

class RenderWithAudio(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.render_with_audio'
    bl_label = 'Render With Audio'

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

    lm.render(preview=True, audio=True)

    print('Hello World!: button_template')

