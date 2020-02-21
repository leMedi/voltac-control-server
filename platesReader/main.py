import logging
import threading
import time
from models.Camera import Camera
from platesReader.licensePlateReader import read_plate_realtime, PlateReaderThread
from core.logger import get_logger

logger = get_logger("ALPR")


# running_threads = list()

# def start_deamon(cameras):
#   global running_threads

#   for camera in cameras:
#     # thread = threading.Thread(target=read_plate_realtime, args=(camera['name'], camera['rtsp'], './frames'))
#     # thread.start()
#     thread = PlateReaderThread(camera['name'], camera['rtsp'], './frames')
#     running_threads.append(thread)
#     thread.start()


# def stop_deamon():
#   print('s running_threads {}'.format(len(running_threads)))
#   for thread in running_threads:
#     thread.stop()
#     running_threads.remove(thread)
#   print('running_threads {}'.format(len(running_threads)))

# def restart_deamon(cameras):
#   stop_deamon()
#   time.sleep(10)
#   start_deamon(cameras)

# def read_xx():
#   cameras = Camera.query.all()
#   restart_deamon(cameras)

class ALPR():
    def __init__(self, frames_folder, on_plate_found_callback):
      self.cameras = list()
      self.running_threads = {}
      self.frames_folder = frames_folder
      self.on_plate_found_callback = on_plate_found_callback

    def set_cameras(self, cameras):
      self.cameras = cameras

    def start(self):
      for camera in self.cameras:
        if camera.id in self.running_threads:
          logger.warning('{} [{}] camera thread already running'.format(camera.name, camera.id))
          continue
        thread = PlateReaderThread(camera.id, camera.rtsp, self.frames_folder, self.on_plate_found_callback)
        self.running_threads[camera.id] = thread
        thread.start()
        logger.debug('{} [{}] camera thread started {}'.format(camera.name, camera.id, camera.rtsp))
      logger.info('ALPR started {} threads'.format(len(self.cameras)))

    def stop(self):
      t = list(self.running_threads)
      for camera_id in t:
        thread = self.running_threads[camera_id]
        thread.stop()
        del self.running_threads[camera_id]

    def reload_cameras(self, cameras):
      self.stop()
      self.set_cameras(cameras)
      self.start()


class MASTER_ALPR():
  instance = None
  def __init__(self, frames_folder, on_plate_found_callback):
      if not MASTER_ALPR.instance:
          MASTER_ALPR.instance = ALPR(frames_folder, on_plate_found_callback)
      else:
          MASTER_ALPR.instance.frames_folder = frames_folder
  def __getattr__(self, name):
      return getattr(self.instance, name)

  def get_instance():
    return MASTER_ALPR.instance