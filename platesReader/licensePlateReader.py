
import numpy as np
import cv2
import sys
import time
import subprocess
import json
import threading

WINDOW_NAME = 'openalpr'
FRAME_SKIP = 30

def open_stream(stream_url):
  if stream_url is '0':
    stream_url = 0
  cap = cv2.VideoCapture(stream_url)
  if not cap.isOpened():
      print('Error opening video stream')
      sys.exit(1)
  return cap


def save_frame_to_jpg(frame, frame_path):
  cv2.imwrite(frame_path, frame)


def read_plate_from_frame(frame_path, plate_found_callback):
  try:
    output = subprocess.run(['alpr', '-j', '-c eu', '-n 3', frame_path],
                            stdout=subprocess.PIPE).stdout.decode('utf-8')
    # result = json.loads(output)

    # results = result['results']
    # if results:
      # return [output, result]
    # else:
      # return None
    
    if output:
      return output
    else:
      return None
        # best_candidate = results[0]
        # print('found plate {} confidence {}'.format(
        #     best_candidate['plate'], best_candidate['confidence']))
    # def dfdf(camera_id, frame_path, result, raw_result):
    # plate_found_callback(result, )

  except Exception as e:
    print('fuck {}'.format(e))
    print(output)


def read_plate_realtime(camera_id, stream_url, frames_folder, plate_found_callback):
  capture = open_stream(stream_url)
  _frame_number = 0
  while(True):
    ret_val, frame = capture.read()

    if not ret_val:
      print('VidepCapture.read() failed. Exiting...')
      break

    _frame_number += 1
    if _frame_number % FRAME_SKIP != 0:
      continue

    _frame_number = 0

    frame_path = '{}/{}_{}.jpg'.format(frames_folder, camera_id, _frame_number)
    save_frame_to_jpg(frame, frame_path)

    read_plate_from_frame(frame_path, plate_found_callback)


class PlateReaderThread(threading.Thread):
  def __init__(self, camera_id, stream_url, frames_folder, plate_found_callback):
    self.camera_id = camera_id
    self.stream_url = stream_url
    self.frames_folder = frames_folder
    self.plate_found_callback = plate_found_callback
    threading.Thread.__init__(self)
    self._stop_event = threading.Event()

  def run(self):
    print('starting thread {}', self.camera_id)
    capture = open_stream(self.stream_url)
    _frame_number = 0
    while not self._stop_event.is_set():
      try:
        ret_val, frame = capture.read()

        if not ret_val:
          print('VidepCapture.read() failed. Exiting...')
          break

        _frame_number += 1
        if _frame_number % FRAME_SKIP != 0:
          continue

        _frame_number = 0

        frame_path = '{}/{}_{}.jpg'.format(self.frames_folder, self.camera_id, _frame_number)
        save_frame_to_jpg(frame, frame_path)

        raw_output = read_plate_from_frame(frame_path, self.plate_found_callback)

        if raw_output is None:
          continue

        result = json.loads(raw_output)


        results = result['results']

        if results:
          best_candidate = results[0]
          print('found plate', best_candidate)
          self.plate_found_callback(self.camera_id, frame_path, result, raw_output)
      except Exception as e:
        print('PlateReaderThread', self.camera_id, e)

    print('thread {} killed', self.camera_id)

  def stop(self):
    self._stop_event.set()
    print('killing thread {}', self.camera_id)
    self.join(1)