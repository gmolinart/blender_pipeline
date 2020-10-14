import bpy
from cgl.plugins.blender import lumbermill as lm
class SetupShaderColor(bpy.types.Operator):
    """
    assigns the viewpor preview button from the material of selected object
    """
    bl_idname = 'object.setup_shader_color'
    bl_label = 'Setup Shader Color'

    def execute(self, context):
        run()
        return {'FINISHED'}

def get_valid_meshes_list(objects):

    valid_objects = []

    for object in objects:
        if object and object.type == "MESH":
            if object.is_instancer == False:
                valid_objects.append(object)
    return valid_objects
def setup_preview_viewport_display(object):
    """
    set up the default viewport display color  diffuse_color on materials
    :param color: Value of the color  of the parent menu  FloatProperty 4
    :param selection:
    """
    materials = get_materials_from_object(object)

    for material in materials:
        node_tree = material.node_tree.nodes
        inputs = preview_inputs_from_node_tree(node_tree)
        preview_colors = get_preview_from_texture(inputs, node_tree)

        for i in range(0, 3):
            material.diffuse_color[i] = preview_colors[i]

def get_materials_from_object(object):
    valid_materials = []

    for material_slot in object.material_slots:
        material = material_slot.material
        valid_materials.append(material_slot.material)

    return (valid_materials)

def get_preview_from_texture(inputs, node_tree):
    texture = None
    if inputs:
        color_input = inputs[1]
        transparent = inputs[2]

        try:
            texture = color_input.links[0].from_node
        except IndexError:
            print('no texture connected')
            pass

    if texture:

        if texture.type == 'TEX_IMAGE':
            preview_color = texture.image.pixels
            diffuse_color = [preview_color[7004],
                             preview_color[7005],
                             preview_color[7006],
                             1 - transparent.default_value]

        if texture.type == "RGB":
            simple_color = texture.outputs['Color'].default_value
            preview_color = [simple_color[1],
                             simple_color[2],
                             simple_color[3],
                             1 - transparent.default_value]

        else:
            preview_color = [1, 1, 1, 1]
            print('_______COMPLEX NODES PLEASE SET MANUALLY_______')
    else:

        inputs = preview_inputs_from_node_tree(node_tree)
        if inputs:

            preview_color = [color_input.default_value[0],
                             color_input.default_value[1],
                             color_input.default_value[2],
                             1]

        else:
            preview_color = [1, 1, 1, 1]

    return preview_color

def preview_inputs_from_node_tree(node_tree):
    color_input = None
    transparent = None
    valid_node = None
    if 'DEFAULTSHADER' in node_tree:
        try:
            color_input = node_tree['DEFAULTSHADER'].inputs['Color']
            transparent = node_tree['DEFAULTSHADER'].inputs['Transparent']
            valid_node = node_tree['DEFAULTSHADER']
            found = True
        except KeyError:
            found = False
    else:
        found = False
        for node in node_tree:

            if node.type == 'BSDF_PRINCIPLED' and not found:
                color_input = node.inputs[0]
                transparent = node.inputs['Transmission']
                found = True
                valid_node = node

    returns = (valid_node, color_input, transparent)

    if found:
        print('__________Valid Materials And inputs______________')
        print(returns)
        return returns
    else:
        returns = (1, 1, 1, 1)
def get_selection(selection=None):
    if selection == None:
        try:
            selection = bpy.context.selected_objects
        except:
            currentScene = lm.scene_object()
            assetName = lm.scene_object().shot
            obj_in_collection = bpy.data.collections[assetName].all_objects

    if not selection:
        selection = bpy.data.objects

    return selection
def run():
    objects = get_selection()
    valid_meshes = get_valid_meshes_list(objects)
    for obj in valid_meshes:
        print(obj.name)
        setup_preview_viewport_display(obj)


if __name__ == '__main__':
    run()
