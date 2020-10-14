import bpy
from cgl.plugins.blender import lumbermill as lm
import os
class ExportToObj(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.export_to_obj'
    bl_label = 'Export To Obj'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}





def create_render_folder(scene):
    render_folder = scene.copy(context='render', filename='').path_root

    if not os.path.isdir(render_folder):
        os.makedirs(render_folder)


def export_obj(selected):
    scene = lm.scene_object()
    obj_path = scene.copy(context='render', set_proper_filename=True, ext='obj')

    create_render_folder(scene)

    bpy.ops.export_scene.obj(filepath=obj_path.path_root, use_selection=selected)





def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    export_obj(True)

