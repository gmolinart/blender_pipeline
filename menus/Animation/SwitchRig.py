import bpy


# from cgl.plugins.blender import lumbermill as lm


def get_rigs():
    print('_____________')
    rigs = []
    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE' and 'proxy' in obj.name:
            rigs.append(obj)

    return (rigs)


def get_items(self, context):
    from cgl.plugins.blender import lumbermill as lm
    import os

    tasks = get_rigs()

    value = [(tasks[i].name,
              tasks[i].name.replace('_proxy', '')
              , '') for i in range(len(tasks))]

    return (value)


class SwitchRig(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.switch_rig'
    bl_label = 'Switch Rig'

    bl_property = "rigs"
    rigs = bpy.props.EnumProperty(items=get_items)

    def execute(self, context):
        print(55555555)
        print(self.rigs)
        for obj in bpy.context.selected_objects:
            obj.select_set(False)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.data.objects[self.rigs].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[self.rigs]
        bpy.ops.object.mode_set(mode='POSE')
        # bpy.ops.object.mode_set(mode='POSE')
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}


if __name__ == '__main__':
    print(get_rigs())
    bpy.utils.register_class(SwitchRig)
    bpy.ops.object.switch_rig('INVOKE_DEFAULT')