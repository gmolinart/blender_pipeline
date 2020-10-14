import bpy
from cgl.plugins.blender import lumbermill as lm

class CopySkinWeights(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.copy_skin_weights'
    bl_label = 'Copy Skin Weights'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def remove_controllers(obj):
    obj = bpy.context.object

    vertex_groups = bpy.context.object.vertex_groups

    for group in vertex_groups:
        if 'fs:' in group.name:
            vg = obj.vertex_groups.get(group.name)
            if vg is not None:
                obj.vertex_groups.remove(vg)
                print(group.name)


def get_selection_order():
    objects = []

    obj_a = bpy.context.active_object
    objects.append(obj_a)

    selection = bpy.context.selected_objects

    for i in selection:
        if i != obj_a:
            obj_b = i

    objects.append(obj_b)

    print('_________{} and {} selected____________'.format(
        objects[0].name, objects[1].name))
    return objects


def applyModifierToMultiUser(scene):
    active = scene.objects.active
    if (active == None):
        print("Select an object")
        return
    if (active.type != "MESH"):
        print("Select an mesh object")
        return
    mesh = active.to_mesh(scene, True, 'PREVIEW')
    linked = []
    selected = []

    for obj in bpy.data.objects:
        if obj.data == active.data:
            linked.append(obj)
    for obj in bpy.context.selected_editable_objects:
        selected.append(obj)
        obj.select = False

    for obj in linked:
        obj.select = True
        obj.modifiers.clear()

    active.data = mesh
    bpy.ops.object.make_links_data(type='OBDATA')

    for obj in linked:
        obj.select = False
    for obj in selected:
        obj.select = True


def copy_vertex_weight(selection=None):
    objects = get_selection_order()

    try:
        obj = objects[0]
        obj.data.use_auto_smooth = True
        mod = obj.modifiers.new("data_transfer", 'DATA_TRANSFER')
        scn = bpy.context.scene

        mod.object = objects[1]
        mod.use_vert_data = True
        mod.data_types_verts = {'VGROUP_WEIGHTS'}

        bpy.ops.object.datalayout_transfer(modifier='data_transfer')
        bpy.ops.object.modifier_apply(modifier="data_transfer")


    except(AttributeError):
        pass


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    objects = get_selection_order()
    if len(objects) == 2:

        copy_vertex_weight()
        remove_controllers(objects[0])
        bpy.ops.object.cleanup_weights()

    else:
        lm.confirm_prompt(message='please select source and destination mesh')

