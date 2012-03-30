# -*- coding: utf-8 -*-
from flask import render_template, request, flash, g, redirect, url_for, abort
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.data.models import Offer, OfferGrant, SubOffer
from heymoose.utils.pagination import current_page, page_limits, paginate
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import advertiser_only, affiliate_only


@bp.route('/offers/')
def offers_all():
	page = current_page()
	per_page = app.config.get('OFFERS_PER_PAGE', 10)
	offset, limit = page_limits(page, per_page)
	aff_id_arg = dict(aff_id=g.user.id) if g.user.is_affiliate else dict()
	offers, count = rc.offers.list(offset=offset, limit=limit, approved=True, active=True, **aff_id_arg)
	pages = paginate(page, count, per_page)
	return render_template('cabinetcpa/offers/all.html', offers=offers, pages=pages)

@bp.route('/offers/my')
@advertiser_only
def offers_list():
	page = current_page()
	per_page = app.config.get('OFFERS_PER_PAGE', 10)
	offset, limit = page_limits(page, per_page)
	offers, count = rc.offers.list(offset=offset, limit=limit, advertiser_id=g.user.id)
	pages = paginate(page, count, per_page)
	return render_template('cabinetcpa/offers/list.html', offers=offers, pages=pages)

@bp.route('/offers/requested')
@affiliate_only
def offers_requested():
	page = current_page()
	per_page = app.config.get('OFFERS_PER_PAGE', 10)
	offset, limit = page_limits(page, per_page)
	offers, count = rc.offers.list_requested(g.user.id, offset=offset, limit=limit)
	pages = paginate(page, count, per_page)
	return render_template('cabinetcpa/offers/requested.html', offers=offers, pages=pages)

@bp.route('/offers/new', methods=['GET', 'POST'])
@advertiser_only
def offers_new():
	tmpl = forms.SubOfferForm(prefix='suboffers-0-')
	form = forms.OfferForm(request.form)
	if request.method == 'POST' and form.validate():
		offer = Offer(advertiser=g.user)
		form.populate_obj(offer)
		suboffers = []
		for suboffer_field in form.suboffers:
			suboffer = SubOffer()
			suboffer_field.form.populate_obj(suboffer)
			suboffers.append(suboffer)
		id = rc.offers.add(offer, 100.00)
		for suboffer in suboffers:
			rc.offers.add_suboffer(id, suboffer)
		flash(u'Оффер успешно создан', 'success')
		return redirect(url_for('.offers_info', id=id))
	return render_template('cabinetcpa/offers/new.html', form=form, tmpl=tmpl)

@bp.route('/offers/<int:id>', methods=['GET', 'POST'])
def offers_info(id):
	offer = rc.offers.get_try_requested(id, g.user.id) if g.user.is_affiliate else rc.offers.get_by_id(id)
	form = forms.OfferRequestForm(request.form)
	if g.user.is_affiliate and not offer.grant and request.method == 'POST' and form.validate():
		offer_grant = OfferGrant(offer=offer, affiliate=g.user, message=form.message.data)
		rc.offer_grants.add(offer_grant)
		flash(u'Заявка на сотрудничество успешно отправлена', 'success')
		return redirect(url_for('.offers_requested'))
	return render_template('cabinetcpa/offers/info/info.html', offer=offer, form=form)

@bp.route('/offers/<int:id>/edit')
@advertiser_only
def offers_info_edit(id):
	offer = rc.offers.get_by_id(id)
	return render_template('cabinetcpa/offers/info/edit.html', offer=offer)

@bp.route('/offers/<int:id>/actions', methods=['GET', 'POST'])
def offers_info_actions(id):
	offer = rc.offers.get_by_id(id)
	form = forms.SubOfferForm(request.form)
	if offer.owned_by(g.user) and request.method == 'POST' and form.validate():
		suboffer = SubOffer()
		form.populate_obj(suboffer)
		rc.offers.add_suboffer(id, suboffer)
		flash(u'Действие успешно добавлено', 'success')
		return redirect(request.url)
	return render_template('cabinetcpa/offers/info/actions.html', offer=offer, form=form)

@bp.route('/offers/<int:id>/materials')
def offers_info_materials(id):
	offer = rc.offers.get_by_id(id)
	return render_template('cabinetcpa/offers/info/materials.html', offer=offer)

@bp.route('/offers/<int:id>/requests')
@advertiser_only
def offers_info_requests(id):
	offer = rc.offers.get_by_id(id)
	if not offer.owned_by(g.user): abort(403)
	
	page = current_page()
	per_page = app.config.get('OFFER_REQUESTS_PER_PAGE', 20)
	offset, limit = page_limits(page, per_page)
	grants, count = rc.offer_grants.list(offer_id=offer.id, approved=True, offset=offset, limit=limit, full=False)
	pages = paginate(page, count, per_page)
	
	if request.method == 'POST':
		id = int(request.form.get('id'))
		grant = rc.offer_grants.get_by_id(id)
		if grant.offer.id == offer.id:
			rc.offer_grants.activate(grant.id)
			flash(u'Заявка успешно утверждена', 'success')
			return redirect(request.url)
	return render_template('cabinetcpa/offers/info/requests.html', offer=offer, grants=grants, pages=pages)

@bp.route('/offers/<int:id>/balance')
@advertiser_only
def offers_info_balance(id):
	offer = rc.offers.get_by_id(id)
	return render_template('cabinetcpa/offers/info/balance.html', offer=offer)

@bp.route('/offers/<int:id>/stats')
def offers_info_stats(id):
	offer = rc.offers.get_by_id(id)
	return render_template('cabinetcpa/offers/info/stats.html', offer=offer)

