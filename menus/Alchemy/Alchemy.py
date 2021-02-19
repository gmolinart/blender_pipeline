import bpy


class Alchemy(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Alchemy'
    bl_label = bl_category

    def draw(self, context):
        """
        in here we'll have all the buttons for the Panel in the order that Alchemy saves them in.
        :param context:
        :return:
        """
        # ADD BUTTONS
        self.layout.row().operator("object.launch")
        self.layout.row().operator("object.pre_publish")
        self.layout.row().operator("object.build")
        self.layout.row().operator("object.version_up")
        self.layout.row().operator("object.render")
        self.layout.row().operator("object.review")
        self.layout.row().operator("object.turntable")
        self.layout.row().operator("object.version_to_latest")
