import bpy


class Rigging(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lumbermill'
    bl_label = 'Rigging'

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
        self.layout.row().operator("object.corrective_blend_shapes")
        self.layout.row().operator("object.setup_rig_test")
        self.layout.row().operator("object.get_default_action")
        self.layout.row().operator("object.get_default_camera")
        self.layout.row().operator("object.add_controllers")
        self.layout.row().operator("object.set_color_from_parent")
        self.layout.row().operator("object.default_controller_shape")
        self.layout.row().operator("object.mesh_to_mdl_task")
        self.layout.row().operator("object.cleanup_weights")
        self.layout.row().operator("object.mirror_vertex_groups")
        self.layout.row().operator("object.remove_mesh_controllers")
        self.layout.row().operator("object.copy_skin_weights")
        self.layout.row().operator("object.remove_drivers")
