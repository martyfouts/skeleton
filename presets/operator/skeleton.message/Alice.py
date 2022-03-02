import bpy
op = bpy.context.active_operator

op.name_from = 'Alice'
op.name_to = 'Bob'
op.message_text = 'gotcha!'
