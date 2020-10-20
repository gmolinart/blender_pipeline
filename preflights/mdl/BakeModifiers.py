from cgl.plugins.preflight.preflight_check import PreflightCheck
import bpy
# from cgl.plugins.blender import lumbermill as lm
# from cgl.plugins.blender import utils


def delete_booleans_shapes():
    objects = bpy.data.objects
    for obj in objects:
        if 'instancer' not in obj.name:

            if obj.show_wire:
                print(obj.name)
                objects.remove(obj)

            elif 'BOOLEAN' in obj.name:
                objects.remove(obj)

            elif obj.display_type == 'BOUNDS':
                objects.remove(obj)

        bpy.ops.object.select_all(action='DESELECT')


def bake_modifiers():

    objects = bpy.context.view_layer.objects
    for obj in objects:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.convert(target='MESH')


class BakeModifiers(PreflightCheck):

    def getName(self):
        pass

    def run(self):
        from cgl.plugins.blender import lumbermill as lm
        import bpy
        objects = bpy.context.view_layer.objects
        for window in bpy.context.window_manager.windows:
            screen = window.screen

            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    override = {'window': window, 'screen': screen, 'area': area}
                    bpy.ops.screen.screen_full_area(override)


            bake_modifiers()
            delete_booleans_shapes()
        bpy.ops.object.unlink_asset()

        print('Bake Modifiers')
        self.pass_check('Check Passed')
        # self.fail_check('Check Failed')
