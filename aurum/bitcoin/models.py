from django.db import models

# Exchange model
class Exchange(models.Model):

	e_id = models.AutoField(primary_key=True)
	code = models.CharField(max_length=20)
	name = models.CharField(max_length=50)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'exchange'

	def __unicode__(self):
		return self.code


# Currency model
class Currency(models.Model):

	c_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=10)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'currency'

	def __unicode__(self):
		return self.name


# Marketdata model
class MarketData(models.Model):
	
	currency = models.ForeignKey(Currency)
	exchange = models.ForeignKey(Exchange)
	highest_price = models.CharField(max_length=20)
	lowest_price = models.CharField(max_length=20)
	average_price = models.CharField(max_length=20)
	timestamp = models.CharField(max_length=20)
	date_time = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'market_data'

	def __unicode__(self):
		return self.average_price
