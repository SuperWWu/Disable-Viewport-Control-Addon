bl_info = {
    "name": "Disable Viewport Control",
    "author": "Woody",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > View or Shift + V",
    "description": "Easily able to disable or enable viewport for selected or unselected objects, perfect for speeding up proformance.",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy

#
# Disable Viewport Coontrol Panel Type
#
class OBJECT_PT_CustomPanel(bpy.types.Panel):
    # bl Properties
    bl_label = "Disable Viewport Control"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'View'
    bl_options = {'DEFAULT_CLOSED'}
    
    # draw Function
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("object.disable_viewport_selected", text="Disable Selected", icon = "RESTRICT_VIEW_ON")
        row = layout.row()
        row.operator("object.disable_viewport_unselected", text="Disable Unselected", icon = "RESTRICT_VIEW_ON")
        row = layout.row()
        layout.operator("object.disable_collection", text="Disable Collection", icon = "OUTLINER_COLLECTION")
        row = layout.row()
        row.operator("object.enable_viewport", text="Enable All", icon = "RESTRICT_VIEW_OFF")

#
# Disable Viewport for Selected Objects Operator Type
#
class OBJECT_OT_DisableViewportSelected(bpy.types.Operator):
    # bl Properties
    bl_label = "Disable Viewport for Selected Objects"
    bl_idname = "object.disable_viewport_selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    # execute Function
    def execute(self, context):
        disable_viewport_for_selected()
        return {'FINISHED'}

#
# Disable Viewport for Unselected Objects Operator Type
#
class OBJECT_OT_DisableViewportUnselected(bpy.types.Operator):
    # bl Properties
    bl_label = "Disable Viewport for Unselected Objects"
    bl_idname = "object.disable_viewport_unselected"
    bl_options = {'REGISTER', 'UNDO'}
    
    # execute Function
    def execute(self, context):
        disable_viewport_for_unselected()
        return {'FINISHED'}
#
# Disable Viewport for Selected Objects Collection Operator Type
#
class OBJECT_OT_disable_collection(bpy.types.Operator):
    bl_idname = "object.disable_collection"
    bl_label = "Disable Collection"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected_objs = context.selected_objects
        collections_to_disable = set()

        for obj in selected_objs:
            collections_to_disable.update(obj.users_collection)
        
        for collection in collections_to_disable:
            collection.hide_viewport = True
        
        return {'FINISHED'}

#
# Enable Viewport for All Objects Operator Type
#
class OBJECT_OT_EnableViewport(bpy.types.Operator):
    # bl Properties
    bl_label = "Enable Viewport for All Objects"
    bl_idname = "object.enable_viewport"
    bl_options = {'REGISTER', 'UNDO'}
    
    # execute Function
    def execute(self, context):
        enable_viewport()
        return {'FINISHED'}

#
# Disable Selected Function
#
def disable_viewport_for_selected():
    for obj in bpy.context.selected_objects:
        obj.hide_viewport = True

#
# Disable Unselected Function
#
def disable_viewport_for_unselected():
    for obj in bpy.context.scene.objects:
        if not obj.select_get():
            obj.hide_viewport = True
        else:
            obj.hide_viewport = False

#
# Enable All Function
#
def enable_viewport():
    for obj in bpy.context.scene.objects:
        obj.hide_viewport = False
        
    # Enable all collections
    for collection in bpy.data.collections:
        collection.hide_viewport = False
        collection.hide_render = False
        collection.hide_select = False

#
# Store keymaps here to access them later
#
addon_keymaps = []

#
# Disable Menu
#
class VIEW3D_MT_disable_viewport_menu(bpy.types.Menu):
    bl_label = "Disable for Viewport Menu"
    bl_idname = "VIEW3D_MT_disable_viewport_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.disable_viewport_selected", text="Disable Viewport for Selected")
        layout.operator("object.disable_viewport_unselected", text="Disable Viewport for Unselected")
        layout.operator("object.disable_collection", text="Disable Viewport for Collection")
        layout.operator("object.enable_viewport", text="Enable All")
#
# Define the classes to register
#
classes = [
    OBJECT_PT_CustomPanel,
    OBJECT_OT_DisableViewportSelected,
    OBJECT_OT_disable_collection,
    OBJECT_OT_DisableViewportUnselected,
    OBJECT_OT_EnableViewport,
    VIEW3D_MT_disable_viewport_menu,
]

#
# Register Functions
#
def register():
    # Register Functions
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode')
    kmi = km.keymap_items.new("wm.call_menu", 'V', 'PRESS', shift=True)
    kmi.properties.name = "VIEW3D_MT_disable_viewport_menu"

def unregister():
    # Unregister Functions
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    # Remove Keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.get('Object Mode')
    if km:
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu' and kmi.properties.name == "VIEW3D_MT_disable_viewport_menu":
                km.keymap_items.remove(kmi)

#
# Main
#
if __name__ == "__main__":
    register()