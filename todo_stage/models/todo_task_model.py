from odoo import models, fields


class TodoTask(models.Model):
    _inherit = ['todo.task']

    tag_ids = fields.Many2many('todo.task.tag', string='Tags')

    effort_estimate = fields.Integer()
    desc = fields.Char('Description')
    state = fields.Selection([('draft', 'draft'), ('open', 'open'), ('done', 'done')], default="draft")
    docs = fields.Html('Documentation')

    date_created = fields.Datetime('Create Date and Time', default=fields.Datetime.now())

    image = fields.Binary('Image')
