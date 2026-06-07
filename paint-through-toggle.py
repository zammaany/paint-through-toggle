bl_info = {
    "name": "Paint Through Toggle",
    "author": "Masoud Zamani",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "location": "Texture Paint",
    "description": "Press C to switch between Surface Mode and Paint Through Mode",
    "category": "Paint",
}

import bpy

addon_keymaps = []


class PAINT_OT_toggle_paintthrough(bpy.types.Operator):
    bl_idname = "paint.toggle_paintthrough"
    bl_label = "Toggle Paint Through"
    bl_description = "Toggle Paint Through / Surface Mode"

    def execute(self, context):
        ip = context.tool_settings.image_paint

        # Determine new state from Occlude
        current = getattr(ip, "use_occlude", True)
        state = not current

        # Toggle settings if they exist
        if hasattr(ip, "use_occlude"):
            ip.use_occlude = state

        if hasattr(ip, "use_backface_culling"):
            ip.use_backface_culling = state

        if hasattr(ip, "use_normal_falloff"):
            ip.use_normal_falloff = state

        # Clear notification
        if state:
            self.report(
                {'INFO'},
                "SURFACE MODE | Occlude ON | Backface Culling ON | Normal Falloff ON"
            )
        else:
            self.report(
                {'INFO'},
                "PAINT THROUGH MODE | Occlude OFF | Backface Culling OFF | Normal Falloff OFF"
            )

        return {'FINISHED'}


def register():
    bpy.utils.register_class(PAINT_OT_toggle_paintthrough)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name="Image Paint", space_type='EMPTY')

        kmi = km.keymap_items.new(
            "paint.toggle_paintthrough",
            type='C',
            value='PRESS'
        )

        addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    bpy.utils.unregister_class(PAINT_OT_toggle_paintthrough)


if __name__ == "__main__":
    register()