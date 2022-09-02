const LIMIT = 100
const FUNCTION_END_POINT = "https://sentence-embedding-eatrmwevgq-ew.a.run.app/";

Papa.parse("data/embeddings.csv", {
  download: true,
  header: true,
  complete: function (raw) {
    // Massage data into format expected by Chartjs
    const truncated = raw.data.slice(0, LIMIT);

    const data = {
      datasets: [
        {
          label: "Active",
          sentences: truncated.map((element) => ` ${element["active_sentence"]}`),
          data: truncated.map((element) => [element["active_x_coord"], element["active_y_coord"]]),
          borderColor: Array(truncated.length).fill("#43a047"),
          backgroundColor: Array(truncated.length).fill("#7cb342")
        },
        {
          label: "Passive",
          sentences: truncated.map((element) => ` ${element["passive_sentence"]}`),
          data: truncated.map((element) => [element["passive_x_coord"], element["passive_y_coord"]]),
          borderColor: Array(truncated.length).fill("#1e88e5"),
          backgroundColor: Array(truncated.length).fill("#039be5")
        }
      ]
    };

    // Try to extract inputs from GET parameters
    const params = new URLSearchParams(window.location.search);
    const active = params.get("active")
    const passive = params.get("passive")

    // If we have inputs, send them to Cloud Function.
    if (active !== null && passive !== null) {
      // Update Form
      document.getElementsByName("active")[0].value = active;
      document.getElementsByName("passive")[0].value = passive;

      // Construt payload for Cloud Function
      const payload = {
        active: active,
        passive: passive
      }

      const request = new XMLHttpRequest();
      request.open("POST", FUNCTION_END_POINT, false);
      request.setRequestHeader("Content-Type", "application/json");
      request.send(JSON.stringify(payload));

      const response = JSON.parse(request.response);

      const activePosition = response.active;
      const passivePosition = response.passive;

      // add active data
      data.datasets[0].sentences.push(active);
      data.datasets[0].data.push([activePosition.x, activePosition.y]);
      data.datasets[0].borderColor.push("#8e24aa");
      data.datasets[0].backgroundColor.push("#d81b60");

      // add passive data
      data.datasets[1].sentences.push(passive);
      data.datasets[1].data.push([passivePosition.x, passivePosition.y]);
      data.datasets[1].borderColor.push("#8e24aa");
      data.datasets[1].backgroundColor.push("#d81b60");
    }

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
