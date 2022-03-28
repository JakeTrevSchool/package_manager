function search_packages(base_url: string) {
  let query = $("#searchbar").val()?.toString();
  if (!query) return;
  query = encodeURIComponent(query);
  let url = base_url + query;
  console.log(url);
  window.location.href = base_url + query;
}
