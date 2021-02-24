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


    if 'proxy' in obj.name:
        name = obj.name.split('_')[0]
    elif ':' in obj.name:
        name = obj.name.split(':')[0]
    else:
        if '.' in obj.name:
            name = obj.name.split('.')[0]
        else:

            name = obj.name

    library = bpy.data.collections[name].library
    libraryPath = bpy.path.abspath(library.filepath)
    filename = Path(bpy.path.abspath(libraryPath)).__str__()

    lumber_object = alc.PathObject(filename)
    alc.save_file()
    alc.open_file(lumber_object.copy(context = 'source').path_root)
    #latestVersion = lumber_object.latest_version().path_root


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    open_selected_library()
