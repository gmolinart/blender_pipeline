import bpy


class Shading(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Alchemy'
    bl_label = 'Shading'

    def draw(self, context):
        """
        in here we'll have all the buttons for the Panel in the order that Alchemy saves them in.
        :param context:
        :return:
        """
        # ADD BUTTONS
        self.layout.row().operator("object.default_shader")
        self.layout.row().operator("object.publish_textures")
        self.layout.row().operator("object.rename_materials")
        self.layout.row().operator("object.setup_shader_color")
        self.layout.row().operator("object.save_materials")
        self.layout.row().operator("object.load_materials")
        self.layout.row().operator("object.add_to_shader_group")
