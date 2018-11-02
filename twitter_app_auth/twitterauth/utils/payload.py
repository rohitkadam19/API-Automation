# Payload helper file to return header details


def get_oauth_headers(base64_key,
                      content_type="application/x-www-form-urlencoded;charset=UTF-8",
                      accept_encoding="application/gzip"):

    return {
        "Authorization": "Basic " + base64_key,
        "Content-Type": content_type,
        "Accept-Encoding": accept_encoding
    }


def get_oauth_data(grant_type="client_credentials"):
    return {"grant_type": grant_type}
