import bpy
op = bpy.context.active_operator

op.name_from = 'Bob'
op.name_to = 'Alice'
op.message_text = 'gotcha!'

