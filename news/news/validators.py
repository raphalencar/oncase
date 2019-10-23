from schematics.models import Model
from schematics.types import URLType, StringType, ListType

class TecmundoItem(Model):
	link = StringType(required=True)
	title = StringType(required=True)
	author = StringType(required=True)
	date = StringType()
	text = StringType(required=True)
	tag = StringType()
	blog = StringType(required=True)

class TecnoblogItem(Model):
	link = StringType(required=True)
	title = StringType(required=True)
	author = StringType(required=True)
	date = StringType()
	text = StringType(required=True)
	tag = StringType()
	blog = StringType(required=True)