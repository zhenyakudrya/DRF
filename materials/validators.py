from rest_framework import serializers

third_party_resources = ['ispring.ru', 'skillbox.ru', 'getcourse.ru']

def validator_third_party_resources(value):
    if set(value.lower().split()) & set(third_party_resources):
        raise serializers.ValidationError('Использованы запрещенные ссылки на сторонние ресурсы')
