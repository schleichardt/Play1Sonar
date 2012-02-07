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
        
        values = dict()
        values['sonarProjectKey'] = app.readConf('application.groupId') + ':' + app.readConf('application.name')
        values['sonarProjectName']  = app.readConf('application.name')
        values['sonarGroupId']  = app.readConf('application.groupId')
        values['sonarProjectVersion']  = app.readConf('application.version')
        values['playPath']  = app.play_env['basedir']
        values['javaVersion']  = app.readConf('java.source')
        if values['javaVersion'] == "":
          values['javaVersion'] = "1.6"
        values['sonarHostUrl'] = app.readConf('sonar.host.url')
        if values['sonarHostUrl'] == "":
          values['sonarHostUrl'] = "http://localhost:9000"
        appHasLibs = len(glob.glob('lib/*.jar')) > 0
        values['appLibsPath'] = ""
        if appHasLibs:
          values['appLibsPath'] = app.path + '/lib/*.jar' + ',' 
        
        #config for Java runner
        propertiesConfigFileContents="""# Generated file, do NOT edit it or add it to your revision control system
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
        propertiesConfigFileContents = propertiesConfigFileContents.format(sonarProjectKey = values['sonarProjectKey'], sonarProjectName = values['sonarProjectName'], sonarProjectVersion = values['sonarProjectVersion'], playPath = values['playPath'], appLibsPath = values['appLibsPath'])
        sonarConfigFileHandle = open(app.path + "/sonar-project.properties", "w")
        sonarConfigFileHandle.write(propertiesConfigFileContents)
        sonarConfigFileHandle.close
        propertiesConfigFileContents = ""
        
        # write config for maven runner
        pomFileContents = """<project xmlns="http://maven.apache.org/POM/4.0.0"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>{sonarGroupId}</groupId>
  <artifactId>{sonarProjectName}</artifactId>
  <name>{sonarProjectName}</name>
  <version>{sonarProjectVersion}</version>
  <build>
        <sourceDirectory>app</sourceDirectory>
        <outputDirectory>precompiled/java/</outputDirectory>
        <plugins>
           <plugin>
              <groupId>org.apache.maven.plugins</groupId>
              <artifactId>maven-compiler-plugin</artifactId>
              <configuration>
                  <source>{javaVersion}</source>
                  <target>{javaVersion}</target>
                  <excludes>
                      <exclude>**/*.*</exclude>
                  </excludes>
              </configuration>
           </plugin>
        </plugins>
  </build>
  <properties>
    <sonar.dynamicAnalysis>reuseReports</sonar.dynamicAnalysis>
    <sonar.host.url>{sonarHostUrl}</sonar.host.url>
    <sonar.surefire.reportsPath>test-result</sonar.surefire.reportsPath>
    <sonar.tests>test</sonar.tests>
    <sonar.cobertura.reportPath>test-result/code-coverage/coverage.xml</sonar.cobertura.reportPath>
  </properties>
</project>"""
        pomFileContents = pomFileContents.format(sonarProjectKey = values['sonarProjectKey'], sonarGroupId = values['sonarGroupId'], sonarProjectName = values['sonarProjectName'], sonarProjectVersion = values['sonarProjectVersion'], playPath = values['playPath'], appLibsPath = values['appLibsPath'], javaVersion = values['javaVersion'], sonarHostUrl = values['sonarHostUrl'])
        pomFileHandle = open(app.path + "/pom.xml", "w")
        pomFileHandle.write(pomFileContents)
        pomFileHandle.close
        pomFileContents = ""

# This will be executed after any command (new, run...)
def after(**kargs):
    command = kargs.get("command")
    app = kargs.get("app")
    args = kargs.get("args")
    env = kargs.get("env")

    if command == "new":
        pass
    