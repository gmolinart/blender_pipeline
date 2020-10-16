from cgl.plugins.preflight.preflight_check import PreflightCheck
from cgl.plugins.blender import lumbermill as lm
import bpy
# from cgl.plugins.blender import utils
import os

class WriteMeshList(PreflightCheck):

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
        print('Write Mesh List')
        bpy.ops.object.write_mesh_list()


        scene = lm.scene_object()
        if os.path.isfile(scene.copy(ext = 'json', context = 'render').path_root):


            self.pass_check('Check Passed')

        else:
            self.fail_check('Check Failed, mesh_list wasnt exported')
