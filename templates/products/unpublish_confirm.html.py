{ % extends
'base.html' %}

{ % block
title %}Снятие
с
публикации
{ % endblock %}

{ % block
content %}
< div


class ="container mt-4" >

< div


class ="row justify-content-center" >

< div


class ="col-md-6" >

< div


class ="card shadow" >

< div


class ="card-header bg-warning" >

< h2


class ="mb-0" >

< i


class ="fas fa-eye-slash" > < / i > Снять с публикации

< / h2 >
< / div >
< div


class ="card-body" >

< p


class ="lead" >


Вы
уверены, что
хотите
снять
с
публикации
продукт
< strong > "{{ product.name }}" < / strong >?
< / p >
< p


class ="text-warning" >

< i


class ="fas fa-info-circle" > < / i >


Продукт
станет
недоступен
для
просмотра
пользователями.
< / p >

< form
method = "post" >
{ % csrf_token %}
< div


class ="d-flex gap-2" >

< button
type = "submit"


class ="btn btn-warning" >

< i


class ="fas fa-eye-slash" > < / i > Снять с публикации

< / button >
< a
href = "{% url 'products:product_list' %}"


class ="btn btn-secondary" >

< i


class ="fas fa-times" > < / i > Отмена

< / a >
< / div >
< / form >
< / div >
< / div >
< / div >
< / div >
< / div >
{ % endblock %}