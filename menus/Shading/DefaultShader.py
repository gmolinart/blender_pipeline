import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils

try:
    from .SetupShaderColor import setup_preview_viewport_display
except:
    setup_preview_viewport_display = utils.setup_preview_viewport_display
    pass


class DefaultShader(bpy.types.Operator):
    """
    Assigns default shader
    """
    bl_idname = 'object.default_shader'
    bl_label = 'Default Shader'
    selection = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def get_default_shader():
    current_scene = lm.scene_object()
    dict = {'company': current_scene.company,
            'context': 'render',
            'project': current_scene.project,
            'scope': 'assets',
            'seq': 'lib',
            'shot': 'DEFAULTSHADER',
            'task': 'shd',
            'version': '001.000',
            'user': 'publish',
            'resolution': 'high',
            'filename': 'lib_DEFAULTSHADER_shd',
            'ext': 'blend'
            }

    path_object = lm.LumberObject(dict)
    path_object = path_object.copy(set_proper_filename=True)

    # print(default_shader.path_root)

    default_in_scene = False
    # for group in bpy.data.node_groups:
    #     if 'DEFAULTSHADER' in group.name:
    #         default_in_scene = True

    if not default_in_scene:
        lm.import_file(filepath=path_object.path_root, linked=False, type='GROUP')


def delete_duplicate_groups(node_name):
    for node in bpy.data.node_groups:
        if node.name.split('.')[0] == node_name:
            if not node.name == node_name:
                bpy.data.node_groups.remove(node)


def get_image_inputs(node, attribute='Base Color'):
    input = node.inputs[attribute]

    try:

        input_surface = input.links[0].from_node
        # color_input = input_surface.inputs[attribute]
        image_node = input.links[0].from_node

    except IndexError:
        image_node = input
    return image_node


def get_valid_meshes(selection=''):
    valid_meshes = []
    if selection == '':
        selection = bpy.context.selected_objects

    else:
        selection = [bpy.data.objects[selection]]

    for object in selection:
        try:
            bpy.ops.object.material_slot_remove_unused()
        except RuntimeError:
            print('context incorrect')
            pass

        if object and object.type == 'MESH':
            valid_meshes.append(object)
    return valid_meshes


def assign_default(object):
    if len(object.material_slots) == 0:
        try:
            material = bpy.data.materials.new(name=object.name)
            object.data.materials.append(material)
            material.use_nodes = True
            group = material.node_tree.nodes.new(type='ShaderNodeGroup')
            print(group)
            group.name = 'GroupShader'
            group.node_tree = bpy.data.node_groups['DEFAULTSHADER']
            group.inputs['Transparent'].default_value = 0
            # TODO, connect output to material shader..
        except AttributeError:
            pass


def updateShader(material):
    failed = []

    print(5 * '_' + material.name + '_____updating ')

    node_tree = material.node_tree.nodes

    for n in node_tree:
        if n.type == 'GROUP':
            n.node_tree = bpy.data.node_groups['DEFAULTSHADER']
            n.inputs[0].default_value = material.diffuse_color
            n.name = 'DEFAULTSHADER'

    node_tree = material.node_tree
    nodes = material.node_tree.nodes
    links = node_tree.links

    for node in nodes:
        if node.name == 'Principled BSDF':
            color = node.inputs['Base Color'].default_value

            image_texture = get_image_inputs(node)
            group = material.node_tree.nodes.new(type='ShaderNodeGroup')
            print(group)
            group.name = 'DEFAULTSHADER'
            group.node_tree = bpy.data.node_groups['DEFAULTSHADER']
            group.inputs['Transparent'].default_value = 0
            links.new(node_tree.nodes['Material Output'].inputs['Surface'], group.outputs[0])

            try:
                print(group.inputs['Color'], image_texture.outputs['Color'])
                links.new(group.inputs['Color'], image_texture.outputs['Color'])
            except AttributeError:
                pass
            node_tree.nodes.remove(node)

        elif 'DEFAULTSHADER' in node.name:
            #            if not node.name == 'DEFAULTSHADER':
            #                #nodes.remove(node)

            if 'Material Output' in node_tree.nodes:

                links.new(node_tree.nodes['Material Output'].inputs['Surface'],
                          node_tree.nodes['DEFAULTSHADER'].outputs[0])

            else:
                print(5 * '_' + material.name + '_____ERROR ')
                failed.append(material)
    return failed


def run():
    get_default_shader()
    failed_items = []

    for obj in get_valid_meshes():
        assign_default(obj)

    selection = bpy.data.materials

    print(len(selection))

    for material in selection:
        if 'cs_' not in material.name:
            if material.use_nodes:
                print(selection)
                failed = updateShader(material)
                if len(failed):
                    for m in failed:
                        failed_items.append(m.name)
    if len(failed_items):
        print(5 * '_' + 'Failed Materials' + 5 * '_')
        for i in failed_items:
            print(i)

        lm.confirm_prompt(message='Failed materials : {}'.format(failed_items))

    else:
        lm.confirm_prompt(message='Default shader assigned')

    delete_duplicate_groups('DEFAULTSHADER')
    delete_duplicate_groups('toon_material')


if __name__ == '__main__':
    run()
