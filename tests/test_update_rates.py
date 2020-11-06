from unittest import TestCase
from datetime import datetime
from dags.update_rates import dag


# Test functionality for updating the database
class TestUpdateRates(TestCase):

    # Ensure the DAG ID matches the expected value
    def test_id(self):

        dag_id = dag.dag_id
        self.assertEqual(dag_id, "update_rates")

    # Test that default args match the rights values
    def test_default_args(self):

        expected_values = {
            "owner": "airflow",
            "start_date": datetime(2020, 11, 1),
            "retries": 1,
        }
        self.assertEqual(expected_values, dag.default_args)

    # Test that the task names match expected values
    def test_tasks(self):

        task_list = ["extract", "transform", "load"]
        self.assertEqual(dag.task_ids, task_list)

    def test_schedule_interval(self):

        schedule = "0 23 * * 1-5"
        self.assertEqual(dag.schedule_interval, schedule)
