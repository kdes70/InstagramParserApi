def get_post_url(json_object):
    return json_object["data"]["shortcode_media"]["display_url"]

def get_post_location(json_object):
    return json_object["data"]["shortcode_media"]["location"]["name"]

def get_post_author_username(json_object):
    return json_object["data"]["shortcode_media"]["owner"]["username"]

def get_post_author_full_name(json_object):
    return json_object["data"]["shortcode_media"]["owner"]["full_name"]

def get_post_text(json_object):
    return json_object["data"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
