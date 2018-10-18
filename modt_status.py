#!/usr/bin/env python

# Requires pyusb and permissions to read/write the mod-t via USB.
# Just polls the Mod-T for status JSON

import sys
import os
import usb.core
import usb.util
import time
import json

# Read pending data from MOD-t (bulk reads of 64 bytes)
def read_modt(ep):
 text=''.join(map(chr, dev.read(ep, 64)))
 fulltext = text
 while len(text)==64:
        text=''.join(map(chr, dev.read(ep, 64)))
        fulltext = fulltext + text
 return fulltext

# Find MOD-t usb device
dev = usb.core.find(idVendor=0x2b75, idProduct=0x0002)

# was it found?
if dev is None:
    raise ValueError('Device not found')

#Finally, loop and query mod-t status every 5 seconds
while True:
 dev.write(4, '{"metadata":{"version":1,"type":"status"}}')
 res = read_modt(0x83)
 try:
  parsed = json.loads(res)
  print(json.dumps(parsed, indent=4, sort_keys=True))
 except Exception:
  print(res)
 time.sleep(5)
