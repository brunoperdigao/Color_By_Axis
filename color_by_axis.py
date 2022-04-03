from calendar import c
import bpy
import bmesh
import bgl
import gpu
import copy
import mathutils
from gpu_extras.batch import batch_for_shader

class CBA_OT_Color_by_Axis(bpy.types.Operator):
    bl_idname = "object.color_by_axis"
    bl_label = "Color By Axis"
    bl_description = "Operator to color edges by axis"
    bl_options = {'REGISTER'}

    axis_type: bpy.props.StringProperty(name="Axis Type")
    

    def __init__(self):
        self.draw_handle = None
        self.draw_event = None

        self.widgets = []

    def invoke(self, context, event):

        self.create_batch()

        args = (self, context)
        self.register_handlers(args, context)

        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}


    def register_handlers(self, args, context):
        self.draw_handle= bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback, args, "WINDOW", "POST_VIEW"
        )
        '''
        self.draw_handle_x= bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_x, args, "WINDOW", "POST_VIEW"
        )

        self.draw_handle_y= bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_y, args, "WINDOW", "POST_VIEW"
        )

        self.draw_handle_z= bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_z, args, "WINDOW", "POST_VIEW"
        )'''

        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)

    def unregister_handlers(self, context):

        context.window_manager.event_timer_remove(self.draw_event)

        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, "WINDOW")
        

        self.draw_handle = None
        self.draw_event = None

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        if event.type in {"ESC"}:
            self.unregister_handlers(context)
            return {'CANCELLED'}

        return {"PASS_THROUGH"}

    def finish(self):
        self.unregister_handlers(context)
        return {"FINISHED"}
    
    def get_verts(self):
        verts_x = []
        verts_y = []
        verts_z = []
        verts_by_edges = []
        

        for o in bpy.context.objects_in_mode:
            
            # Here I get the object location, scale and rotation, so I can mix with the rotation of a reference object.
            # That way I can compare the vertices locations based on the reference axis
            
            obj_location = o.matrix_world.to_translation()
            obj_scale = o.matrix_world.to_scale()
            obj_rotation = o.matrix_world.to_euler()

            # Object global matrix
            world_matrix = o.matrix_world
            custom_matrix = None

            bm = bmesh.from_edit_mesh(o.data)

            # Calling the property directly from the context
            axis_reference = bpy.context.scene.axis_ref

            if self.axis_type == 'REFERENCE' and axis_reference:
            # ATTENTION for now this is referencing the object by name. Have to improve that        
            # Get the reference rotation
                #custom_euler = copy.copy(bpy.context.scene.objects['Empty'].matrix_world.to_euler())
                custom_euler = copy.copy(axis_reference.matrix_world.to_euler())
                                                
                custom_euler[0] = custom_euler[0] - obj_rotation[0]
                if custom_euler[0] < 0:
                    custom_euler[0] = custom_euler[0] * -1
                custom_euler[1] = custom_euler[1] - obj_rotation[1]
                if custom_euler[1] < 0:
                    custom_euler[1] = custom_euler[1] * -1
                custom_euler[2] = custom_euler[2] - obj_rotation[2]
                if custom_euler[2] < 0:
                    custom_euler[2] = custom_euler[2] * -1
                
                # Custom matrix, mixed with the reference rotation
                custom_matrix = mathutils.Matrix.LocRotScale(obj_location, custom_euler, obj_scale)
            
            
            for e in bm.edges:
                #if e.select:
                v1 = e.verts[0].co
                v2 = e.verts[1].co
                
                v1_global = world_matrix @ e.verts[0].co
                v2_global = world_matrix @ e.verts[1].co
                
                if not custom_matrix:
                    pass
                else:


                    v1_custom = custom_matrix @ e.verts[0].co
                    v2_custom = custom_matrix @ e.verts[1].co

                    # Have to do this rounding for precision problems
                    # I noticed this when the object location were 180 degress different from the reference.
                    v1_x_round = round(v1_custom[0], 4)
                    v1_y_round = round(v1_custom[1], 4)
                    v1_z_round = round(v1_custom[2], 4)
                    v2_x_round = round(v2_custom[0], 4)
                    v2_y_round = round(v2_custom[1], 4)
                    v2_z_round = round(v2_custom[2], 4)

                    if (v1_y_round == v2_y_round) & (v1_z_round == v2_z_round): # Compare the rounded numbers
                        v1 = v1_global
                        v2 = v2_global
                        verts_x.append(v1)    
                        verts_x.append(v2)  

                    elif (v1_x_round == v2_x_round) & (v1_z_round == v2_z_round): 
                        v1 = v1_global
                        v2 = v2_global
                        verts_y.append(v1)    
                        verts_y.append(v2)
                
                    elif (v1_x_round == v2_x_round) & (v1_y_round == v2_y_round): 
                        v1 = v1_global
                        v2 = v2_global
                        verts_z.append(v1)    
                        verts_z.append(v2)
                
                if self.axis_type == 'GLOBAL':
                    if (v1_global[1] == v2_global[1]) & (v1_global[2] == v2_global[2]): # Compare the rounded numbers
                        v1 = v1_global
                        v2 = v2_global
                        verts_x.append(v1)    
                        verts_x.append(v2)  

                    elif (v1_global[0] == v2_global[0]) & (v1_global[2] == v2_global[2]): 
                        v1 = v1_global
                        v2 = v2_global
                        verts_y.append(v1)    
                        verts_y.append(v2)
                    
                    elif (v1_global[0] == v2_global[0]) & (v1_global[1] == v2_global[1]): 
                        v1 = v1_global
                        v2 = v2_global
                        verts_z.append(v1)    
                        verts_z.append(v2)

                if self.axis_type == 'LOCAL':
                    if (v1[1] == v2[1]) & (v1[2] == v2[2]): # Compare the rounded numbers
                        v1 = v1_global
                        v2 = v2_global
                        verts_x.append(v1)    
                        verts_x.append(v2)  

                    elif (v1[0] == v2[0]) & (v1[2] == v2[2]): 
                        v1 = v1_global
                        v2 = v2_global
                        verts_y.append(v1)    
                        verts_y.append(v2)
                    
                    elif (v1[0] == v2[0]) & (v1[1] == v2[1]): 
                        v1 = v1_global
                        v2 = v2_global
                        verts_z.append(v1)    
                        verts_z.append(v2)
            
        return verts_x, verts_y, verts_z
    
    def create_batch(self):
        
        vertices_x, vertices_y, vertices_z = self.get_verts()
        self.shader_x = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch_x = batch_for_shader(self.shader_x, 'LINES', {"pos": vertices_x})
                
        self.shader_y = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch_y = batch_for_shader(self.shader_y, 'LINES', {"pos": vertices_y})
        
        self.shader_z = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch_z = batch_for_shader(self.shader_z, 'LINES', {"pos": vertices_z})

    def draw_callback(self, op, context):
        bgl.glLineWidth(5)
        self.shader_x.bind()
        self.shader_x.uniform_float("color", (1, 0, 0, 1))
        self.batch_x.draw(self.shader_x)

        #bgl.glLineWidth(5)
        self.shader_y.bind()
        self.shader_y.uniform_float("color", (0, 1, 0, 1))
        self.batch_y.draw(self.shader_y)

        #bgl.glLineWidth(5)          
        self.shader_z.bind()
        self.shader_z.uniform_float("color", (0, 0, 1, 1))
        self.batch_z.draw(self.shader_z)