#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init, task, depends
from sys import path

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.install_dependencies")


name = "maze_game"
default_task = "run"


@init
def set_properties(project):
    project.build_depends_on("pygame")
    project.set_property('coverage_break_build', False)

@task
# @depends("install_dependencies")
def run(project):
    # pass
    path.append("src/main/python")
    import maze
    maze.main()
