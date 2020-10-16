# from cgl.plugins.blender import utils
import bpy
from cgl.core.utils.read_write import load_json
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.preflight.preflight_check import PreflightCheck


def unlink_asset(object):
    filepath = None

    try:
        libname = object.data.library
    except AttributeError:
        for lib in bpy.data.libraries:
            libname = object.instance_collection

    print('_________unlinking__________')
    print(object)

    if 'proxy' in object.name:
        name = object.name.split('_')[0]
    else:
        name = object.name

    obj = bpy.data.objects[name]

    if not libname:
        bpy.data.batch_remove(ids=([obj]))
    else:
        try:
            filepath = libname.library.filepath

        except AttributeError:
            pass
        if filepath and lm.PathObject(filepath).type == 'env':
            remove_linked_environment_dependencies(libname.library)

        bpy.data.batch_remove(ids=(libname, obj))
        remove_unused_libraries()


def remove_linked_environment_dependencies(library):
    env = library
    bpy.ops.file.make_paths_absolute()
    env_path = lm.LumberObject(env.filepath)
    env_layout = env_path.copy(ext='json').path_root
    env_asset_collection = bpy.data.collections['{}_assets'.format(env_path.asset)]
    data = load_json(env_layout)

    for i in data:
        print(i)
        name = data[i]['name']

        if i in bpy.data.objects:
            obj = bpy.data.objects[i]
            unlink_asset(obj)
    try:

        bpy.data.collections.remove(env_asset_collection)
    except KeyError:
        pass


def remove_unused_libraries():
    libraries = bpy.data.libraries

    objects = bpy.data.objects
    instancers = []

    libraries_in_scene = []

    for obj in objects:
        if obj.is_instancer:
            instancers.append(obj)

    try:
        for i in instancers:
            lib = i.instance_collection.library
            if lib not in libraries_in_scene:
                libraries_in_scene.append(lib)

        for lib in libraries:
            if lib not in libraries_in_scene:
                print(lib)
                # bpy.data.libraries.remove(lib)
                bpy.data.batch_remove(ids=(lib,))
    except AttributeError:
        pass


def remove_instancers():
    for object in bpy.data.objects:

        filepath = None

        try:
            libname = object.data.library
        except AttributeError:
            for lib in bpy.data.libraries:
                libname = object.instance_collection

        print('_________unlinking__________')
        print(object)

        if 'proxy' in object.name:
            name = object.name.split('_')[0]
        else:
            name = object.name

        obj = bpy.data.objects[name]

        if not libname:
            bpy.data.batch_remove(ids=([obj]))
        else:
            try:
                filepath = libname.library.filepath

            except AttributeError:
                pass
     #       if filepath and lm.PathObject(filepath).type == 'env':
     #           remove_linked_environment_dependencies(libname.library)

     #       bpy.data.batch_remove(ids=(libname, obj))
            remove_unused_libraries()


class RemoveLinkedAssets(PreflightCheck):

    def getName(self):
        pass

    def run(self):
        """
        script to be executed when the preflight is run.

        If the preflight is successful:
        self.pass_check('Message about a passed Check')

        if the preflight fails:
        self.fail_check('Message about a failed check')
        :return:
        """
        # set_viewer_active()
        #remove_instancers()
        print('Remove Linked Assets')
        self.pass_check('Check Passed')
        # self.fail_check('Check Failed')
