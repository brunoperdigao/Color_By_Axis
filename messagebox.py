import bpy

class CBA_OT_MessageBox(bpy.types.Operator):
    bl_idname = "message.messagebox"
    bl_label = ""
 
    message_line1: bpy.props.StringProperty(
        name = "message",
        description = "message",
        default = ''
    )

    message_line2: bpy.props.StringProperty(
        name = "message",
        description = "message",
        default = ''
    )
 
    def execute(self, context):
        self.report({'WARNING'}, self.message_line1 + self.message_line2    )
        print(self.message_line1, self.message_line2)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True) 
        col.label(text="Warning!", icon='ERROR')
        col.label(text=self.message_line1)
        if self.message_line2:
            col.label(text=self.message_line2)
        col.label(text="")