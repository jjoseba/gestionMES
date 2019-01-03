# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import gettext as _
from django.db import models

from core.models import User
from mes import settings


class Process(models.Model):

    title = models.CharField(null=True, blank=True, verbose_name=_('Título'), max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    member_type = models.CharField(null=True, blank=True,max_length=30, choices=settings.MEMBER_TYPES, verbose_name=_('Tipo de socia'))

    class Meta:
        verbose_name = _('Proceso')
        verbose_name_plural = _('Procesos')
        permissions = (
            ("mespermission_can_manage_processes", _("Puede gestionar los procesos")),
        )

    def __str__(self):
        return "{}".format(self.title).encode('utf-8')


class ProcessStep(models.Model):

    process = models.ForeignKey(Process, null=False, on_delete=models.CASCADE, verbose_name=_('Proceso'), related_name='steps')
    order = models.IntegerField(default=0, verbose_name=('Orden'))
    title = models.CharField(null=True, blank=True, verbose_name=_('Título'), max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name=_('Descripción'))
    fa_icon = models.CharField(null=True, blank=True, verbose_name=_('Icono del paso'), max_length=50)
    color = models.CharField(max_length=20, blank=True, default="#FFFFFF")

    class Meta:
        verbose_name = _('Paso de un proceso')
        verbose_name_plural = _('Pasos de un proceso')
        ordering = ['order']

    def __str__(self):
        return "{} - {}".format(self.process.title, self.title).encode('utf-8')


class ProcessStepTask(models.Model):
    process_step = models.ForeignKey(ProcessStep, null=False, on_delete=models.CASCADE, verbose_name=_('Tarea de un proceso'),
                                related_name='checklist')
    description = models.TextField(null=True, blank=True, verbose_name=_('Descripción'))

    class Meta:
        verbose_name = _('Tarea de un proceso')
        verbose_name_plural = _('Tareas de un proceso')


# Class to define the current process established for each of the bussiness processes defined
class CurrentProcess(models.Model):

    shortname = models.CharField(primary_key=True, unique=True, verbose_name=_('Nombre corto'), max_length=50)
    title = models.CharField(null=True, blank=True, verbose_name=_('Título'), max_length=250)
    process = models.ForeignKey(Process, null=True, verbose_name=_('Proceso asociado'))

    class Meta:
        verbose_name = _('Proceso asignado')
        verbose_name_plural = _('Procesos asignados')
        permissions = (
            ("mespermission_can_manage_current_process", _("Puede gestionar los procesos asociados a cada tarea")),
        )

# Class to define the concrete step inside a process
class CurrentProcessStep(models.Model):
    process = models.ForeignKey(Process, verbose_name=_('Proceso asociado'))
    shortname = models.CharField(primary_key=True, unique=True, verbose_name=_('Nombre corto'), max_length=50)

    class Meta:
        verbose_name = _('Paso asignado del proceso')
        verbose_name_plural = _('Paso asignado del proceso')


class ProcessWorkflow(models.Model):
    process = models.ForeignKey(Process, verbose_name=_('Proceso que sigue'))
    start_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de inicio'))
    current_state = models.ForeignKey(ProcessStep, verbose_name=_('Paso actual'))
    completed = models.BooleanField(default=False, verbose_name=_('Completado'))

    class Meta:
        verbose_name = _('Workflow de Proceso')
        verbose_name_plural = _('Workflows de proceso')

    def add_comment(self, user, comment):

        event = ProcessWorkflowEvent()
        event.workflow = self
        event.step = None
        event.completed_by = user
        event.comment = comment
        event.save()

    def complete_current_step(self, user):
        order = self.current_state.order if self.current_state != None else 0
        next_step = ProcessStep.objects.filter(process=self.process, order__gt=order, order_by=order).first()

        event = ProcessWorkflowEvent()
        event.workflow = self
        event.step = self.current_state
        event.completed_by = user
        event.save()

        if next_step is None:
            # We are in the last step!
            self.current_state = None
            self.completed = True
            self.save()
        else:
            self.current_state = next_step
            self.save()



class ProcessWorkflowEvent(models.Model):
    workflow = models.ForeignKey(ProcessWorkflow, verbose_name=_('Evento de un proceso'), related_name='history_events')
    step = models.ForeignKey(ProcessStep, null=True, verbose_name=_('Paso del proceso'))
    completed_by = models.ForeignKey(User, verbose_name=_('Usuario'))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha'))
    comment = models.TextField(blank=True, null=True, verbose_name=_('Comentario'))

    class Meta:
        verbose_name = _('Evento de Proceso')
        verbose_name_plural = _('Eventos de proceso')


class ProcessWorkflowTask(models.Model):
    workflow = models.ForeignKey(ProcessWorkflow, verbose_name=_('Evento de un proceso'), related_name='completed_checklist')
    task = models.ForeignKey(ProcessStepTask, null=True, verbose_name=_('Tarea completada'))
    completed_by = models.ForeignKey(User, verbose_name=_('Usuario'))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha'))

    class Meta:
        verbose_name = _('Tarea completadas del proceso')
        verbose_name_plural = _('Tareas completadas del proceso')

