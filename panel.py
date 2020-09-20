import bpy

class Anton_PT_Panel(bpy.types.Panel):
    bl_idname = 'ANTON_PT_panel'
    bl_label = 'anton'
    bl_category = 'anton'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, 'workspace_path')

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, "number_of_forces")
        rowsub.operator('anton.forceupdate', icon='ADD')

        for item in scene.forceprop:
            row = layout.row()
            row.label(text=' ')
            row.prop(item, 'magnitude')
            scene.forced_magnitudes['FORCE_{}'.format(item.name)] = item.magnitude
            row.operator('anton.directionupdate', icon='FULLSCREEN_ENTER').force_id = 'FORCE_{}'.format(item.name)

        col = layout.column()
        col.operator('anton.define', text='Define')

        row = layout.row()
        row.label(text=" ")

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, 'material')

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, "res")

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, "volumina_ratio")
        rowsub.prop(scene.anton, "penalty_exponent")

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, 'nds_density')
        rowsub.prop(scene.anton, 'precision')

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, 'number_of_iterations')

        rowsub = layout.row(align=True)
        rowsub.alignment = 'CENTER'
        rowsub.prop(scene.anton, "include_forced")
        rowsub.prop(scene.anton, "include_fixed")

        col = layout.column()
        col.operator('anton.process', text='Generate')

        row = layout.row()
        row.label(text=" ")

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, 'viz_iteration')
        rowsub.prop(scene.anton, "density_out")

        col = layout.column()
        col.operator('anton.visualize', text='Visualize')

        row = layout.row()
        row.label(text=" ")

        row = layout.row(align=True)
        row.alignment = 'RIGHT'
        row.label(text="Made with")
        row.label(icon='FUND')

