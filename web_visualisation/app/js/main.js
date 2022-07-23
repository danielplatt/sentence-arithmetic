// The limit of pairs to load from the file
const LIMIT = 100

Papa.parse("data/embeddings.csv", {
  download: true,
  header: true,
  complete: function (raw) {
    const truncated = raw.data.slice(0, LIMIT - 1);
    const data = {
      datasets: [
        {
          label: "Active",
          sentences: truncated.map((element) => {
            return element["active_sentence"]
          }),
          data: truncated.map((element) => {
            return [element["active_x_coord"], element["active_y_coord"]]
          }),
          borderColor: "#43a047",
          backgroundColor: "#7cb342"
        },
        {
          label: "Passive",
          sentences: truncated.map((element) => {
            return element["passive_sentence"]
          }),
          data: truncated.map((element) => {
            return [element["passive_x_coord"], element["passive_y_coord"]]
          }),
          borderColor: "#1e88e5",
          backgroundColor: "#039be5"
        }
      ]
    };

    Chart.defaults.font.size = 19;
    Chart.defaults.font.family = "\"Alegreya\", sans-serif";

    const chart = new Chart(document.getElementById("sentences"), {
      type: "scatter",
      data: data,
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function (ctx) {
                return ctx.dataset.sentences[ctx.dataIndex];
              }
            }
          }
        }
      }
    });
  }
});
