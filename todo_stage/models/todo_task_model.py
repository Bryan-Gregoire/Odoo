from odoo import models, fields
from odoo.tools.populate import compute


class TodoTask(models.Model):
    _inherit = ['todo.task']

    tag_ids = fields.Many2many('todo.task.tag', string='Tags')

    effort_estimate = fields.Integer()
    desc = fields.Char('Description')
    state = fields.Selection([('draft', 'draft'), ('open', 'open'), ('done', 'done')], default="draft")
    docs = fields.Html('Documentation')

    date_created = fields.Datetime('Create Date and Time', default=fields.Datetime.now())

    image = fields.Binary('Image')

    user_todo_count = fields.Integer("User To-Do count", compute="_compute_user_todo_count")

    def set_to_open(self):
        self.state = 'open'

    def set_to_closed(self):
        self.state = 'done'

    def set_to_draft(self):
        self.state = 'draft'

    def _compute_user_todo_count(self):
        self.user_todo_count = self.search_count([('user_id', '=', self.user_id.id)])

    # def _compute_user_todo_count(self):
    #     for task in self:
    #         task.user_todo_count = task.search_count(
    #             [('user_id', '=', task.user_id.id)])
