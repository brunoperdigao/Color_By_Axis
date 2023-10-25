from distutils.command.config import config
import bpy
import bmesh
import gpu
import mathutils
import copy
from gpu_extras.batch import batch_for_shader


class CBA_Edges(bpy.types.Operator):
    bl_idname = "object.color_by_axis_edges"
    bl_label = "Color By Axis"
    bl_description = "Operator to color edges by axis"
    bl_options = {'REGISTER'}

    draw_handler = None


    @staticmethod
    def get_verts():
        context = bpy.context
        axis_type = context.scene.axis_type
        depsgraph = context.evaluated_depsgraph_get()
        verts = [[], [], []]

        def equals(c1, c2, precision=4):
            return abs(c1 - c2) < 10 ** (-precision)

        for o in context.selected_objects:
            if o.type not in ("MESH", "CURVE", "SURFACE", "FONT", "META"):
                continue
            if context.mode == "EDIT_MESH":
                bm = bmesh.from_edit_mesh(o.data)
            else:
                object_eval = o.evaluated_get(depsgraph)
                mesh_eval = object_eval.to_mesh()
                bm = bmesh.new()
                bm.from_mesh(mesh_eval)

            axis_reference = context.scene.axis_ref
            matrix_world = o.matrix_world
            matrix_calc = mathutils.Matrix.Identity(4)

            if axis_type == "REFERENCE" and axis_reference:
                obj_location = o.matrix_world.to_translation()
                obj_scale = o.matrix_world.to_scale()
                obj_rotation = o.matrix_world.to_euler()

                # Get the reference rotation
                custom_euler = copy.copy(axis_reference.matrix_world.to_euler())

                # To get the rotation relative to the reference, subtract the reference euler by the object euler, and avoid negative numbers
                custom_euler[0] = custom_euler[0] - obj_rotation[0]
                custom_euler[1] = custom_euler[1] - obj_rotation[1]
                custom_euler[2] = custom_euler[2] - obj_rotation[2]
                for v in custom_euler:
                    if v < 0:
                        v = v * (-1)

                # Custom matrix, mixed with the reference rotation
                matrix_calc = mathutils.Matrix.LocRotScale(obj_location, custom_euler, obj_scale)


            elif axis_type == "GLOBAL":
                matrix_calc = matrix_world

            for e in bm.edges:
                if context.mode == "EDIT_MESH" and e.hide:
                    pass
                else:
                    v1_global = matrix_world @ e.verts[0].co
                    v2_global = matrix_world @ e.verts[1].co
                    v1 = matrix_calc @ e.verts[0].co
                    v2 = matrix_calc @ e.verts[1].co
                    for i, axis in enumerate(((1, 2), (0, 2), (0, 1))):
                        if equals(v1[axis[0]], v2[axis[0]]) and equals(v1[axis[1]], v2[axis[1]]):
                            verts[i].append(v1_global)
                            verts[i].append(v2_global)

        return verts

    @staticmethod
    def draw():
        if not hasattr(bpy.context.scene, "draw_permanent") or not bpy.context.scene.draw_permanent:
            return

        context = bpy.context
        line_width = context.scene.line_width
        # Get colors from User Preferences in Blender Default Theme
        theme = context.preferences.themes[0]
        ui = theme.user_interface

        verts_axes = CBA_Edges.get_verts()
        for i, color in enumerate(((tuple(ui.axis_x) + (1,)), (tuple(ui.axis_y) + (1,)), (tuple(ui.axis_z) + (1,)))):
            coords = verts_axes[i]
            shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")
            batch = batch_for_shader(shader, "LINES", {"pos": coords})
            shader.bind()
            shader.uniform_float("color", color)
            gpu.state.line_width_set(line_width)
            if not hasattr(bpy.context.scene, "draw_in_front") or not bpy.context.scene.draw_in_front:
                gpu.state.depth_test_set('LESS_EQUAL')
                gpu.state.depth_mask_set(True)
                
            batch.draw(shader)

