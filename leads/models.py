from django.db import models


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_PROGRESS = 'in_progress', 'В работе'
        DONE = 'done', 'Закрыта'

    class Source(models.TextChoices):
        WEBSITE = 'website', 'Сайт'
        TELEGRAM = 'telegram', 'Telegram'
        WHATSAPP = 'whatsapp', 'WhatsApp'
        CALL = 'call', 'Звонок'
        OTHER = 'other', 'Другое'

    full_name = models.CharField('Имя клиента', max_length=120)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email', blank=True)
    company = models.CharField('Компания', max_length=120, blank=True)
    source = models.CharField('Источник', max_length=20, choices=Source.choices, default=Source.WEBSITE)
    budget = models.PositiveIntegerField('Бюджет', null=True, blank=True)
    status = models.CharField('Статус', max_length=20, choices=Status.choices, default=Status.NEW)
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self) -> str:
        return f'{self.full_name} — {self.get_status_display()}'
