import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.core.utils.read_write import load_json


class UnlinkAsset(bpy.types.Operator):
    """
    Unlinks selected Object
    """
    bl_idname = 'object.unlink_asset'
    bl_label = 'Unlink Asset'

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        remove_unused_libraries()
        return {'FINISHED'}


def remove_unused_libraries():
    libraries = bpy.data.libraries

    objects = bpy.data.objects

    obj_to_delete = []
    libraries_in_scene = []

    for obj in objects:
        if obj.is_instancer:
            if obj.instance_collection == None:
                if 'instancer' not in obj.name:
                    obj_to_delete.append(obj)
            else:
                lib = obj.instance_collection.library
                libraries_in_scene.append(lib)

    for lib in bpy.data.libraries:
        if lib not in libraries_in_scene:
            obj_to_delete.append(lib)

    print(obj_to_delete)
    bpy.data.batch_remove(ids=(obj_to_delete))

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


def remove_linked_environment_dependencies(library):
    env = library
    bpy.ops.file.make_paths_absolute()
    env_path = lm.LumberObject(env.filepath)
    env_layout = env_path.copy(ext='json').path_root

    data = load_json(env_layout)

    for i in data:
        print(i)
        name = data[i]['name']

        if i in bpy.data.objects:
            obj = bpy.data.objects[i]
            unlink_asset(obj)
    try:
        env_asset_collection = bpy.data.collections['{}_assets'.format(env_path.asset)]
        bpy.data.collections.remove(env_asset_collection)
    except KeyError:
        pass


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    for object in bpy.context.selected_objects:
        unlink_asset(object)

    remove_unused_libraries()


if __name__ == "__main__":
    run()