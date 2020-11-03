import bpy


class Lighting(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lumbermill'
    bl_label = 'Lighting'

    def draw(self, context):
        """
        in here we'll have all the buttons for the Panel in the order that lumbermill saves them in.
        :param context:
        :return:
        """
        # ADD BUTTONS
        self.layout.row().operator("object.default_light_setup")
        self.layout.row().operator("object.import_all_objects")
        self.layout.row().operator("object.split_scene")
