"use strict";
function search_packages(base_url) {
    var _a;
    let query = (_a = $("#searchbar").val()) === null || _a === void 0 ? void 0 : _a.toString();
    if (!query)
        return;
    query = encodeURIComponent(query);
    let url = base_url + query;
    console.log(url);
    window.location.href = base_url + query;
}
