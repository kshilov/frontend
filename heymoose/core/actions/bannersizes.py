from mappers import banner_size_from_xml
from heymoose.core.rest import get, post

resource_path = '/banner-sizes'


def add_banner_size(width, height):
	params_dict = dict(width=width,	height=height)
	id = post(path=resource_path, params_dict=params_dict)
	return int(id)


def get_banner_sizes(**kwargs):
	return map(banner_size_from_xml, get(path=resource_path, params_dict=kwargs))