const LIMIT = 100

Papa.parse("data/embeddings.csv", {
  download: true,
  header: true,
  complete: function (raw) {
    const truncated = raw.data.slice(0, LIMIT);
    const data = {
      datasets: [
        {
          label: "Active",
          sentences: truncated.map((element) => ` ${element["active_sentence"]}`),
          data: truncated.map((element) => [element["active_x_coord"], element["active_y_coord"]]),
          borderColor: "#43a047",
          backgroundColor: "#7cb342"
        },
        {
          label: "Passive",
          sentences: truncated.map((element) => ` ${element["passive_sentence"]}`),
          data: truncated.map((element) => [element["passive_x_coord"], element["passive_y_coord"]]),
          borderColor: "#1e88e5",
          backgroundColor: "#039be5"
        }
      ]
    };

    const PLUGIN_ID = "sentence";

    const plugin = {
      id: "sentenceConnector",
      afterInit: (chart) => {
        chart[PLUGIN_ID] = {
          index: null
        }
      },
      afterEvent: (chart, evt) => {
        const activeEls = chart.getElementsAtEventForMode(evt.event, "nearest", {
          intersect: true
        }, true)

        if (activeEls.length === 0) {
          chart[PLUGIN_ID].index = null
          return;
        }


        chart[PLUGIN_ID].index = activeEls[0].index;
      },
      beforeDatasetsDraw: (chart, _, opts) => {
        const {
          ctx
        } = chart;
        const {
          index
        } = chart[PLUGIN_ID];

        if (index === null) {
          return;
        }
        const dp0 = chart.getDatasetMeta(0).data[index]
        const dp1 = chart.getDatasetMeta(1).data[index]

        ctx.lineWidth = opts.width || 0;
        ctx.setLineDash(opts.dash || []);
        ctx.strokeStyle = opts.color || "black"

        ctx.save();
        ctx.beginPath();
        ctx.moveTo(dp0.x, dp0.y);
        ctx.lineTo(dp1.x, dp1.y);
        ctx.stroke();
        ctx.restore();
      }
    }

    Chart.defaults.font.size = 16;
    Chart.defaults.font.family = "\"Alegreya\", sans-serif";

    new Chart(document.getElementById("sentences"), {
      type: "scatter",
      data: data,
      options: {
        responsive: true,
        plugins: {
          sentenceConnector: {
            dash: [2, 2],
            color: "#f4511e",
            width: 2
          },
          legend: {
            position: "top",
          },
          tooltip: {
            callbacks: {
              label: function (ctx) {
                return ctx.dataset.sentences[ctx.dataIndex]
                  // Remove extra whitespace
                  .replace(/\s\s+/g, " ").trim()
                  // Split in arrays of 4 words
                  .match(/\b[\w']+(?:\s+[\w']+){0,4}/g);
              }
            }
          }
        }
      },
      plugins: [plugin]
    });
  }
});
