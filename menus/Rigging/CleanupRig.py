import bpy
from cgl.plugins.blender import lumbermill as lm

class CleanupRig(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.cleanup_rig'
    bl_label = 'Cleanup Rig'

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def cleanup_scene():
    "deletes all unecesary info "

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

        #override = bpy.context.copy()
        #override["area.type"] = ['OUTLINER']
        #override["display_mode"] = ['ORPHAN_DATA']
        #bpy.ops.outliner.orphans_purge(override)

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


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    cleanup_scene()
    print('cleanup complete')


