# Generated by Django 4.2.7 on 2023-12-10 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_transaction_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='reason',
            field=models.CharField(choices=[('Продажа', 'Продажа'), ('Покупка', 'Покупка'), ('Перевод', 'Перевод'), ('Другое', 'Другое')], max_length=10, verbose_name='Тип транзакции'),
        ),
    ]