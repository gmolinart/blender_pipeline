import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.core.utils.read_write import load_json


class SetupCollections(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.setup_collections'
    bl_label = 'Setup Collections'

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def create_environment_objects_collection(asset):
    asset_collection_name = '{}_assets'.format(asset)
    if asset_collection_name in bpy.data.collections['env'].children:
        asset_collection = bpy.data.collections[asset_collection_name]

    else:
        asset_collection = bpy.data.collections.new(asset_collection_name)
        bpy.data.collections['env'].children.link(asset_collection)

    return asset_collection


def move_to_collection(objectName, asset_collection):
    if objectName in bpy.context.view_layer.objects:
        print(objectName)
        obj = bpy.data.objects[objectName]

        if objectName not in asset_collection.objects:
            if objectName in bpy.data.objects:
                asset_collection.objects.link(obj)

        keep_single_user_collection(obj, assetName=asset_collection.name)


def parent_linked_environment_assets(library):
    import os
    env = library
    bpy.ops.file.make_paths_absolute()
    env_path = lm.LumberObject(env.filepath)
    env_layout = env_path.copy(ext='json').path_root
    asset_collection = create_collection('env')

    if os.path.isfile(env_layout):
        data = load_json(env_layout)
        env_object_collection = create_environment_objects_collection(env_path.asset)

        for i in data:
            name = data[i]['name']
            print(44444444444)
            print(env_object_collection)
            move_to_collection(i, env_object_collection)
        print(env_path.asset)
        move_to_collection(env_path.asset, bpy.data.collections['env'])


def keep_single_user_collection(obj, assetName=None):
    if not assetName:
        assetName = lm.scene_object().shot

    try:
        bpy.data.collections[assetName].objects.link(obj)

    except(RuntimeError):
        pass

    for collection in obj.users_collection:
        if collection.name != assetName:
            collection.objects.unlink(obj)


def reparent_collections(view_layer):
    for obj in view_layer:

        if obj.instance_type == 'COLLECTION':
            if obj.instance_collection:

                collection = obj.instance_collection
                print(collection)
                print(collection.library)
                if collection.library:

                    path_object = lm.LumberObject(collection.library.filepath)

                    create_collection(path_object.type)
                    for collection in bpy.data.collections:

                        if collection.name == path_object.type:
                            # print(collection.name )

                            if collection not in obj.users_collection:
                                try:
                                    collection.objects.link(obj)
                                except RuntimeError:
                                    print(" Error: Could not link the object {} ".format(obj),
                                          "because one of it's collections is  is linked.")
                    unlink_collections(obj, path_object.type)

    for collection in bpy.context.scene.collection.children:
        if len(collection.objects) < 1:
            print(collection.name)
            bpy.context.scene.collection.children.unlink(collection)


def unlink_collections(obj, type):
    user_collections = obj.users_collection
    if len(obj.users_collection) > 1:
        for collection in user_collections:
            if collection.name != type:
                try:
                    print('unlinking {}   {}'.format(obj.name, type))
                    collection.objects.unlink(obj)
                except:
                    pass


def create_collection(type):
    if type not in bpy.data.collections:
        bpy.data.collections.new(type)

    collection = bpy.data.collections[type]
    try:

        bpy.context.scene.collection.children.link(collection)
    except(RuntimeError):
        print('{} collection already in scene'.format(type))
        pass


def parent_object(view_layer, type, obj_type):
    create_collection(type)
    collection = bpy.data.collections[type]
    for obj in view_layer:
        if obj.type == obj_type:
            try:
                collection.objects.link(obj)
            except(RuntimeError):
                print('{} already in light collection'.format(obj.name))

        unlink_collections(obj, type)


def return_lib_path(library):
    from pathlib import Path
    print(library)
    library_path = bpy.path.abspath(library.filepath)
    filename = Path(bpy.path.abspath(library_path)).__str__()
    return (filename)


def run():
    view_layer = bpy.context.scene.objects

    bpy.ops.file.make_paths_absolute()

    reparent_collections(view_layer)
    parent_object(view_layer, 'cam', 'CAMERA')
    parent_object(view_layer, 'light', 'LIGHT')
    parent_object(view_layer, 'gpencil', 'GPENCIL')
    parent_object(view_layer, 'armature', 'ARMATURE')
    for lib in bpy.data.libraries:
        type = lm.LumberObject(return_lib_path(lib)).type
        if type == 'env':
            print('________________________env library found:')
            print(lib)

            parent_linked_environment_assets(lib)

    bpy.ops.file.make_paths_relative()


if __name__ == "__main__":
    run()