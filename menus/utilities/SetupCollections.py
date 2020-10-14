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


def reparent_linked_environemnt_assets(library):
    env = library
    bpy.ops.file.make_paths_absolute()
    env_path = lm.LumberObject(env.filepath)
    env_layout = env_path.copy(ext='json').path_root

    data = load_json(env_layout)
    assets_collection_name = '{}_assets'.format(env_path.asset)
    if assets_collection_name not in bpy.data.collections['env'].children:

        assets_collection = bpy.data.collections.new(assets_collection_name)
        bpy.data.collections['env'].children.link(assets_collection)
    else:
        assets_collection = bpy.data.collections[assets_collection_name]

    for i in data:
        print(i)
        name = data[i]['name']

        if i in bpy.data.objects:
            obj = bpy.data.objects[i]
            if assets_collection not in obj.users_collection:
                assets_collection.objects.link(obj)

            keep_single_user_collection(obj, assetName=assets_collection_name)


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
                print(11111111111111)
                print(collection)
                print(collection.library)
                if collection.library:

                    path_object = lm.LumberObject(collection.library.filepath)

                    create_collection(path_object.type)
                    for collection in bpy.data.collections:

                        if collection.name == path_object.type:
                            # print(collection.name )

                            if collection not in obj.users_collection:
                                collection.objects.link(obj)

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
            reparent_linked_environemnt_assets(lib)

    bpy.ops.file.make_paths_relative()


#run()