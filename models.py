import datetime

from peewee import *

DATABASE = SqliteDatabase('lots.sqlite')

class Lot(Model):
	reader_Name = CharField()
	field_values = CharField()
	created_at = DateTimeField(default= datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Lot], safe=True)
	DATABASE.close()
