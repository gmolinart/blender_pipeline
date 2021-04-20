import bpy
from cgl.plugins.blender import alchemy as alc
from pathlib import Path

class OpenSelected(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.open_selected'
    bl_label = 'Open Selected'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def open_selected_library():
    obj = bpy.context.active_object
    from cgl.plugins.blender.msd import path_object_from_source_path
    library = obj['source_path']


    lumber_object = path_object_from_source_path(library)

    alc.save_file()

    import os
    os.startfile(lumber_object.copy(context ='source').path_root, 'open')

    #latestVersion = lumber_object.latest_version().path_root


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    open_selected_library()
