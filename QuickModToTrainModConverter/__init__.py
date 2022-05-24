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

bl_info = {
    "name" : "QuickMod To TrainMod Addon",
    "author" : "Eden",
    "description" : "",
    "blender" : (3, 0, 0),
    "version" : (0, 0, 3),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from . qttc_op import QTTC_OT_Convert
from . qttc_ui import QTTC_PT_Panel

classes = (QTTC_OT_Convert, QTTC_PT_Panel)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.TOPBAR_MT_file.append(QTTC_PT_Panel.draw)

def unregister():
    bpy.types.TOPBAR_MT_file.remove(QTTC_PT_Panel.draw)
    for c in classes:
        bpy.utils.unregister_class(c)
