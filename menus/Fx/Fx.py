import bpy


class Fx(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Alchemy'
    bl_label = 'Fx'
    def draw(self, context):
        """
        in here we'll have all the buttons for the Panel in the order that Alchemy saves them in.
        :param context:
        :return:
        """
        # ADD BUTTONS
        self.layout.row().operator("object.create_instance")
