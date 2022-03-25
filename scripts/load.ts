//schema:
interface responseScheme {
  version: string;
  status: string;
  download_url: string;
  content: string;
}

function load_version(url: string) {
  fetch(url)
    .then((response) => response.json())
    .then((data: responseScheme) => {
      console.log(data);
      if (data.status === "OK") {
        //handle ok
      } else {
        //handle not ok
      }
    });
}
