from django.core.exceptions import ValidationError


def validate_cpf(value):
    str_num = str(value)
    str_num = str_num.replace('.', '')
    str_num = str_num.replace('-', '')
    tam = len(str_num)

    if tam != 11:
        raise ValidationError('CPF deve ter 11 números. Pode ter ponto e hífen.', 'length')

    for i in range(1, 10):
        if str_num.count(str(i)) == 11:
            raise ValidationError('Fail: only repeated numbers', 'rep_num')

    str_primeiro_digito = str_num[:-2]
    primeiro_digito = str_num[-2]

    str_segundo_digito = str_num[:-1]
    segundo_digito = str_num[-1]

    try:
        validar_soma_digito(primeiro_digito, 10, str_primeiro_digito)
        validar_soma_digito(segundo_digito, 11, str_segundo_digito)
    except ValueError as e:
        raise ValidationError('CPF deve ter números. Pode ter ponto e hífen.', 'digits')


def validar_soma_digito(x_digito, x_start, num):
    start = x_start
    total = 0
    for i in num:
        total += start * int(i)
        start -= 1

    result = (total * 10) % 11
    if result == 10:
        result = 0

    if result == int(x_digito):
        return True

    raise ValidationError('CPF inválido', 'invalid')
