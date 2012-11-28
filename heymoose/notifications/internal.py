from heymoose import app, signals
from base import notify_user, notify_users
import templates


@signals.offer_blocked.connect
def offer_blocked(app, affiliates, notify_affiliates=False, **kwargs):
	notify_users(affiliates, templates.OFFER_BLOCKED, notified=notify_affiliates, **kwargs)
	notify_user(kwargs['offer'].advertiser, templates.OFFER_BLOCKED, **kwargs)


@signals.offer_unblocked.connect
def offer_unblocked(app, affiliates, notify_affiliates=False, **kwargs):
	notify_users(affiliates, templates.OFFER_UNBLOCKED, notified=notify_affiliates, **kwargs)
	notify_user(kwargs['offer'].advertiser, templates.OFFER_UNBLOCKED, **kwargs)

@signals.site_moderated.connect
def site_moderated(app, site, **kwargs):
	notify_user(site.affiliate, templates.SITE_MODERATED, site=site)
