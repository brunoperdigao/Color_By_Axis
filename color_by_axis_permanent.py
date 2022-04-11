import bpy
import bmesh
import bgl
import gpu
import mathutils
from gpu_extras.batch import batch_for_shader


class CBA_Permanent:
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
                matrix_calc = axis_reference.matrix_world
            elif axis_type == "GLOBAL":
                matrix_calc = matrix_world

            for e in bm.edges:
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
        bgl.glLineWidth(2)
        verts_axes = CBA_Permanent.get_verts()
        for i, color in enumerate(((1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1))):
            coords = verts_axes[i]
            shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")
            batch = batch_for_shader(shader, "LINES", {"pos": coords})
            shader.bind()
            shader.uniform_float("color", color)
            batch.draw(shader)
