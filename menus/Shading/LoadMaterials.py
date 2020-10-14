import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils
import json


class LoadMaterials(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.load_materials'
    bl_label = 'Load Materials'

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}



def read_materials(path_object=None):
    """

    :type path_object: object
    """
    from cgl.plugins.blender import lumbermill as lm
    from cgl.core.utils.read_write import load_json
    """
    Reads the materials on the shdr task from defined from a json file
    :return:
    """
    import bpy
    if path_object is None:
        path_object = lm.scene_object()

    shaders = path_object.copy(task='shd', user='publish', set_proper_filename=True).latest_version()
    outFile = shaders.copy(ext='json').path_root

    data = load_json(outFile)

    for obj in data.keys():
        object = bpy.data.objects[obj]
        # data = object.data
        index = 0

        for material in data[obj].keys():

            if material not in bpy.data.materials:
                lm.import_file(shaders.path_root, collection_name=material, type='MATERIAL', linked=False)

            if material not in object.data.materials:
                object.data.materials.append(bpy.data.materials[material])

            face_list = data[obj][material]

            for face in face_list:
                object.data.polygons[face].select = True

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.context.tool_settings.mesh_select_mode = [False, False, True]
            object.active_material_index = index
            bpy.ops.object.material_slot_assign()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            index += 1



def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    try:

        read_materials()
    except FileNotFoundError:
        lm.confirm_prompt(message= 'the latest shader task is empty please export shader again')