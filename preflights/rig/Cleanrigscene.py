from cgl.plugins.preflight.preflight_check import PreflightCheck
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils
import bpy



# def cleanup_scene():
#     "deletes all unecesary info "
#
#     assetName = lm.scene_object().shot
#     rig_collection = bpy.data.collections[assetName]
#     sceneName = lm.scene_object().filename_base
#     scenes = []
#     for scene in bpy.data.scenes:
#         scenes.append(scene.name)
#
#         if sceneName not in scenes:
#             newScene = bpy.data.scenes.new(sceneName)
#
#         else:
#             newScene = bpy.data.scenes[sceneName]
#
#     for scene in bpy.data.scenes:
#
#         override = bpy.context.copy()
#         override["area.type"] = ['OUTLINER']
#         override["display_mode"] = ['ORPHAN_DATA']
#         #bpy.ops.outliner.orphans_purge(override)
#
#         list_of_collections = []
#
#         for collection in newScene.collection.children:
#             list_of_collections.append(collection)
#
#         if rig_collection not in list_of_collections:
#             newScene.collection.children.link(rig_collection)
#
#
#     for scene in bpy.data.scenes:
#
#         if scene.name == 'Scene':
#             bpy.data.scenes.remove(scene)
#
#     data = [bpy.data.objects,
#             bpy.data.collections,
#             bpy.data.materials,
#             bpy.data.meshes,
#             bpy.data.lights]
#
#     # for type in data:
#
#     #     for obj in type:
#     #         if obj.users < 1:
#     #             type.remove(obj)




class Cleanrigscene(PreflightCheck):

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
        #cleanup_scene()
        bpy.ops.object.cleanup_rig()

        print('Cleanrigscene')
        self.pass_check('Check Passed')
        # self.fail_check('Check Failed')
