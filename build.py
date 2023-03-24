#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init, task

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


name = "maze_game"
default_task = "run"


@init
def set_properties(project):
    project.build_depends_on("pygame")
    project.set_property('coverage_break_build', False)

@task
def run(project):
    pass
    # path.append("src/main/python")
    # from test_pack import test_app
    # test_app.main()
