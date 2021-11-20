from odoo import models, fields, api

from odoo.exceptions import ValidationError


class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['todo.task', 'mail.thread']

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

    @api.onchange('user_id')
    def _onchange_responsible(self):
        self.team_ids = None
        return {'warning': {'title': "Warning", 'message': "Please choose a new Team", 'type': "notification"}, }

    @api.constrains('name')
    def _check_name_size(self):
        for todo in self:
            if len(todo.name) < 5:
                raise ValidationError('Title must have 5 chars !')

    # def _compute_user_todo_count(self):
    #     for task in self:
    #         task.user_todo_count = task.search_count(
    #             [('user_id', '=', task.user_id.id)])
