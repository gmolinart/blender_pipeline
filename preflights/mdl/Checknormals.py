from cgl.plugins.preflight.preflight_check import PreflightCheck
import bpy
from cgl.plugins.blender import lumbermill as lm
# from cgl.plugins.blender import utils
import logging


def applyModifierToMultiUser(scene):
    active = scene.objects.active
    if (active == None):
        print("Select an object")
        return
    if (active.type != "MESH"):
        print("Select an mesh object")
        return
    mesh = active.to_mesh(scene, True, 'PREVIEW')
    linked = []
    selected = []
    for obj in bpy.data.objects:
        if obj.data == active.data:
                linked.append(obj)
    for obj in bpy.context.selected_editable_objects:
        selected.append(obj)
        obj.select = False

    for obj in linked:
        obj.select = True
        obj.modifiers.clear()
    active.data = mesh
    bpy.ops.object.make_links_data(type='OBDATA')

    for obj in linked:
        obj.select = False
    for obj in selected:
        obj.select = True

class Checknormals(PreflightCheck):

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
        currentScene = lm.scene_object()
        assetName = lm.scene_object().shot
        obj_in_collection = bpy.data.collections[assetName].all_objects

        if lm.scene_object().type != 'env':

            for obj in obj_in_collection:
                try :
                    bpy.ops.object.select_all(action='DESELECT')
                    obj.select_set(True)
                    obj.data.use_auto_smooth = True
                    mod = obj.modifiers.new("weighted_normal", 'WEIGHTED_NORMAL')
                    scn = bpy.context.scene
                    applyModifierToMultiUser(scn)
                except(AttributeError):
                    logging.debug('{} Skipping, wasnt able to setup normals '.format(obj.name))
                    pass

        print('Normals Check' )
        self.pass_check('Check Passed')

        # self.fail_check('Check Failed')
