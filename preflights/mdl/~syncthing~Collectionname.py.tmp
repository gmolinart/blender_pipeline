from cgl.plugins.preflight.preflight_check import PreflightCheck
from cgl.plugins.blender import lumbermill as lm
# from cgl.plugins.blender import utils
import bpy

class CollectionName(PreflightCheck):

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
        #bpy.ops.object.build()
        currentScene = lm.scene_object()
        assetName = lm.scene_object().shot
        collectionExists = False
        for collections in bpy.data.collections:

            if assetName == collections.name:
                print('{} exists'.format(assetName))
                collectionExists = True

        if collectionExists:
            self.pass_check('Check Passed')

        else:
            self.fail_check('Couldnt find collection with Asset name')
