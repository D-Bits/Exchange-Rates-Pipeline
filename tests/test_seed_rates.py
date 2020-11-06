from unittest import TestCase
from datetime import datetime
from dags.seed_rates import dag


class TestSeedRates(TestCase):

    # Ensure the DAG ID matches the expected value
    def test_id(self):

        dag_id = dag.dag_id
        self.assertEqual(dag_id, "seed_rates")

    # Test that the task names match expected values
    def test_tasks(self):

        task_list = ["extract", "transform", "load"]
        self.assertEqual(dag.task_ids, task_list)

    def test_schedule_interval(self):

        self.assertEqual(dag.schedule_interval, None)
