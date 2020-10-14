from cgl.plugins.preflight.preflight_check import PreflightCheck
from cgl.plugins.blender import lumbermill as lm
# from cgl.plugins.blender import utils
import bpy

class Resettransformations(PreflightCheck):

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
                try:
                    bpy.ops.object.select_all(action='DESELECT')
                    obj.select_set(True)
                    bpy.ops.object.make_single_user(object=True, obdata=True, material=True, animation=False)
                    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

                except(AttributeError):
                    logging.debug('{} Skipping'.format(obj.name))
                    pass

        print('Resettransformations')
        self.pass_check('Check Passed')
            # self.fail_check('Check Failed')


