# coding: spec

from photons_app.errors import ProgrammerError, BadTask
from photons_app.option_spec.task_objs import Task
from photons_app.task_finder import TaskFinder
from photons_app.test_helpers import TestCase
from photons_app.actions import all_tasks

from noseOfYeti.tokeniser.support import noy_sup_setUp
from input_algorithms import spec_base as sb
import mock

describe TestCase, "TaskFinder":
    before_each:
        self.collector = mock.Mock(name="collector")
        self.task_finder = TaskFinder(self.collector)

    it "takes in a collector":
        task_finder = TaskFinder(self.collector)

        self.assertIs(task_finder.collector, self.collector)
        self.assertIs(task_finder.tasks, all_tasks)

    describe "task_runner":
        before_each:
            self.task = mock.Mock(name="task")
            self.reference = mock.Mock(name="reference")

        describe "after finding tasks":
            before_each:
                self.one_task = mock.Mock(name="one_task")
                self.two_task = mock.Mock(name="two_task")
                self.tasks = {"one": self.one_task, "two": self.two_task}
                self.task_finder.tasks = self.tasks

            it "complains if the task is not in self.tasks":
                assert "three" not in self.task_finder.tasks
                with self.fuzzyAssertRaisesError(BadTask, "Unknown task", task="three", available=["one", "two"]):
                    self.task_finder.task_runner("three", self.reference)

                with self.fuzzyAssertRaisesError(BadTask, "Unknown task", task="three", available=["one", "two"]):
                    self.task_finder.task_runner("target:three", self.reference)

            it "runs the chosen task":
                res = mock.Mock(name="res")
                self.one_task.run.return_value = res

                available_actions = mock.Mock(name='available_actions')

                with mock.patch("photons_app.task_finder.available_actions", available_actions):
                    self.assertIs(self.task_finder.task_runner("one", self.reference), res)

                self.one_task.run.assert_called_once_with(sb.NotSpecified, self.collector, self.reference
                    , available_actions, self.tasks
                    )

            it "runs the chosen task with the specified target":
                res = mock.Mock(name="res")
                self.one_task.run.return_value = res

                available_actions = mock.Mock(name='available_actions')

                with mock.patch("photons_app.task_finder.available_actions", available_actions):
                    self.assertIs(self.task_finder.task_runner("target:one", self.reference), res)

                self.one_task.run.assert_called_once_with("target", self.collector, self.reference
                    , available_actions, self.tasks
                    )

            it "runs the chosen task with the other kwargs":
                one = mock.Mock(name="one")
                res = mock.Mock(name="res")
                self.one_task.run.return_value = res

                available_actions = mock.Mock(name='available_actions')

                with mock.patch("photons_app.task_finder.available_actions", available_actions):
                    self.assertIs(self.task_finder.task_runner("target:one", self.reference, one=one, two=3), res)

                self.one_task.run.assert_called_once_with("target", self.collector, self.reference
                    , available_actions, self.tasks, one=one, two=3
                    )
