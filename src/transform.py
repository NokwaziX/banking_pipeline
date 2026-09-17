"""
This file is the TRANSFORM step of the fraud detection pipeline.

It takes the loaded transaction data and calculates summary numbers
from it - things like the total fraud rate. It does not check for
problems (that's Clean's job) or save anything (that's Storage's job).
"""