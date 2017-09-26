#/usr/bin/env python3
import sys, os
import time
sys.path.insert(0,'../../lib')
for swc in ['BspService', 'common', 'FreeRunningTimer', 'SteeringWheelButtonFeedback']:
   sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../'+swc)))
import autosar
start=time.time()
from SteeringWheelButtonReader import SteeringWheelButtonReader
from BspService import BspService


derived_dir = 'derived'
if not os.path.exists(derived_dir):
   os.makedirs(derived_dir)

ws = autosar.workspace()
ws.apply(SteeringWheelButtonReader)
ws.apply(BspService)
partition = autosar.rte.Partition()
partition.addComponent(ws.find('/ComponentType/SteeringWheelButtonReader'))
partition.addComponent(ws.find('/ComponentType/BspService'))
swc1 = ws.find('/ComponentType/SteeringWheelButtonReader')
swc2 = ws.find('/ComponentType/BspService')
for port in swc1.requirePorts:
   print(port.name)
print('BspService:')
for port in swc2.providePorts:
   print(port.name)


typeGenerator = autosar.rte.TypeGenerator(partition)
typeGenerator.generate(derived_dir+'/Rte_Type.h')
headerGenerator = autosar.rte.ComponentHeaderGenerator(partition)
headerGenerator.generate(derived_dir)
rteGenerator = autosar.rte.RteGenerator(autosar.rte.Config(partition))
rteGenerator.generate(derived_dir)
delta=float(time.time()-start)*1000
print('%dms'%(round(delta)))
