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
from bpy.types import Operator
from bpy.props import StringProperty
from . preset_support import *

skeleton_keymap = None

def ShowMessageBox(message = "", icon = 'INFO'):
    """ a hack that uses a popup menu as a message box"""
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, icon=icon)

# You can't attach operator properties to a panel, so instead, this creates
# example properties and attaches them to the Scene type so they can be
# accessed in one of the panels
# see also https://docs.blender.org/api/current/bpy.props.html

def updater(self, context):
    """ A hook called when any of the global properties change.
        It simply sets a class variable to indicate that the change has happened.
    """
    SKELETON_OT_Message.need_update = True

# These are the global versions of the properties, attached to Scene because why not?
def add_properties():
    bpy.types.Scene.name_from = bpy.props.StringProperty(
        name="who from",
        description="Name of the sender",
        default="Marty",
        update=updater,
    )
    bpy.types.Scene.name_to = bpy.props.StringProperty(
        name="who to",
        description="Name of the receiver",
        default="Bruce",
        update=updater,
    )
    bpy.types.Scene.message_text = bpy.props.StringProperty(
        name="message text",
        description="text of the message",
        default="Hello",
        update=updater,
    )

def remove_properties():
    del bpy.types.Scene.message_text
    del bpy.types.Scene.name_to
    del bpy.types.Scene.name_from

# See https://docs.blender.org/api/current/bpy.types.Operator.html for a brief
# example of an operator.
# See https://docs.blender.org/api/current/bpy.types.Operator.html#bpy.types.Operator.bl_options
# for a discussion of bl_options
# See https://sinestesia.co/blog/tutorials/using-blenders-presets-in-python/
# for an overview of using presets
class SKELETON_OT_Message(Operator):
    """ Skeleton Operator
        All this does is report a message as info in the info window.
        An addon preference toggles whether it also displays a message
        in a popup in the viewport.
    """
    bl_idname = "skeleton.message"
    bl_label = "I'm a Skeleton Operator"
    bl_description = "report a structured info message"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    # Since you can't display operator properties in a panel we keep both the global
    # versions above and the local versions here.  If we don't want the overkill of
    # the panel display than we can kill the global versions and the functionality
    # supporting keeping the two in sync
    name_from : bpy.props.StringProperty(
            name="who from",
            description="Name of the sender",
            default="Marty",
        )

    name_to : bpy.props.StringProperty(
            name="who to",
            description="Name of the receiver",
            default="Bruce",
        )

    message_text : bpy.props.StringProperty(
            name="message text",
            description="text of the message",
            default="Hello",
        )

    need_update = False   

    def update_locals(self, context):
        self.name_to = context.scene.name_to
        self.name_from = context.scene.name_from
        self.message_text = context.scene.message_text

    # Because of the inability to display operator properties in a panel, this
    # function updates the global copies if the local copy changes.
    def update_globals(self, context):
        context.scene.name_to = self.name_to
        context.scene.name_from = self.name_from
        context.scene.message_text = self.message_text

    @classmethod
    # https://docs.blender.org/api/current/bpy.types.Operator.html#bpy.types.Operator.poll
    def poll(cls, context):
        if context.mode == "OBJECT":
            return True
        else:
            cls.poll_message_set("Only works in OBJECT mode")
            return False

    # https://docs.blender.org/api/current/bpy.types.Operator.html#bpy.types.Operator.execute
    def execute(self, context):

        if self.need_update:
            self.update_locals(context)

        # for preferences usage see
        # https://docs.blender.org/api/current/bpy.types.AddonPreferences.html
        preferences = context.preferences
        addon_preferences = preferences.addons[__package__].preferences
        if addon_preferences.doPopup:
            ShowMessageBox(f"{self.name_from} says {self.message_text} to {self.name_to}")

        # Something harmless for the operator to do
        self.report({'INFO'},
            f"{self.name_from} just wanted to say {self.message_text}, {self.name_to}.")

        # Because you can't display operator properties in a panel
        # make sure the global versions are consistent with the local
        self.update_globals(context)
        # The call to updateGlobal will cause the global's updater
        # function to be called, causing need_update to be set to True
        # but we don't need an update so we override that change before
        # leaving the function.
        SKELETON_OT_Message.need_update = False
        return {'FINISHED'}

    # https://docs.blender.org/api/current/bpy.types.Operator.html#bpy.types.Operator.invoke
    # https://docs.blender.org/api/current/bpy.types.Operator.html#invoke-function
    # enable this if you want a popup with confirmation that allows setting the operator
    # properties before invoking the execute routine.
    #def invoke(self, context, event):
        # https://docs.blender.org/api/current/bpy.types.Operator.html#dialog-box
    #   return context.window_manager.invoke_props_dialog(self)

    # https://docs.blender.org/api/current/bpy.types.Operator.html#custom-drawing
    def draw(self, context):
        row = self.layout
        row.prop(self, "name_from", text="From")
        row.prop(self, "name_to", text="To")
        row.prop(self, "message_text", text="Message")

    # Local convention.  If a class wants to add menus or keymaps or other
    # custom bits, it does so through an initialize routine that is called
    # from __init__'s register routine after the class is registered.
    def initialize():
        add_properties()
        copy_presets(__package__, "operator", "skeleton.message")
        key_config = bpy.context.window_manager.keyconfigs.addon
        if key_config:
            key_map = key_config.keymaps.new(name='3D View', space_type='VIEW_3D')
            key_entry = key_map.keymap_items.new(SKELETON_OT_Message.bl_idname,
                                                                type='W',
                                                                value='PRESS',
                                                                ctrl=True,
            )
            skeleton_keymap = (key_map, key_entry)

    # Local convention.  If a class has an initialize it might also need to
    # undo the initialization through this routine that is called from
    # __init__'s unregister routine before the class is unregistered.
    def deinitialize():
        if skeleton_keymap:
            key_map, key_entry = skeleton_keymap
            key_map.keymap_items.remove(key_entry)
            bpy.context.window_manager.keyconfigs.addon.keymaps.remove(key_map)
        remove_properties()