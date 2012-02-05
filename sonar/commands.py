# Here you can create play commands that are specific to the module, and extend existing commands

import play.commands.precompile
from play.utils import *

MODULE = 'sonar'

# Commands that are specific to your module

COMMANDS = ['sonar']

def execute(**kargs):
    command = kargs.get("command")
    app = kargs.get("app")
    args = kargs.get("args")
    env = kargs.get("env")

# This will be executed before any command (new, run...)
def before(**kargs):
    command = kargs.get("command")
    app = kargs.get("app")
    args = kargs.get("args")
    env = kargs.get("env")
    if command == "sonar":
        play.commands.precompile.execute(command=command, app=app, args=args, env=env)
        configFileContents="""# Generated file, do NOT edit it or add it to your revision control system
# Required metadata
sonar.projectKey={sonarProjectKey}
sonar.projectName={sonarProjectName}
sonar.projectVersion={sonarProjectVersion}

# Comma-separated paths to directories with sources (required)
sources=app,test

# Comma-separated paths to directories with binaries (optional), in case of Java - directories with class files
binaries=precompiled/java/

# Comma-separated paths to files with third-party libraries (optional), in case of Java - JAR files
libraries={playPath}/framework/*.jar,{playPath}/framework/lib/*.jar
"""
### TODO add lib/*.jar to libraries if not empty
        configFileContents = configFileContents.format(sonarProjectKey = app.readConf('sonar.projectKey'), sonarProjectName = app.readConf('sonar.projectName'), sonarProjectVersion = app.readConf('sonar.projectVersion'), playPath = app.play_env['basedir'])
        sonarConfigFileHandle = open(app.path + "/sonar-project.properties", "w")
        sonarConfigFileHandle.write(configFileContents)
        sonarConfigFileHandle.close

# This will be executed after any command (new, run...)
def after(**kargs):
    command = kargs.get("command")
    app = kargs.get("app")
    args = kargs.get("args")
    env = kargs.get("env")

    if command == "new":
        pass
