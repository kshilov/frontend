from mappers import transaction_from_xml, count_from_xml
from heymoose.core.rest import get
from heymoose.utils.shortcuts import dict_update_filled_params

resource_path = '/account'

def get_account_transactions(account_id, offset=None, limit=None):
	path = '{0}/{1}/transactions'.format(resource_path, account_id)
	params = dict(accountId=account_id)
	dict_update_filled_params(params, offset=offset, limit=limit)
	xml = get(path=path, params_dict=params)
	return map(transaction_from_xml, xml), int(xml.attrib['count'])


def get_account_transactions_count(account_id):
	path = '{0}/{1}/transactions/count'.format(resource_path, account_id)
	params = dict(accountId=account_id)
	return count_from_xml(get(path=path, params_dict=params))