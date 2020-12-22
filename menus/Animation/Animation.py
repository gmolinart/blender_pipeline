import bpy


class Animation(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lumbermill'
    bl_label = 'Animation'

    def draw(self, context):
        """
        in here we'll have all the buttons for the Panel in the order that lumbermill saves them in.
        :param context:
        :return:
        """
        # ADD BUTTONS
        self.layout.row().operator("object.publish")
        self.layout.row().operator("object.create_grease_pencil")
        self.layout.row().operator("object.copy_relationship")
        self.layout.row().operator("object.paste_relationship")
        self.layout.row().operator("object.ik_fk_switch")
        self.layout.row().operator("object.switch_proxy")
        self.layout.row().operator("object.switch_rig")
        self.layout.row().operator("object.switch_extras")
        self.layout.row().operator("object.write_animation_data")
        self.layout.row().operator("object.render_with_audio")
        self.layout.row().operator("object.publish")
        self.layout.row().operator("object.grease_pencil_switch")
        self.layout.row().operator("object.gp_main_layers")
        self.layout.row().operator("object.interactive")
        self.layout.row().operator("object.current_frame")
