from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import time
import numpy as numpy
import picamera

from PIL import Image
from tflite_runtime.interpreter import Interpreter
