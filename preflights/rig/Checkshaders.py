from cgl.plugins.preflight.preflight_check import PreflightCheck
# from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils
import bpy


class Checkshaders(PreflightCheck):

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

        failed_items = []
        for obj in bpy.data.objects:
            try:

                if 'cs_' not in obj.name:
                    if obj.type == "MESH":
                        bpy.ops.object.default_shader(selection = obj.name)
                        utils.rename_materials(selection = obj.name)


                        print('Checkshaders')

            except:
                    failed_items.append(obj.name)

        if failed_items:

            self.fail_check(
                'Check Failed , Error trying to auto assign  '
                '\nPlease run that command  via the button or check the shader in : '
                '\n{}'.format(*failed_items, sep='\n- '))


        self.pass_check('Check Passed')
