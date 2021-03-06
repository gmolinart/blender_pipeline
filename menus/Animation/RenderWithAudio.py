import bpy
from cgl.plugins.blender import alchemy as alc

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
    from cgl.plugins.blender import alchemy as alc
    alc.render(preview=True, audio=True)

    scene = alc.scene_object()
    file_out = scene.copy(context = 'render').path_root.replace('/high/', '/high/.thumb')
    #alc.render(preview=True, file_out = file_out )


    print('Hello World!: button_template')

