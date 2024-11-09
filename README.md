# Deprecated
This repository is now deprecated. The examples apply to Blender versions 3.x. It has not been tested on newer versions of Blender.

This Blender Add-on is a skeleton add-on that I use as a starting point
for creating new small scale add-ons.

# General layout
This add-on takes the approach of placing presets in their own folder
and subdividing that folder based on whether they are operator
presets or panel presets. It places operators and panels in their
own separate files.  It is meant for small scale add-ons.

# General changes to customize it
- change `bl_info` to reflect the status of the add-on
- change 'skeleton' to the add-on name everywhere it appears
- change the imports and `classes` to match your actual classes
- write your own operators and panels as needed
- rewrite this file to match your new add-on

# Add-on Preferences support
`SkeletonAddonPreferences` is the class that supports drawing the
add-on's preferences in Preferences. Edit it to add properties
that you want to be saved for use by every instance of the add-on.
Remove the `doPopup` property in most cases.

# helper functions
## `preset_support.py`
See [Using Blender's Presets in Python](https://sinestesia.co/blog/tutorials/using-blenders-presets-in-python/)
for details. This file provides `copy_presets(addon, category, folder)`
a function that copies presets from where the addon installer unpacked
them when it unzipped the addon to the directories where they'll be
used.
## Added class methods
`initialize()` and `deinitialize()` can be added to any class that is
registered in init. If they are present they are called in `register`
and `unregister` respectively. This allows keeping local initialization
with the classes rather than forcing it all into the registration
routines.
## installation and removal
This skeleton follows the convention of using a loop in `register` and
`unregister` to handle all of the classes in an array called `classes`.
This allows limiting the number of places that have to be changed when
a class is added or deleted.

# Operators
The skeleton operators demonstrate the use of presets and Undo. They
include a workaround to the problem that you can't expose an operator's
properties in a panel.  There's a lot of code that can be removed if
that isn't necessary, but it's not clearly marked. (ToDo)

# Panels
The skeleton demonstrates having a side panel tab that contains both
an additional panel and a subpanel.  Since there are multiple classes
that will have common settings, it uses a helper mix-in class to
gather all of those settings in one place.



