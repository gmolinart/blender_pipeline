import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils
class ReadLayoutFromSelected(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.read_layout_from_selected'
    bl_label = 'Read Layout From Selected'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}

def return_asset_name(object):
    if 'proxy' in object.name:
        name = object.name.split('_')[0]
        return name

    else:
        if '.' in object.name:

            name = object.name.split('.')[0]
        else:
            name = object.name

        return name


def get_lib_from_object(object):
    if not object.is_instancer:
        object = bpy.data.object[return_asset_name(object)]
    library = object.instance_collection.library

    return (library)


def return_lib_path(library):
    from pathlib import Path
    print(library)
    library_path = bpy.path.abspath(library.filepath)
    filename = Path(bpy.path.abspath(library_path)).__str__()
    return (filename)

def run():
    import os
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    object = bpy.context.object

    if object :
        library= get_lib_from_object(object)
        path = return_lib_path(library)
        path_object = lm.LumberObject(path)
        json = path_object.copy(ext='json').path_root
        if os.path.isfile(json):
            utils.read_layout(outFile=json)
            bpy.ops.object.setup_collections()
    else:
        lm.confirm_prompt(message='please select an object')
