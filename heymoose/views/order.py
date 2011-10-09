# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.decorators import customer_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
import heymoose.core.actions.orders as orders
from heymoose.views.work import *

def order_form_template(form_params=None):
	order_form = forms.OrderForm()
	if form_params:
		order_form.ordername.data = form_params['ordername']
		order_form.orderbalance.data = form_params['orderbalance']
		order_form.orderbody.data = form_params['orderbody']
		order_form.ordercpa.data = form_params['ordercpa']

	g.params['orderform'] = order_form
	return render_template('order-creation-form.html', params = g.params)

@frontend.route('/create_order', methods=['POST'])
@customer_only
def create_order():
	#TODO проверка данных
	order_form = forms.OrderForm(request.form)
	if request.method == "POST" and order_form.validate():
		file = request.files['orderimage']
		image_data = file.stream.read()
		print "Going to add order"
		orders.add_order(userId=g.user.id,
						title=order_form.ordername.data,
						body=order_form.orderbody.data,
						balance = order_form.orderbalance.data,
						cpa=order_form.ordercpa.data,
		                desc=order_form.orderdesc.data,
						image_data=image_data)
		return redirect(url_for('user_cabinet', username=g.user.nickname))

	print "Form error"
	flash_form_errors(order_form.errors.values(), 'ordererror')
	return order_form_template(request.form)

##TODO: Make it more simple, use AJAX for all forms
#@frontend.route('/order/<order_id>', methods = ['POST', 'GET'])
#@customer_only
#def show_order(order_id=None):
#	if not order_id:
#		return redirect(url_for('user_cabinet', username=g.user.nickname))
#
#	order = g.user.load_order(order_id)
#	order_form = forms.OrderForm()
#	if order:
#		g.params['order'] = order
#		order_form.ordername.data = order.title
#		order_form.orderbalance.data = order.balance
#		order_form.orderbody.data = order.body
#		order_form.ordercpa.data = order.cpa
#	else:
#		return redirect(url_for('user_cabinet', username=g.user.nickname))
#
#	if request.method == "POST":
#		order_form = forms.OrderForm(request.form)
#		if order_form.validate():
#			try:
#				g.user.create_order(userId=g.user.id,
#									title=order_form.ordername.data,
#				                    body=order_form.orderbody.data,
#									balance = order_form.orderbalance.data,
#				                    cpa=order_form.ordercpa.data)
#			except Exception as inst:
#				app_logger.error(inst)
#				app_logger.error(sys.exc_info())
#
#			return redirect(url_for('user_cabinet', username=g.user.nickname))
#		flash_form_errors(order_form.errors.values(), 'ordererror')
#
#	g.params['orderform'] = order_form
#	return render_template('cabinet-questionlist.html', params=g.params)

@frontend.route('/delete_order/<order_id>')
@customer_only
def delete_order(order_id):
	return redirect(url_for('user_cabinet', username=g.user.nickname))

@frontend.route('/order_form', methods=['POST', 'GET'])
@customer_only
def order_form():
	if request.method == 'POST':
		pass
		#file = request.files['questionlist']
		#if file:
			#g.params['questionlist'] = file.stream.read().decode('utf8')
	return order_form_template()

@frontend.route('/approve_order/<order_id>', methods = ['POST', 'GET'])
@admin_only
def approve_order(order_id=None):
	order_id = int(order_id)
	if not order_id:
		return redirect(url_for('user_cabinet', username=g.user.nickname))

	orders.approve_order(order_id)
	return redirect(url_for('admin_cabinet'))


