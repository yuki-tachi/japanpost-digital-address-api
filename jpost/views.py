from django.shortcuts import render

from jpost.common.japanpost_token_client import JapanPostTokenClient
from jpost.common.japanpost_api_manager import JapanPostApiManager


def search_view(request):
    context = {}
    # クエリパラメータからzipcodeを取得（例: /searchcode?zipcode=1000001）
    search_code = request.GET.get("search_code", "")

    print(f"search_code: {search_code}")

    if not search_code:
        context = {"searched_code": "", "status_code": None}
    else:
        searched_code, status_code = JapanPostApiManager.instance().searchcode(
            search_code
        )
        context = {"searched_code": searched_code, "status_code": status_code}

    return render(request, "jpost/searchcode.html", context)


def address_form_view(request):

    context = {}
    token = JapanPostTokenClient.get_token()

    if request.method == "POST":
        postal_code = request.POST.get("postal_code", "")

        prefecture = request.POST.get("prefecture", "")
        context = {"postal_code": postal_code, "prefecture": prefecture, "token": token}
        return render(request, "jpost/address_form_result.html", context)

    context = {"token": token}

    # addresses = JapanPostApiManager.instance().searchcode("120002")

    return render(request, "jpost/address_form.html", context)
