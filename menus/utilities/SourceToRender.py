
import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.core.utils.general import split_all, cgl_copy

class SourceToRender(bpy.types.Operator):
    """
    copies files in source directory to render
    """
    bl_idname = 'object.source_to_render'
    bl_label = 'Source To Render'

    def execute(self, context):
        run()
        return {'FINISHED'}






def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    scene = lm.scene_object()
    current_source = scene.copy(context='source', filename=None, ext=None).path_root
    current_render = scene.copy(context='render', filename=None, ext=None).path_root
    cgl_copy(current_source,current_render)