import operations
import time
import os
import logging

os.system('chmod +x rec_video.py')
print('test mode')
try:
    operations.test_mode()
    print('end test mode')
    while (operations.lift_off() == False) :
        time.sleep(1)
    print('flight mode')
    operations.logger.info('Liftoff signal received')
    while (operations.ugravity() == False):
        time.sleep(1)
    operations.logger.info('Microgravity signal received')
    print('ugravity started')

except:
    print('except geral')

operations.rec_video()
operations.perform_experiment()
print('Experiment finished')
operations.logger.info('Experiment finished')
