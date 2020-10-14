import bpy
from cgl.plugins.blender import lumbermill as lm


class CleanupScene(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.cleanup_scene'
    bl_label = 'Cleanup Scene'
    assetName =  bpy.props.StringProperty()

    #    @classmethod
    #    def poll(cls, context):
    #        return context.active_object is not None

    def execute(self, context):
        run(self.assetName)
        return {'FINISHED'}


def cleanup_scene(assetName):
    '''
    :param assetname: collection that will be kepth
    '''

    if not assetName:
        assetName = lm.scene_object().shot

    rig_collection = bpy.data.collections[assetName]
    sceneName = lm.scene_object().filename_base
    scenes = []
    for scene in bpy.data.scenes:
        scenes.append(scene.name)

        if sceneName not in scenes:
            newScene = bpy.data.scenes.new(sceneName)

        else:
            newScene = bpy.data.scenes[sceneName]

    for scene in bpy.data.scenes:

        # override = bpy.context.copy()
        # override["area.type"] = ['OUTLINER']
        # override["display_mode"] = ['ORPHAN_DATA']
        # bpy.ops.outliner.orphans_purge(override)

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
    scene = lm.scene_object()

    if scene.type == 'prop':

        for lib in bpy.data.libraries:
            print(lib.name)

    for collection in scene_collections.children:
        if collection.name != assetName:
            print(collection.name)
            scene_collections.children.unlink(collection)


def run(assetName= ''):
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    cleanup_scene(assetName)
    print('cleanup complete')

