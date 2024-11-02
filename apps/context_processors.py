from root.settings import languages_dict


def languages(request):
    return {
        'languages': languages_dict
    }
