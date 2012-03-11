from base import models, types
from base.fields import Field, FieldList

class IdentifiableModel(models.ModelBase):
	id = Field(types.Integer, '@id', readonly=True)

class Account(IdentifiableModel):
	balance = Field(types.Integer, 'balance')
	
class Order(IdentifiableModel):
	title = Field(types.String, 'title', default=u'UNKNOWN')

class User(IdentifiableModel):
	email = Field(types.String, 'email')
	roles = FieldList(types.String, 'roles/role')
	account = Field(Account, 'account', default=0)
	orders = FieldList(Order, 'orders/order')
