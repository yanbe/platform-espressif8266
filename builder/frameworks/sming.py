# Copyright 2014-present Ivan Kravets <me@ikravets.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Sming

Open Source framework for high efficiency WiFi SoC ESP8266 native
development with C++ language.

https://github.com/SmingHub/Sming
"""

from os import listdir
from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.DevPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-sming")
FRAMEWORK_VERSION = platform.get_package_version("framework-sming")
assert isdir(FRAMEWORK_DIR)

env.Append(
    CPPDEFINES=["ARDUINO=%s" % FRAMEWORK_VERSION.split(".")[1]],

    LIBPATH=[
        join(FRAMEWORK_DIR, "sdk", "lib"),
        join(FRAMEWORK_DIR, "compiler", "lib"),
        join(FRAMEWORK_DIR, "compiler", "ld")

    ],

    LIBS=["microc", "microgcc", "phy", "pp", "net80211", "lwip",
          "hal", "wpa", "main", "crypto", "pwm", "smartconfig"],

    CPPPATH=[
        join(FRAMEWORK_DIR, "rboot"),
        join(FRAMEWORK_DIR, "include"),
        join(FRAMEWORK_DIR, "sdk", "include"),
        join(FRAMEWORK_DIR, "system", "include"),
        join("$BUILD_DIR"),
        join("$BUILD_DIR", "Wiring"),
        join("$BUILD_DIR", "SmingCore"),
        join("$BUILD_DIR", "SmingCore", "Platform"),
        join("$BUILD_DIR", "FrameworkSming", "rbootAppcode"),
        join("$BUILD_DIR", "FrameworkSmingRboot"),
        join("$BUILD_DIR", "FrameworkSmingRbootAppCode")
    ],

    CCFLAGS=[
        "-Wpointer-arith",
        "-Wundef",
        "-Werror",
        "-Wl,-EL",
        "-finline-functions"
    ],

    CXXFLAGS=[
        "-Wpointer-arith",
        "-Wl,-EL",
        "-nostdlib"
    ]
)

env.Replace(
    LDSCRIPT_PATH="eagle.app.v6.cpp.ld"
)


libs = []

service_dir = join(FRAMEWORK_DIR, "Services")
for d in listdir(service_dir):
    if isdir(join(service_dir, d)):
        env.Append(
            CPPPATH=[join("$BUILD_DIR", "FrameworkSmingServices", d)]
        )

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkSmingRbootAppCode"),
    join(FRAMEWORK_DIR, "rboot", "appcode")
))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "Wiring"),
    join(FRAMEWORK_DIR, "Wiring")
))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "SmingCore"),
    join(FRAMEWORK_DIR, "SmingCore")
))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkSmingSystem"),
    join(FRAMEWORK_DIR, "system")
))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkSmingServices"),
    join(FRAMEWORK_DIR, "Services")
))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkSmingAppInit"),
    join(FRAMEWORK_DIR, "appinit")
))


env.Prepend(LIBS=libs)
