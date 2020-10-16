from cgl.plugins.preflight.preflight_check import PreflightCheck
# from cgl.plugins.blender import lumbermill as lm
# from cgl.plugins.blender import utils


class BakeModifiers(PreflightCheck):

    def getName(self):
        pass

    def run(self):
        from cgl.plugins.blender import lumbermill as lm

        import bpy

        objects = bpy.data.objects


        for window in bpy.context.window_manager.windows:
            screen = window.screen

            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    override = {'window': window, 'screen': screen, 'area': area}
                    bpy.ops.screen.screen_full_area(override)

        bpy.ops.object.select_all(action='SELECT')

        bpy.ops.object.convert(target='MESH')

        for obj in objects:
            if obj.show_wire:
                print(obj.name)
                objects.remove(obj)

            elif 'BOOLEAN' in obj.name:
                objects.remove(obj)

            elif obj.display_type == 'BOUNDS':
                objects.remove(obj)

        print('Bake Modifiers')
        self.pass_check('Check Passed')
        # self.fail_check('Check Failed')
