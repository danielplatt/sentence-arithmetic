Papa.parse("data/embeddings.csv", {
  download: true,
  header: true,
  complete: function (raw) {
    const data = {
      datasets: [
        {
          label: "Active",
          sentences: raw.data.map((element) => {
            return element["active_sentence"]
          }),
          data: raw.data.map((element) => {
            return [element["active_x_coord"], element["active_y_coord"]]
          }),
          borderColor: "red",
          backgroundColor: "purple"
        },
        {
          label: "Passive",
          sentences: raw.data.map((element) => {
            return element["passive_sentence"]
          }),
          data: raw.data.map((element) => {
            return [element["passive_x_coord"], element["passive_y_coord"]]
          }),
          borderColor: "blue",
          backgroundColor: "cyan"
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
            display: true,
            text: "Sentences"
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
