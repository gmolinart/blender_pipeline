import bpy
from cgl.plugins.blender import alchemy as alc


def get_items(self, context):
    from cgl.plugins.blender import alchemy as alc

    path_object = alc.scene_object()

    variant = path_object.glob_project_element('variant')
    version = variant.reverse()
    print(variant)

    value = [(variant[i], variant[i], '') for i in range(len(variant))]

    return (value)


class SwitchVariant(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'alchemy.switch_variant'
    bl_label = 'Switch Variant'

    bl_property = "selected_variant"
    selected_variant = bpy.props.EnumProperty(items=get_items)

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.selected_variant)
        new_user = alc.scene_object().copy(variant=self.selected_variant, latest=True)
        import os
        if os.path.isfile(new_user.path_root):
            open_file = new_user.path_root

        else:
            for i in new_user.glob_project_element('user'):
                path = new_user.copy(user=i).path_root
                if os.path.isfile(path):
                    open_file = path

        alc.open_file(open_file)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SwitchVariant)


def unregister():
    bpy.utils.unregister_class(SwitchVariant)


if __name__ == "__main__":
    register()

    # test call

    bpy.ops.alchemy.switch_variant('INVOKE_DEFAULT')