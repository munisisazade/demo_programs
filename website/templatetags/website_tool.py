from django import template

register = template.Library()


@register.filter
def get_youtube_embed_url(url):
    if url:
        result = 'https://www.youtube.com/embed/' + url[-11:]
        return result
    else:
        return 'https://www.youtube.com/embed/hb04Nh7GxmE'

@register.filter
def get_youtube_video_image(url):
    if url:
        result = 'https://img.youtube.com/vi/' + str(url[-11:]) + '/hqdefault.jpg'
        return result
    else:
        return '/static/content/about.jpg'