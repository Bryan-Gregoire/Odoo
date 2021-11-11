from odoo import models, fields


class TodoTask(models.Model):
    _name = 'todo.task'
    #_description = ''

    name = fields.Char("name", required=True)
    is_done = fields.Boolean('is done')
    active = fields.Boolean("active", default=True)
    data_deadline = fields.Date("date deadline")

    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user)
    team_ids = fields.Many2many('res.partner', string="Team")
