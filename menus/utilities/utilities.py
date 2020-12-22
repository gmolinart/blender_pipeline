import bpy


class utilities(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lumbermill'
    bl_label = 'Utilities'

    def draw(self, context):
        """
        in here we'll have all the buttons for the Panel in the order that lumbermill saves them in.
        :param context:
        :return:
        """
        # ADD BUTTONS
        self.layout.row().operator("object.import_asset")
        self.layout.row().operator("object.correct_file_name")
        self.layout.row().operator("object.open_asset")
        self.layout.row().operator("object.open_shot")
        self.layout.row().operator("object.delete_defaults")
        self.layout.row().operator("object.import_references")
        self.layout.row().operator("object.import_audio")
        self.layout.row().operator("object.delete_turntable")
        self.layout.row().operator("object.setup_collections")
        self.layout.row().operator("object.fix_collection_name")
        self.layout.row().operator("object.rename_object")
        self.layout.row().operator("object.cleanup_scene")
        self.layout.row().operator("object.show_in_folder")
        self.layout.row().operator("object.delete_workspaces")
        self.layout.row().operator("object.switch_users")
        self.layout.row().operator("object.switch_task")
        self.layout.row().operator("object.switch_versions")
        self.layout.row().operator("object.switch_resolution")
        self.layout.row().operator("object.open_selected")
        self.layout.row().operator("object.collection_to_asset")
        self.layout.row().operator("object.open_documentation")
        self.layout.row().operator("object.source_to_render")
        self.layout.row().operator("object.copy_to_anim_project")
