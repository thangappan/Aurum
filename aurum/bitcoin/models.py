from django.db import models

# Exchange model
class Exchange(models.Model):

	exchange_id = models.IntegerField(primary_key=True)
	exchange_code = models.CharField(max_length=20)
	exchange_name = models.CharField(max_length=50)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'exchange'

	def __unicode__(self):
		return self.exchange_code


# Currency model
class Currency(models.Model):

	currency_id = models.IntegerField(primary_key=True)
	currency_name = models.CharField(max_length=10)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'currency'

	def __unicode__(self):
		return self.currency_name


# Marketdata model
class MarketData(models.Model):
	
	currency = models.ForeignKey(Currency)
	exchange = models.ForeignKey(Exchange)
	highest_price = models.CharField(max_length=20)
	lowest_price = models.CharField(max_length=20)
	average_price = models.CharField(max_length=20)
	timestamp = models.CharField(max_length=20)
	datetime = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'market_data'
