from django.db import models

from authentication.models import CustomUser


class Tag(models.Model):
    title = models.CharField(max_length=17, verbose_name="Тег")

    def __str__(self):
        return str(self.title)


class Developer(models.Model):
    tags = models.ManyToManyField(Tag, verbose_name="Тег разработчика")
    img = models.ImageField(blank=True, null=True, upload_to='developers', verbose_name="Фото разработчика")
    title = models.CharField(max_length=31, verbose_name="Разработчик")
    description = models.CharField(max_length=127, null=True, blank=True, verbose_name="Описание разработчика")

    def __str__(self):
        return str(self.title)


class Token(models.Model):
    tags = models.ManyToManyField(Tag, verbose_name="Тег проекта")
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, verbose_name="Тег разработчика проекта")
    img = models.ImageField(upload_to='tokens', verbose_name="Фото проекта")
    title = models.CharField(max_length=31, verbose_name="Проект")
    ticker = models.CharField(max_length=7, verbose_name="Тикер")
    description = models.CharField(max_length=127, null=True, blank=True, verbose_name="Описание проекта")

    def __str__(self):
        return str(self.title)


class Transaction(models.Model):

    REASONS = {
        ("Продажа", "Продажа"),
        ("Покупка", "Покупка"),
    }

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор транзакции")
    token = models.ForeignKey(Token, on_delete=models.CASCADE, verbose_name="Токен транзакции")
    reason = models.CharField(choices=REASONS, max_length=10, verbose_name="Тип транзакции")
    qnt = models.FloatField(verbose_name="Количество")
    price = models.FloatField(verbose_name="Цена")
    date = models.DateField(verbose_name="Дата")

    def __str__(self):
        return str(self.id)


class SavedToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор избранного по проектам")
    tokens = models.ManyToManyField(Token, verbose_name="Проекты")

    def __str__(self):
        return str(self.id)


class SavedDeveloper(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор избранного по разработчикам")
    developers = models.ManyToManyField(Developer, verbose_name="Разработчики")

    def __str__(self):
        return str(self.id)
