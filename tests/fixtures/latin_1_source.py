#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-


class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def fullname(self):
        return "%s %s" % (self.first_name, self.last_name)

    def not_called(self):
        print("Shouldn't be called")

person = Person("Ælfric", "McFly")
person.fullname()
