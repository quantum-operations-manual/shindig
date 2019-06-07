import os
import sys
import json
import subprocess

def get_engine_install(project_name):
    launcher_dat = os.path.join(os.environ['programdata'], 'Epic', 'UnrealEngineLauncher', 'LauncherInstalled.dat')
    if not os.path.exists(launcher_dat):
        print('ERROR: Cannot find launcher installation, please make sure the Epic Games Launcher is installed and you have downloaded UE4.')
        sys.exit(1)

    with open(launcher_dat, 'r') as fobj:
        engine_config = json.load(fobj)

    project_fname = get_fully_qualified_project(project_name)
    with open(project_fname, 'r') as fobj:
        project = json.load(fobj)

    project_version = project['EngineAssociation']
    candidates = filter(lambda a: a['AppVersion'].startswith(project_version), engine_config['InstallationList'])

    try:
        engine = next(candidates)
    except ValueError:
        print('Cannot find the engine version required by this project:', project_version, 'please install it.')
        sys.exit(1)
    print(engine)
    return engine

def get_binaries_dir(install):
    return os.path.join(install['InstallLocation'], 'Engine', 'Binaries')

def get_ue_automation_tool(install):
    return os.path.join(get_binaries_dir(install), '..', 'Build', 'BatchFiles', 'RunUAT.bat')

def get_editor(install):
    return os.path.join(get_binaries_dir(install), 'Win64', 'UE4Editor.exe')

def get_ue_build_tool(install):
    return os.path.join(get_binaries_dir(install), 'DotNET', 'UnrealBuildTool.exe')

def get_fully_qualified_project(project):
    """This assumes that Tools is directly under the project root directory"""
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(project_dir, project + '.uproject')

def get_relative_project(project):
    full = get_fully_qualified_project(project)
    cwd = os.getcwd()
    return os.path.relpath(full, cwd)

def generate_project_files(project_name):
    engine = get_engine_install(project_name)
    ue_build_tool = get_ue_build_tool(engine)
    project_fname = get_fully_qualified_project(project_name)
    cmd = [ue_build_tool, '-projectfiles', '-project=%s' % project_fname, '-game', '-rocket', '-progress']
    build_tool_run = subprocess.Popen(cmd, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with build_tool_run.stdout:
        for line in build_tool_run.stdout:
            print('%s' % line.strip())

def compile_game(project_name, platform, configuration):
    engine = get_engine_install(project_name)
    ue_automation_tool = get_ue_automation_tool(engine)
    project_fname = get_fully_qualified_project(project_name)
    cmd = [ue_automation_tool, 'BuildCookRun', '-project=%s' % project_fname, '-platform=' + platform, '-clientconfig='+configuration, '-serverconfig='+configuration, '-build']
    build_tool_run = subprocess.Popen(cmd, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with build_tool_run.stdout:
        for line in build_tool_run.stdout:
            print('%s' % line.strip())

def start_editor(project_name):
    engine = get_engine_install(project_name)
    editor = get_editor(engine)
    project_fname = get_fully_qualified_project(project_name)
    cmd = [editor, project_fname]
    subprocess.Popen(cmd, universal_newlines=True, shell=True)
