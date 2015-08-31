#!/usr/bin/env python

# Copyright 2015 Samsung Electronics Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#  This file converts src/js/iotjs.js to a C-array in include/iotjs_js.h file

import sys
import glob
import os

def extractName(path):
    return os.path.splitext(os.path.basename(path))[0]

def writeLine(fo, content, indent=0):
    buf = '  ' * indent
    buf += content
    buf += '\n'
    fo.write(buf)

def regroup(l, n):
    return [ l[i:i+n] for i in range(0, len(l), n) ]

LICENSE = '''/* Copyright 2015 Samsung Electronics Co., Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the \"License\");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an \"AS IS\" BASIS
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * This file is generated by tools/js2c.py
 * Do not modify this.
 */
'''

HEADER = '''#ifndef IOTJS_JS_H
#define IOTJS_JS_H
namespace iotjs {
'''
FOOTER = '''}
#endif
'''

SRC_PATH = '../src/'
JS_PATH = SRC_PATH + 'js/'

fout = open(SRC_PATH + 'iotjs_js.h', 'w')

fout.write(LICENSE);
fout.write(HEADER);

files = glob.glob(JS_PATH + '*.js')
for path in files:
    name = extractName(path)
    fout.write('const char ' + name + '_n [] = "' + name + '";\n')
    fout.write('const char ' + name + '_s [] = {\n')

    code = open(path, 'r').read() + '\0'
    for line in regroup(code, 10):
        buf = ', '.join(map(lambda ch: str(ord(ch)), line))
        if line[-1] != '\0':
            buf += ','
        writeLine(fout, buf, 1)
    writeLine(fout, '};')
    writeLine(fout, 'const int ' + name + '_l = ' + str(len(code)-1) + ';')

NATIVE_STRUCT = '''
struct native_mod {
  const char* name;
  const char* source;
  const int length;
};

__attribute__ ((used)) static struct native_mod natives[] = {
'''
fout.write(NATIVE_STRUCT)
filenames = map(extractName, files)
for name in filenames:
    writeLine(fout, '{ ' + name + '_n, ' + name + '_s, ' + name + '_l },', 1)
writeLine(fout, '{ NULL, NULL, 0 }', 1)
writeLine(fout, '};')

fout.write(FOOTER)