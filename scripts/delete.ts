function delete_package(target: string) {
  let del = confirm(
    "Are you sure you want to delete this package? This action cannot be reversed"
  );
  if (del) window.location.href = target;
}
