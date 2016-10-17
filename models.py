import datetime

from peewee import *

DATABASE = SqliteDatabase('lots.sqlite')

class Lot(Model):
	field_values = CharField(default="Error retrieving")
	reader_Name = CharField(default="Error retrieving")
	created_at = DateTimeField(default= datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Lot], safe=True)
	DATABASE.close()
