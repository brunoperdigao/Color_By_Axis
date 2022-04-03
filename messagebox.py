import bpy

class CBA_OT_MessageBox(bpy.types.Operator):
    bl_idname = "message.messagebox"
    bl_label = ""
 
    message: bpy.props.StringProperty(
        name = "message",
        description = "message",
        default = ''
    )
 
    def execute(self, context):
        self.report({'WARNING'}, self.message)
        print(self.message)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)
 
    def draw(self, context):
        self.layout.label(text=self.message)
        self.layout.label(text="")