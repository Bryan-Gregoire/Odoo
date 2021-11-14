from odoo import models, fields, api, exceptions

import logging

_logger = logging.getLogger(__name__)


class TodoTask(models.Model):
    _name = 'todo.task'
    # _description = ''

    _logger.info('----> Bryan TodoTask init %s', __name__)
    name = fields.Char("name", required=True)
    is_done = fields.Boolean('is done')
    active = fields.Boolean("active", default=True)
    data_deadline = fields.Date("date deadline")

    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user)
    team_ids = fields.Many2many('res.partner', string="Team")

    def do_clear_done(self):
        for task in self:
            if task.active:
                _logger.info("Bryan TodoTask do_clear_done set active to false")
                task.active = False
            else:
                raise exceptions.Warning("Task already not active")

    def write(self, values):
        if 'active' not in values:
            _logger.info("Bryan TodoTask write set active to true")
            values['active'] = True
        return super(TodoTask, self).write(values)

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(TodoTask, self).copy(default)

    def __str__(self):
        return f"Task(id={self.id}, name={self.name}, is_done={self.is_done}, active={self.active}," \
               f" data_deadline={self.data_deadline}, user_name={self.user_id.name}, team_count={len(self.team_ids)})"
