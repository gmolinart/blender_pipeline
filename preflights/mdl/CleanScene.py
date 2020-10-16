from cgl.plugins.preflight.preflight_check import PreflightCheck
# from cgl.plugins.blender import lumbermill as lm
# from cgl.plugins.blender import utils
import bpy


def remove_environments():
    import bpy
    from cgl.plugins.blender import lumbermill as lm

    if 'env' in bpy.data.collections:

        for obj in bpy.data.collections['env'].objects:
            try:
                if 'env' in obj.instance_collection.library.name:
                    obj.select_set(True)
                    bpy.ops.object.unlink_asset()

            except AttributeError:
                pass


class CleanScene(PreflightCheck):

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
        print('Cleanscene')

        remove_environments()
        bpy.ops.object.cleanup_scene()

        self.pass_check('Check Passed')
        # self.fail_check('Check Failed')
