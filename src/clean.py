"""
This file is the CLEAN step of the fraud detection pipeline.

It checks the loaded transaction data for two kinds of problems:
missing columns, and missing (blank) values in any column. It does not
fix anything - it only reports what it finds, so a human decides what
to do about it.
"""
