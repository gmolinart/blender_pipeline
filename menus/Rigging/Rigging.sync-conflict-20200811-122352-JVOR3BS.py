import bpy


class Rigging(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rigging'
    bl_label = bl_category

    def draw(self, context):
        """
        in here we'll have all the buttons for the Panel in the order that lumbermill saves them in.
        :param context:
        :return:
        """
        # ADD BUTTONS
        self.layout.row().operator("object.simple_controller")
        self.layout.row().operator("object.fixrignames")
        self.layout.row().operator("object.parent_mesh_to_rig")
        self.layout.row().operator("object.checkshaders")
        self.layout.row().operator("object.cleanup_rig")
        self.layout.row().operator("object.reset_armature")
        self.layout.row().operator("object.create_hooks")
        self.layout.row().operator("object.remove_constraints")
        self.layout.row().operator("object.remove_modifiers")
        self.layout.row().operator("object.create_four_way_controller")
        self.layout.row().operator("object.corrective_blend_shapes")
        self.layout.row().operator("object.setup_rig_test")
        self.layout.row().operator("object.get_default_action")
        self.layout.row().operator("object.get_default_camera")
