import controller_include as ci
import ach
import diff_drive

c = ach.Channel(ci.CONTROLLER_REF_NAME)
controller = ci.CONTROLLER_REF()
while(1):
  controller.mot1 = 0x1FF
  controller.mot2 = -0x1FF
  c.put(controller)
