import bpy
from cgl.plugins.blender import alchemy as alc


class SplitScene(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.split_scene'
    bl_label = 'Split Scene'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}




def get_characters():
    characters = []
    for collection in bpy.data.collections:
        if 'char_' in collection.name:
            characters.append(collection.name)


    print(characters)
    return (characters)


def get_division_list():
    division_list = ['env', 'props']

    for obj in get_characters():
        division_list.append(obj)

    return division_list


def get_scene_name(item):
    scene_name = "{}_{}".format(alc.scene_object().filename_base, item)
    return (scene_name)


def split_scene():
    division_list = get_division_list()

    for i in division_list:
        print(i)
        bpy.ops.scene.new(type='LINK_COPY')
        bpy.context.scene.name = get_scene_name(i)

        bpy.context.window.scene = bpy.data.scenes[alc.scene_object().filename_base]


def keep_single_user_collection(obj, assetName=None):
    if not assetName:
        assetName = alc.scene_object().shot

    try:
        bpy.data.collections[assetName].objects.link(obj)

    except(RuntimeError):
        pass

    for collection in obj.users_collection:
        if collection.name != assetName:
            collection.objects.unlink(obj)


def delete_elements():
    division_list = get_division_list()

    for i in division_list:
        bpy.context.window.scene = bpy.data.scenes[get_scene_name(i)]
        collections = bpy.context.scene.collection.children

        item_to_keep = i

        for collection in collections:
            print(collection)
            if not collection.name == item_to_keep:
                bpy.context.scene.collection.children.unlink(bpy.data.collections[collection.name])

        bpy.context.window.scene = bpy.data.scenes[alc.scene_object().filename_base]


def delete_duplicate_scenes():
    scenes = bpy.data.scenes
    for scene in scenes:
        if not scene.name == alc.scene_object().filename_base:
            bpy.context.window.scene = scene
            bpy.ops.scene.delete()


def cleanup_scene(assetName):
    '''
    :param assetname: collection that will be kepth
    '''

    if not assetName:
        assetName = alc.scene_object().shot

    rig_collection = bpy.data.collections[assetName]
    sceneName = alc.scene_object().filename_base
    scenes = []
    for scene in bpy.data.scenes:
        scenes.append(scene.name)

        if sceneName not in scenes:
            newScene = bpy.data.scenes.new(sceneName)

        else:
            newScene = bpy.data.scenes[sceneName]

    for scene in bpy.data.scenes:

        list_of_collections = []

        for collection in newScene.collection.children:
            list_of_collections.append(collection)

        if rig_collection not in list_of_collections:
            newScene.collection.children.link(rig_collection)

        if scene.name != sceneName:
            bpy.data.scenes.remove(scene)

    data = [bpy.data.objects,
            bpy.data.collections,
            bpy.data.materials,
            bpy.data.meshes,
            bpy.data.lights]

    for type in data:

        for obj in type:
            if obj.users < 1:
                type.remove(obj)

    for action in bpy.data.actions:
        bpy.data.actions.remove(action)

    scene_collections = bpy.context.scene.collection
    scene = alc.scene_object()

    if scene.type == 'prop':

        for lib in bpy.data.libraries:
            print(lib.name)

    for collection in scene_collections.children:
        if collection.name != assetName:
            print(collection.name)
            scene_collections.children.unlink(collection)


def purge():
    # print(C.area.spaces[0])
    type_orig, bpy.context.area.type = bpy.context.area.type, 'OUTLINER'
    # print(C.area.type)
    # print(C.area.spaces[0])
    bpy.context.area.spaces[0].display_mode = 'ORPHAN_DATA'
    bpy.ops.outliner.orphans_purge()
    bpy.context.area.type = type_orig


def create_collection(type, parent=None):
    if not parent:
        parent = bpy.context.scene.collection

    if type not in bpy.data.collections:
        bpy.data.collections.new(type)

    collection = bpy.data.collections[type]
    try:

        parent.children.link(collection)
    except(RuntimeError):
        print('{} collection already in scene'.format(type))
        pass


def keep_single_character():
    scene = bpy.context.scene

    if 'char' in scene.name:

        char = scene.name.split('_')[-1]
        for obj in get_characters():
            if not obj == char:
                bpy.data.objects[obj].hide_viewport = True




# purge()
def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    delete_duplicate_scenes()
    split_scene()
    delete_elements()

