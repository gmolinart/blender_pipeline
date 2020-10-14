import bpy
from cgl.plugins.blender import lumbermill as lm


class CreateLow(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.create_low'
    bl_label = 'Create Low'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def parent_mesh_to_collection(collection_name='', low=False, objects=None):
    if collection_name == '':
        collection_name = lm.scene_object().shot

    if low:
        collection_name = '{}_low'.format(lm.scene_object().shot)

    meshes = []
    if not objects:
        objects = bpy.context.selected_objects

    for obj in objects:

        if obj.type == "MESH":

            print(obj.name)
            meshes.append(obj)
            try:
                for collection in bpy.data.collections:
                    if collection.name == collection_name:
                        collection.objects.link(obj)

            except(RuntimeError, TypeError, NameError, AttributeError):
                pass

            for collection in obj.users_collection:
                if collection.name != collection_name:
                    collection.objects.unlink(obj)

    return meshes


def create_low_collection(collection_name=''):
    if collection_name == '':
        scene = lm.scene_object().shot
        collection_name = '{}_low'.format(scene)

    if collection_name not in bpy.data.collections:
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)


def delete_modifiers():
    objects = bpy.context.selected_objects
    for obj in objects:
        for mod in obj.modifiers:
            bpy.ops.object.modifier_remove(modifier=mod.name)


def make_selected_proxy():
    proxy_objects = []
    for obj in bpy.context.selected_objects:
        new_object = obj.copy()
        new_object.data = obj.data.copy()
        bpy.context.collection.objects.link(new_object)
        new_object.name = obj.name + '_low'

        delete_modifiers()
        proxy = bpy.ops.object.modifier_add(type='DECIMATE')
        for mod in new_object.modifiers:
            if mod.type == 'DECIMATE':
                print(mod)
                mod.ratio = 0.5

        proxy_objects.append(new_object)
    return proxy_objects


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    proxy = make_selected_proxy()
    create_low_collection()
    parent_mesh_to_collection(low=True, objects=proxy)


