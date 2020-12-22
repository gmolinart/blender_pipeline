import bpy
from cgl.plugins.blender import lumbermill as lm

class RenderToSource(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.render_to_source'
    bl_label = 'Render To Source'

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

    scene = lm.scene_object()
    current_source = scene.copy(context='render', filename=None, ext=None).path_root
    current_render = scene.copy(context='source', filename=None, ext=None).path_root
    cgl_copy(current_source,current_render)

