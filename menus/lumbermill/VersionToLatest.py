import bpy
from cgl.plugins.blender import lumbermill as lm
from pathlib import Path
import os


class VersionToLatest(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.version_to_latest'
    bl_label = 'Version To Latest'

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
    print(library)
    library_path = bpy.path.abspath(library.filepath)
    filename = Path(bpy.path.abspath(library_path)).__str__()
    return (filename)


def versionToLatest():
    selection = bpy.context.selected_objects
    if not selection:
        selection = bpy.data.libraries

    for obj in selection:

        if 'proxy' in obj.name:
            obj = bpy.data.objects[obj.name.replace('_proxy', '')]
            print(obj)
        library = get_lib_from_object(obj)
        filename = return_lib_path(library)
        print(filename)

        lumber_object = lm.LumberObject(filename)

        if os.path.isfile(lumber_object.copy(context='render').latest_version().path_root):
            latest_version = lumber_object.latest_version().copy(context='render')

        else:
            if os.path.isfile(lumber_object.copy(context='source').latest_version().path_root):
                latest_version = lumber_object.latest_version().copy(context='source')

            else:
                lm.confirm_prompt(message='folder empty, no version found, please check on lumbermill')

        library.filepath = bpy.path.relpath(latest_version.path_root)
        library.reload()

        lm.confirm_prompt(message='{} update to {}'.format(latest_version.asset, latest_version.version))


def run():
    """
    Version up of selected object to latest published version on the system.
    :return:
    """

    versionToLatest()


if __name__ == '__main__':
    run()


