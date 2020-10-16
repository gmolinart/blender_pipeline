import bpy


class Layout(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lumbermill'
    bl_label = 'Layout'

    def draw(self, context):
        """
        in here we'll have all the buttons for the Panel in the order that lumbermill saves them in.
        :param context:
        :return:
        """
        # ADD BUTTONS
        self.layout.row().operator("object.read_layout")
        self.layout.row().operator("object.write_layout")
        self.layout.row().operator("object.publish_cameras")
        self.layout.row().operator("object.rename_cameras")
        self.layout.row().operator("object.switch_selected_resolution")
        self.layout.row().operator("object.switch_selected_user")
        self.layout.row().operator("object.switch_selected_version")
        self.layout.row().operator("object.unlink_asset")
        self.layout.row().operator("object.read_layout_from_selected")
