#考察知识点
#PropertyGroup 属性组定义、BoolProperty 布尔属性
#面板自动绘制参数控件
#算子内读取参数并做条件判断
#完整的注册注销流程、撤销支持
#功能要求
#面板中提供两个可勾选选项：
#Z 轴位置归零（默认勾选）
#重置缩放为 1（默认勾选）
#选中多个物体后点击执行，仅处理网格类型物体
#根据勾选状态执行对应操作，未勾选的选项不执行
#空选时弹出黄色警告提示，操作成功弹出信息提示，异常弹出错误提示
#支持 Ctrl+Z 撤销


import bpy

class ReplaceToolProps(bpy.types.PropertyGroup):
    zero_z: bpy.props.BoolProperty(name = "Z轴位置归零",default = True)
    reset_scale: bpy.props.BoolProperty(name="重置缩放为1",default = True)#
    
class TOOL_PT_Replace(bpy.types.Panel):
    bl_idname = "TOOL_PT_Replace"
    bl_label = "批量归零重置"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TA工具箱"
    
    def draw(self,context):
        layout = self.layout
        props = context.scene.reset_tool_props#
        
        layout.prop(props,"zero_z")
        layout.prop(props,"reset_scale")
        
        layout.separator()
        layout.operator("tool.batch_reset",text="执行重置")
        
class TOOL_OT_Replace(bpy.types.Operator):
    bl_idname = "tool.batch_reset"
    bl_label = "批量归零重置"
    bl_options = {'REGISTER','UNDO'}
    
    def execute(self,context):
        props = context.scene.reset_tool_props#
        zero_z = props.zero_z#
        reset_scale = props.reset_scale#
        selected_objs = bpy.context.selected_objects
        
        if len(selected_objs) == 0:
            self.report({'WARNING'},"请先选中要处理的物体")
            return {'CANCELLED'}
        try:
            count = 0
            for obj in selected_objs:
                if obj.type == "MESH":
                    if props.zero_z:
                        obj.location.z = 0
                    if props.reset_scale:
                        obj.scale = (1,1,1)
                    
                    count +=1
                        
        except Exception as e:
            self.report({'ERROR'},f"操作失败：{str(e)}")
            return {'CANCELLED'}
        else:
            self.report({'INFO'},f"完成，共处理{count}个网格物体")
            return {'FINISHED'}
        
        
        
def register():
    bpy.utils.register_class(ReplaceToolProps)
    bpy.types.Scene.reset_tool_props = bpy.props.PointerProperty(type=ReplaceToolProps)
    
    bpy.utils.register_class(TOOL_OT_Replace)
    bpy.utils.register_class(TOOL_PT_Replace)
    
def unregister():
    bpy.utils.unregister_class(TOOL_PT_Replace)
    bpy.utils.unregister_class(TOOL_OT_Replace)
    
    del bpy.types.Scene.reset_tool_props
    bpy.utils.unregister_class(ReplaceToolProps)
    
if __name__=="__main__":
    try:
        unregister()
    
    except:
        pass
    
    register()