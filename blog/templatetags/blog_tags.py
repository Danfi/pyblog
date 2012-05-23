#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
from django.template import Node,Variable
register = template.Library()

class calculateFloor(Node):
    def __init__(self,num,page,commentsPerPage):
        self.num = num
        self.page = page
        self.commentsPerPage = commentsPerPage

    def render(self, context):
        num = Variable(self.num).resolve(context)
        page = Variable(self.page).resolve(context)
        commentsPerPage = Variable(self.commentsPerPage).resolve(context)

        return num+(page-1)*commentsPerPage

@register.tag(name="calculate_floor")
def calculate_floor(parser, token):
    bits = token.contents.split()
    return calculateFloor(bits[1],bits[2],bits[3])