import bpy
from cgl.plugins.blender import alchemy as alc
from pathlib import Path
import os

from importlib import reload
from cgl.plugins.blender import utils

reload(utils)


class VersionToLatest(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'alchemy.version_to_latest'
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


def get_collection_from_path_object(path_object):
    import bpy

    list = []
    path_object_name = '{}_{}_{}:{}'.format(path_object.type, path_object.asset, path_object.variant, path_object.task)

    for i in bpy.data.collections:

        if i.name == path_object_name:

            if i.library.filepath.replace('\\', '/') == path_object.path_root:
                print()
                print('FOUnd_____________________')
                return (i)


def versionToLatest():
    from cgl.plugins.blender.utils import get_scene_collection, get_object, load_library, purge_unused_data, \
        set_all_paths_relative
    from cgl.plugins.blender.msd import tag_object
    from cgl.plugins.blender.msd import path_object_from_source_path, tag_object
    selection = bpy.context.selected_objects

    set_all_paths_relative(False)
    purge_unused_data()
    if not selection:
        selection = bpy.data.libraries

    for obj in selection:
        if obj.type == 'EMPTY':

            if 'proxy' in obj.name:
                obj = bpy.data.objects[obj.name.replace('_proxy', '')]
                print(obj)

            object = get_object(obj)
            try:
                library = object['source_path']
            except:
                print('ERROR ON {}'.format(obj))
                continue

            lumber_object = path_object_from_source_path(library)

            latest_version = lumber_object.latest_version().copy(context='render')

            print(latest_version.path_root)

            if latest_version.task == 'mdl':
                load_library(latest_version)

                collection = get_collection_from_path_object(path_object=latest_version)

                # print(222222222222222222)
                # print(collection)

                obj.instance_collection = collection
                tag_object(obj, 'source_path', latest_version.path)
            if latest_version.task == 'rig':
                library = obj.instance_collection.library
                library.filepath = latest_version.path_root
                library.reload()
            tag_object(obj, 'source_path', latest_version.path)

    set_all_paths_relative(True)
    alc.confirm_prompt(message='{} update to {}'.format(latest_version.asset, latest_version.version))


def run():
    """
    Version up of selected object to latest published version on the system.
    :return:
    """

    versionToLatest()


if __name__ == '__main__':
    run()


