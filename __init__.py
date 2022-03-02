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


# This is a skeleton 2.8+ addon.

# See https://wiki.blender.org/wiki/Process/Addons/Guidelines/metainfo
bl_info = {
    "name" : "Addon Skeleton",
    "description" : "A skeleton addon",
    "author" : "Marty Fouts <fouts@fogey.com>",
    "version" : (0, 0, 1),
    "blender" : (2, 80, 0),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "",
    "category" : "3D View"
}

# This bit is here because Python doesn't do recursive reloading 
# This works for a single level but I don't know if it will work
# if the imported modules import other modules for the package.
if 'bpy' in locals():
    from importlib import reload
    import sys
    for k, v in list(sys.modules.items()):
        if k.startswith(__package__ + "."):
            reload(v)
# End of recursive reload support

import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty

from . skeleton_ops import SKELETON_OT_Message
from . skeleton_panel import (SKELETON_PT_sidebar, 
                            SKELETON_MT_presets,
                            SKELETON_OT_Presets,
)

# An example of Add-on specific preferences modified from
# https://docs.blender.org/api/current/bpy.types.AddonPreferences.html
class SkeletonAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    doPopup: BoolProperty(
        name="Display a popup",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "doPopup")

classes = [
    SKELETON_OT_Message,
    SKELETON_PT_sidebar,
    SKELETON_MT_presets,
    SKELETON_OT_Presets,
    SkeletonAddonPreferences,
]

# See https://wiki.blender.org/wiki/Reference/Release_Notes/2.80/Python_API/Addons
# for a description of Addon registration in 2.8+
def register():
    for c in classes:
        bpy.utils.register_class(c)
        # Local convention.  If a class wants to add menus or keymaps or other
        # custom bits, it does so through an initialize routine that is called
        # from __init__'s register routine after the class is registered.
        if 'initialize' in dir(c):
            c.initialize()


def unregister():
    for c in classes:
        # Local convention.  If a class has an initialize it might also need to
        # undo the initialization through this routine that is called from
        # __init__'s unregister routine before the class is unregistered.
        if 'deinitialize' in dir(c):
            c.deinitialize()
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()