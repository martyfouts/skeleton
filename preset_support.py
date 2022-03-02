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

from bpy.utils import resource_path
from pathlib import Path
from shutil import copy2

def copy_presets(addon, category, folder):
    """ Copy presets from the addons folder to the presets folder.
        See https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html
        for the standard directory layout
    """
    USER = Path(resource_path('USER'))

    # If there are no presets associated with the addon there is nothing to do
    src = USER / "scripts/addons" / addon / "presets" / category / folder
    if not src.exists():
        return

    # If the destination folder already exists do not overwrite.
    dst = USER / "scripts/presets" / category / folder
    if dst.exists():
        return

    dst.mkdir()
    dstpath = str(dst)
    for file in src.glob("*.py"):
        copy2(str(file), dstpath)