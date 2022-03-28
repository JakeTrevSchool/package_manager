//schema:
interface responseScheme {
  version: string;
  status: string;
  download_url: string;
  content: string;
}

function load_version(select: HTMLSelectElement, base_url: string) {
  console.log("loading version: " + select.value);
  let version_ID = select.value;
  let url = base_url + version_ID;
  fetch(url)
    .then((response) => response.json())
    .then((data: responseScheme) => {
      let code_div = $("#code");
      let download_button = $("#download_version");

      let code_block;

      if (data.status === "OK") {
        code_block = "<pre><code>" + data.content + "</pre></code>";
        download_button.attr("href", data.download_url);
        download_button.click(update_downloads);
      } else {
        // this block should never run
        // but im not taking any chances
        code_block = data.content;
        download_button.removeAttr("href");
        download_button.prop("onclick", null);
      }

      code_div.html(code_block);
    })
    .then(() => {
      // @ts-ignore
      hljs.highlightAll();
    });
}
