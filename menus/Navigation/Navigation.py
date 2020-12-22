import bpy


class Navigation(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lumbermill'
    bl_label = 'Navigation'

    def draw(self, context):
        """
        in here we'll have all the buttons for the Panel in the order that lumbermill saves them in.
        :param context:
        :return:
        """
        # ADD BUTTONS
        self.layout.row().operator("object.open_selected")
        self.layout.row().operator("object.open_shot")
        self.layout.row().operator("object.open_asset")
        self.layout.row().operator("object.switch_resolution")
        self.layout.row().operator("object.switch_versions")
        self.layout.row().operator("object.switch_users")
        self.layout.row().operator("object.switch_context")
        self.layout.row().operator("object.switch_task")
        self.layout.row().operator("object.back_to_previous")
        self.layout.row().operator("object.copy_to_user")
        self.layout.row().operator("object.copy_to_task")
