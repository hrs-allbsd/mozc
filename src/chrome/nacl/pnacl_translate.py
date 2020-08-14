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

"""A utility tool to run pnacl-translate for all archtectures.

Example usage:
  The following command generates stripped nexefile_arm.nexe and
  nexefile_x86_32.nexe and nexefile_x86_64.nexe.

  python pnacl_translate.py --command=/path/to/toolchain/linux_pnacl \
    --input=/path/to/pexefile --output_base=/path/to/nexefile \
    --configuration=Release
"""

import optparse
import os
import shutil
import subprocess
import sys
import tempfile


def Translate(toolchain_root, input_file, output_base):
  """Translates the input file for three architectures."""
  targets = (('arm', 'arm'), ('x86-32', 'x86_32'), ('x86-64', 'x86_64'))
  translate_command = os.path.join(toolchain_root, 'bin/pnacl-translate')
  for target in targets:
    cmd = (translate_command, '--allow-llvm-bitcode-input', '-arch', target[0],
           input_file, '-o', '%s_%s.nexe' % (output_base, target[1]))
    print('Running: ' + ' '.join(cmd))
    if subprocess.Popen(cmd).wait() != 0:
      print('ERROR: ' + ' '.join(cmd), file=sys.stderr)
      raise RuntimeError('Translate Error')
    print('Done: ' + ' '.join(cmd))


def StripAndTranslate(toolchain_root, input_file, output_base):
  """Strips and translates the input file for three architectures."""
  strip_command = os.path.join(toolchain_root, 'bin/pnacl-strip')
  try:
    temp_dir = tempfile.mkdtemp()
    temp_file_base = os.path.join(temp_dir, 'stripped')
    cmd = (strip_command, input_file, '-o', temp_file_base)
    print('Running: ' + ' '.join(cmd))
    if subprocess.Popen(cmd).wait() != 0:
      print('ERROR: ' + ' '.join(cmd), file=sys.stderr)
      raise RuntimeError('Strip Error')
    print('Done: ' + ' '.join(cmd))
    Translate(toolchain_root, temp_file_base, temp_file_base)
    targets = ('arm', 'x86_32', 'x86_64')
    for target in targets:
      cmd = (strip_command, '%s_%s.nexe' % (temp_file_base, target),
             '-o', '%s_%s.nexe' % (output_base, target))
      print('Running: ' + ' '.join(cmd))
      if subprocess.Popen(cmd).wait() != 0:
        print('ERROR: ' + ' '.join(cmd), file=sys.stderr)
        raise RuntimeError('Strip Error')
      print('Done: ' + ' '.join(cmd))
  finally:
    shutil.rmtree(temp_dir)


def main():
  """Translate pexe file to x86-32 and x86-64 and arm nexe files."""
  parser = optparse.OptionParser(usage='Usage: %prog')
  parser.add_option('--toolchain_root', dest='toolchain_root',
                    help='pnacl toolchain root path')
  parser.add_option('--input', dest='input',
                    help='input pexe file')
  parser.add_option('--output_base', dest='output_base',
                    help='output base path')
  parser.add_option('--configuration', dest='configuration',
                    help='build configuration')
  (options, _) = parser.parse_args()

  if not options.toolchain_root:
    print('Error: toolchain_root is not set.', file=sys.stderr)
    sys.exit(1)

  if not options.input:
    print('Error: input is not set.', file=sys.stderr)
    sys.exit(1)

  if not options.output_base:
    print('Error: output_base is not set.', file=sys.stderr)
    sys.exit(1)

  if options.configuration == 'Release':
    return StripAndTranslate(options.toolchain_root,
                             options.input,
                             options.output_base)
  else:
    return Translate(options.toolchain_root,
                     options.input,
                     options.output_base)


if __name__ == '__main__':
  main()
