import unittest

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, AccessError


class TestTodo(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestTodo, self).setUp(*args,**kwargs)
        # Création d'un nouvel utilisateur pour les tests
        self.fresh_user = self.env['res.users'].create({
            'login': 'bob',
            'name': 'Bob Bobman',
        })
        # Recherche de l'utilisateur avec les droits suffisants sur le module
        self.task_manager = self.env.ref('todo_app.task_manager')

    def test__create(self):
        "Create a simple Todo"
        Todo = self.env['todo.task'].with_user(self.task_manager)
        task = Todo.create({'name': 'Test Task'})
        self.assertEqual(task.name, 'Test Task')
        self.assertEqual(task.is_done, False)
        self.assertEqual(task.active, True)
        self.assertEqual(task.data_deadline, False)
        self.assertEqual(len(task.team_ids), 0)

    def test__create_default_value(self):
        "Create a simple TOdo with default values"
        Todo = self.env['todo.task'].with_user(self.task_manager)
        task = Todo.create({'name': 'Test Task 2'})
        self.assertEqual(task.active, True)

    def test_clear_done(self):
        "Clear Done sets to non active"
        Todo = self.env['todo.task'].with_user(self.task_manager)
        task = Todo.create({'name': 'Test Task 3'})
        task.do_clear_done()
        self.assertFalse(task.active, True)

    def test_clear_done_exception(self):
        "CLear done exception"
        Todo = self.env['todo.task'].with_user(self.task_manager)
        task = Todo.create({'name': 'Test Task 4'})
        task.do_clear_done()
        with self.assertRaises(UserError):
            task.do_clear_done()

    def test_copy_once(self):
        "COpy a simple Todo"
        Todo = self.env['todo.task'].with_user(self.task_manager)
        task = Todo.create({'name': 'Test Task 5'})
        copy = task.copy()
        self.assertEqual(copy.name, 'Copy of Test Task 5')

    def test_copy_twice(self):
        "COpy a simple Todo"
        Todo = self.env['todo.task'].with_user(self.task_manager)
        task = Todo.create({'name': 'Test Task 6'})
        first_copy = task.copy()
        second_copy = task.copy()
        self.assertEqual(first_copy.name, 'Copy of Test Task 6')
        self.assertEqual(second_copy.name, 'Copy of Test Task 6 (1)')

    def test_record_rule(self):
        "Test for a user not in the group"
        Todo = self.env['todo.task'].with_user(self.fresh_user)
        with self.assertRaises(AccessError):
            task = Todo.create({'name': 'New Task'})



















