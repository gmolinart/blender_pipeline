import bpy


class Modeling(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Alchemy'
    bl_label = 'Modeling'

    def draw(self, context):
        """
        in here we'll have all the buttons for the Panel in the order that Alchemy saves them in.
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
        self.layout.row().operator("object.fix_mesh_name")
        self.layout.row().operator("object.import_base_mesh")
        self.layout.row().operator("object.read__model__hirarchy")
