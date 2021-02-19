import bpy
# from cgl.plugins.blender import Alchemy as lm

from cgl.plugins.blender import alchemy as alc
from cgl.plugins.blender.tasks import shd

from cgl.plugins.blender.utils import get_selection, parent_object, get_object
from cgl.plugins.blender import utils
from cgl.plugins.blender.tasks.mdl import create_material_groups
from importlib import reload

reload(utils)


def get_items(self, contt):
    tasks = shd.get_valid_material_list()
    tasks.append('Add New')
    print(tasks)

    value = [(tasks[i], tasks[i], '') for i in range(len(tasks))]

    return (value)


class AddToShaderGroup(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.add_to_shader_group'
    bl_label = 'Add To Shader Group'
    bl_property = "shaders"
    shaders = bpy.props.EnumProperty(items=get_items)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if self.shaders == 'Add New':
            print(self.shaders)
            create_material_groups()
            return

        shader = bpy.data.objects[self.shaders]
        selection = get_selection()
        for obj in selection:
            print(self.shaders)
            print(selection)

            parent_object(obj, shader)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)

        return {'FINISHED'}


if __name__ == '__main__':
    bpy.utils.register_class(AddToShaderGroup)
    bpy.ops.object.add_to_shader_group('INVOKE_DEFAULT')