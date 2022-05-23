import bpy

from bpy.types import Panel

class QTTC_PT_Panel(Panel):
    bl_space_type = 'TOPBAR'
    bl_region_type = 'HEADER'
    bl_label = "Converter"
    bl_category = "Eden's Rolling Line Utils"

    def draw(self, context):
        
        layout = self.layout
        layout.separator()
        layout.operator('qttc.convert', text="Convert")