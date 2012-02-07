# Here you can create play commands that are specific to the module, and extend existing commands

import play.commands.deps
import play.commands.precompile
from play.utils import *
import glob

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
        play.commands.deps.execute(command='dependencies', app=app, args=args, env=env)
        play.commands.precompile.execute(command=command, app=app, args=args, env=env)
        #auto-test not callable
        configFileContents="""# Generated file, do NOT edit it or add it to your revision control system
# http://docs.codehaus.org/display/SONAR/Advanced+parameters        
        
# Required metadata
sonar.projectKey={sonarProjectKey}
sonar.projectName={sonarProjectName}
sonar.projectVersion={sonarProjectVersion}

# Comma-separated paths to directories with sources (required)
sources=app

# Comma-separated paths to directories with binaries (optional), in case of Java - directories with class files
binaries=precompiled/java/

# Comma-separated paths to files with third-party libraries (optional), in case of Java - JAR files
libraries={appLibsPath}{playPath}/framework/*.jar,{playPath}/framework/lib/*.jar

sonar.dynamicAnalysis=reuseReports
sonar.tests=test
sonar.surefire.reportsPath=test-result
#cobertura does not need to be used, missing cobertura does not interfer with analysis
sonar.cobertura.reportPath=test-result/code-coverage/coverage.xml
"""
### TODO call play auto-test
        appHasLibs = len(glob.glob('lib/*.jar')) > 0
#        if appHasLibs:
        appLibsPathValue = ""
        if appHasLibs:
          appLibsPathValue = app.path + '/lib/*.jar' + ',' 
        configFileContents = configFileContents.format(sonarProjectKey = app.readConf('sonar.projectKey'), sonarProjectName = app.readConf('sonar.projectName'), sonarProjectVersion = app.readConf('sonar.projectVersion'), playPath = app.play_env['basedir'], appLibsPath = appLibsPathValue)
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
    