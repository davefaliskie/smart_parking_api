import datetime

from peewee import *

DATABASE = SqliteDatabase('lots.sqlite')

class Lot(Model):
	field_values = CharField()
	reader_Name = CharField()
	created_at = DateTimeField(default= datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Lot], safe=True)
	DATABASE.close()
