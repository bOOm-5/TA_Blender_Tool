#考察知识点
#StringProperty 字符串属性
#结合系统路径操作、文件导出
#参数条件分支逻辑
#界面提示信息拼接
#功能要求
#面板中提供：
#文本输入框：导出文件夹名（默认值：fbx_export）
#勾选框：仅导出选中物体（默认勾选）
#点击执行后，自动在桌面创建对应文件夹，将场景导出为 FBX 文件
#导出完成后提示：共导出 X 个物体，路径为 XXX
#空选且勾选「仅导出选中」时，弹出警告

import bpy
import os

class FBXToolProps(bpy.types.PropertyGroup):
    file_name : bpy.props.StringProperty(name = "导出文件夹名",default="fbx_export")
    only_selected : bpy.props.BoolProperty(name = "仅导出选中物体",default=True)
    
class TOOL_PT_FBX(bpy.types.Panel):
    bl_idname = "TOOL_PT_FBX"
    bl_label = "导出FBX文件"
    bl_space_type = 'VIEW_3D'
    bl_region_type  ='UI'
    bl_category = "TA工具箱"
    
    def draw(self,context):
        layout = self.layout
        props = context.scene.fbx_tool_props
        
        layout.prop(props,"file_name")
        layout.prop(props,"only_selected")
        
        layout.separator()
        layout.operator("tool.file_export",text="导出文件")
        
class TOOL_OT_FBX(bpy.types.Operator):
    bl_idname = "tool.file_export"
    bl_label = "导出FBX文件"
    bl_options = {'REGISTER','UNDO'}
    
    def execute(self,context):
        props = context.scene.fbx_tool_props
        file_name = props.file_name
        only_selected = props.only_selected
        
        if only_selected:
            selected_objs = bpy.context.selected_objects
            if len(selected_objs) == 0:
                self.report({'WARNING'},"亲爱的请先选中物体")
                return {'CANCELLED'}
        
        try:
            count = 0
            desktop = os.path.join(os.path.expanduser("~"),"Desktop")
            file_path = os.path.join(desktop,file_name)                
            
            if not os.path.exists(file_path):
                os.makedirs(file_path)
                
            export_path = os.path.join(file_path,"export_result.fbx")
            
            bpy.ops.export_scene.fbx(
                filepath=export_path,
                use_selection=only_selected
            )
            if only_selected:
                count = len(context.selected_objects)
            else:
                count = len(context.scene.objects)    
            
          
                    
        except Exception as e:
            self.report({'ERROR'},f"未知错误:{str(e)}")
            return {'CANCELLED'}
        
        else:
            self.report({'INFO'},f"共处理{count}个物体,导出路径:{file_path}")
            return {'FINISHED'}
def register():
    bpy.utils.register_class(FBXToolProps)
    bpy.types.Scene.fbx_tool_props = bpy.props.PointerProperty(type=FBXToolProps)
    
    bpy.utils.register_class(TOOL_OT_FBX)
    bpy.utils.register_class(TOOL_PT_FBX)
    
def unregister():
    bpy.utils.unregister_class(TOOL_PT_FBX)
    bpy.utils.unregister_class(TOOL_OT_FBX)
    
    del bpy.types.Scene.fbx_tool_props
    bpy.utils.unregister_class(FBXToolProps)
    
if __name__=="__main__":
    try:
        unregister()
    except:
        pass
    register()