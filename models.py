import datetime

from peewee import *

DATABASE = SqliteDatabase('spaces.sqlite')

class Space(Model):
	field_values = CharField()
	created_at = DateTimeField(default= datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Space], safe=True)
	DATABASE.close()
