import bpy
# from cgl.plugins.blender import Alchemy as lm

class RemoveDrivers(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.remove_drivers'
    bl_label = 'Remove Drivers'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def remove_drivers():

    for obj in bpy.context.selected_objects:
        if obj.animation_data is not None:
            for driver in obj.animation_data.drivers:
                print('%s.%s is driven to %s' % (obj.name, driver.data_path, driver.driver.expression))

            drivers_data = obj.animation_data.drivers
            for dr in drivers_data:
                obj.driver_remove(dr.data_path, -1)
    obj.hide_viewport = False

def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    remove_drivers()

