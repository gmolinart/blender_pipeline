import bpy


class Modeling(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lumbermill'
    bl_label = 'Modeling'

    def draw(self, context):
        """
        in here we'll have all the buttons for the Panel in the order that lumbermill saves them in.
        :param context:
        :return:
        """
        # ADD BUTTONS
        self.layout.row().operator("object.checknormals")
        self.layout.row().operator("object.create_low")
        self.layout.row().operator("object.publish_low")
        self.layout.row().operator("object.center_reset")
        self.layout.row().operator("object.export_to_obj")
        self.layout.row().operator("object.write_mesh_list")
        self.layout.row().operator("object.update_resolutions")
        self.layout.row().operator("object.copy_latest_low")
