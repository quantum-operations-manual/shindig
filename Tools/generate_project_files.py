from __future__ import print_function
import os
import sys
import json
import subprocess

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

launcher_dat = os.path.join(os.environ['programdata'], 'Epic', 'UnrealEngineLauncher', 'LauncherInstalled.dat')
if not os.path.exists(launcher_dat):
    print('ERROR: Cannot find launcher installation, please make sure the Epic Games Launcher is installed and you have downloaded UE4.')
    sys.exit(1)

with open(launcher_dat, 'r') as fobj:
    engine_config = json.load(fobj)

project_fname = os.path.join(project_dir, 'Shindig.uproject')
with open(project_fname, 'r') as fobj:
    project = json.load(fobj)

project_version = project['EngineAssociation']
found_engine = False
for engine in engine_config['InstallationList']:
    if engine['AppVersion'].startswith(project_version):
        found_engine = True
        break

if not found_engine:
    print('Cannot find the engine version required by this project:', project_version, 'please install it.')
    sys.exit(1)
ue_build_tool = os.path.join(engine['InstallLocation'], 'Engine', 'Binaries', 'DotNET', 'UnrealBuildTool.exe')
cmd = [ue_build_tool, '-projectfiles', '-project=%s' % project_fname, '-game', '-rocket', '-progress']
build_tool_run = subprocess.Popen(cmd, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
with build_tool_run.stdout:
    for line in build_tool_run.stdout:
        print('%s', line.strip())