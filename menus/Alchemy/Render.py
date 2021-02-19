import bpy
from cgl.plugins.blender import alchemy as alc

class Render(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.render'
    bl_label = 'Render'


    def execute(self, context):
        run()
        return {'FINISHED'}


def switch_overlays(visible=False):
    for window in bpy.context.window_manager.windows:
        screen = window.screen

        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.overlay.show_overlays = visible
def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    #switch_overlays(visible=False)
    previewRenderTypes = ['anim', 'rig', 'mdl', 'lay','grmt', 'remsh']
    if alc.scene_object().task in previewRenderTypes:


        alc.render(preview=True)

    else:
        alc.render()


