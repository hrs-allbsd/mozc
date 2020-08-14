# -*- coding: utf-8 -*-
# Copyright 2010-2018, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__author__ = "mukai"

import optparse
import sys

class Mapping(object):
  def __init__(self, options):
    self._mapname = options.mapname
    self._key_type = options.key_type
    self._result_type = options.result_type
    self._filename = options.filename

  def PrintLine(self, line):
    columns = line.strip().split(b'\t')
    if len(columns) != 2:
      return
    (key, value) = columns
    mapname = self._mapname
    if key.startswith(b'Shift '):
      mapname += 'Shift'
      key = key[len(b'Shift '):len(key)]

    if self._key_type == 'unsigned short' and not key.startswith(b'kVK_'):
      key = b'kVK_ANSI_' + key

    if self._result_type == 'const char *':
      value = b'"%b"' % b''.join([b'\\x%x' % c for c in value])
    elif self._result_type == 'KeyEvent::SpecialKey':
      value = b'KeyEvent::' + value
    print('  (*k%s)[%s] = %s;' % (mapname, key.decode('utf-8'), value.decode('utf-8')))

  def PrintHeader(self):
    print("""// Copyright 2009 Google Inc.  All Rights Reserved.
// Author: mukai
//
// This file is automatically generated by
// generate_maping.py.
// Do not edit directly and do not include this from any file other
// than KeyCodeMap.mm

namespace {
static std::map<%(key_type)s, %(result_type)s> *k%(mapname)s = nullptr;
static std::map<%(key_type)s, %(result_type)s> *k%(mapname)sShift = nullptr;
static once_t kOnceFor%(mapname)s = MOZC_ONCE_INIT;
void Init%(mapname)s() {
  if (k%(mapname)s != nullptr || k%(mapname)sShift != nullptr) {
    return;
  }
  k%(mapname)s = new(std::nothrow)std::map<%(key_type)s, %(result_type)s>;
  if (k%(mapname)s == nullptr) {
    return;
  }
  k%(mapname)sShift = new(std::nothrow)std::map<%(key_type)s, %(result_type)s>;
  if (k%(mapname)sShift == nullptr) {
    delete k%(mapname)s;
    k%(mapname)s = nullptr;
    return;
  }
""" % {'key_type': self._key_type,
       'mapname': self._mapname,
       'result_type': self._result_type })

  def PrintFooter(self):
    print("""}
}  // namespace
""" % {'mapname': self._mapname})

  def Print(self):
    self.PrintHeader()
    with open(self._filename, 'rb') as file:
      for line in file:
        self.PrintLine(line)
    self.PrintFooter()

def ParseOption():
  """ Parse command line options. """
  parser = optparse.OptionParser()
  parser.add_option("--mapname", dest="mapname")
  parser.add_option("--key_type", dest="key_type")
  parser.add_option("--result_type", dest="result_type")
  parser.add_option("--filename", dest="filename")
  (options, unused_args) = parser.parse_args()

  if not options.mapname:
    print("Error: the output map name should be specified.")
    sys.exit(2)
  if not options.key_type:
    options.key_type = 'unsigned short'
  if not options.result_type:
    print("Error: the result type of the output map should be specified.")
  if not options.filename:
    print("Error: the file name is not specified.")
  return options

def main():
  options = ParseOption()
  Mapping(options).Print()

if __name__ == '__main__':
  main()
