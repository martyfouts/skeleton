# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.types import Panel, Operator, Menu
from . skeleton_ops import SKELETON_OT_Message
from bl_operators.presets import AddPresetBase
from . preset_support import *

# Add a preset menu that can be incorporated into the panel
# See https://docs.blender.org/api/current/bpy.types.Menu.html#preset-menus
class SKELETON_MT_presets(Menu):
    bl_label = "Greeting Presets"
    preset_subdir = "operator/skeleton.panel"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset


class SKELETON_OT_Presets(AddPresetBase, Operator):
    """Add the presets for the skeleton panel"""
    bl_idname = "skeleton.panel"
    bl_label = "Add Skeleton Preset"
    preset_menu = "SKELETON_MT_presets"
    # variable used for all preset values
    preset_defines = [
        "scene = bpy.context.scene"
    ]
    # properties to store in the preset
    preset_values = [
        "scene.name_from",
        "scene.name_to",
        "scene.message_text",
    ]
    # where to store the preset
    preset_subdir = "operator/skeleton.panel"
# ----- end of preset prep

class skeleton_panel_common:
    """ mixin class with common properties shared by all the skeleton panels
        At the moment there is only one panel, but typical addons will have
        at least multiple subpanels, if not adjacent panels.
    """
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "skeleton"
    bl_options = set()

class SKELETON_PT_sidebar(Panel, skeleton_panel_common):
    """Display preferences, properties, and a test button"""
    bl_label = "Closet"

    def draw(self, context):
        col = self.layout.column(align=True)

        # A button to invoke the operator
        prop = col.operator(SKELETON_OT_Message.bl_idname, text="Say Something")

        col.separator(factor=2.0)
        col.label(text="Preferences", icon="PREFERENCES")
        # for preferences usage see
        # https://docs.blender.org/api/current/bpy.types.AddonPreferences.html
        preferences = context.preferences
        addon_preferences = preferences.addons[__package__].preferences
        col.prop(addon_preferences, "doPopup")

        # You can't attach operator properties to a panel, so instead, this
        # displays the global properties and allows them to be changed 
        col.separator(factor=2.0)

        # Display the header with the preset menu and add/remove buttons
        row = col.row(align=True)
        row.label(text="Message")
        row.menu(SKELETON_MT_presets.__name__, text="", icon="PRESET")
        row.operator(SKELETON_OT_Presets.bl_idname, text="", icon="ADD")
        op = row.operator(SKELETON_OT_Presets.bl_idname, text="", icon="REMOVE")
        op.remove_active = True

        # Display the properties
        col.prop(context.scene, "name_from", text="from")
        col.prop(context.scene, "name_to", text="to")
        col.prop(context.scene, "message_text", text="say")

    def initialize():
        copy_presets(__package__, "operator", "skeleton.panel")


    