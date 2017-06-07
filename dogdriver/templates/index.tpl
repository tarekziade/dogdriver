<%inherit file="base.tpl"/>
<script src="//code.jquery.com/jquery-3.2.1.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.bundle.js"></script>


<div class="column-group gutters">
  <div class="all-33 small-100 tiny-100">
    <h3>CPU Load (%)</h3>
    <canvas id="CPU"></canvas>
    <p class="quarter-top-space">Some comment about CPU</p>
  </div>
  <div class="all-33 small-100 tiny-100">
    <h3>Requests Per Second</h3>
    <canvas id="RPS"></canvas>
    <p class="quarter-top-space">Some comment about RPS</p>
  </div>
  <div class="all-33 small-100 tiny-100">
    <h3>Backend Latency (ms)</h3>
    <canvas id="RT"></canvas>
    <p class="quarter-top-space">Some comment about Response Time</p>
  </div>
</div>

<script>

Date.prototype.format = function() {
  var hour = this.getHours() + ':' + this.getMinutes();
  var date = (this.getMonth() + 1) + "/" +  this.getDate();
  return hour + ' ' + date;
}

Chart.defaults.derivedlinee = Chart.defaults.line;

var custom = Chart.controllers.line.extend({
    draw: function (ease) {
        Chart.controllers.line.prototype.draw.call(this, ease);

        var meta = this.getMeta();
        var scale = this.chart.scales['x-axis'];
        var ctx = this.chart.chart.ctx;


        ctx.save();

        var releases = (this.chart.config.data.releases);

        for (var i=0; i < releases.length; i++) {
            var version = releases[i];
            if (version != "") {
                var point = meta.data[i];
                // draw line
                ctx.beginPath();
                ctx.strokeStyle = 'red';
                ctx.lineWidth = 2;
                ctx.moveTo(point._model.x, 5);
                ctx.lineTo(point._model.x, scale.top);
                ctx.stroke();

                // write label
                ctx.textAlign = 'left';
                ctx.font = "14px Georgia";
                ctx.fillStyle = 'black';
                ctx.fillText(version, point._model.x + 4, 10);
            }
        }
        ctx.restore();
    }
});


Chart.controllers.derivedLine = custom;


function drawChart(project, metric, target) {
var jsonData = $.ajax({
    url: 'http://localhost:8080/runs/' + project + '/' + metric + '?source=tarek',
    dataType: 'json',
  }).done(function (results) {

var labels = [], data = [], releases = [];
var chart = {
        labels: labels,
        releases: releases,
        datasets: [{
            data: data,
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            spanGaps: false,
        }]
};

    results["data"].forEach(function(run) {
       labels.push(new Date(run.label*1000).format());
       data.push(run.value);
       releases.push(run.release);
    });


   var ctx = document.getElementById(target);
   var myChart = new Chart(ctx, {
    type: 'derivedLine',
    data: chart,
    options: {
        backgroundColor:'rgb(10,10,10)',
        legend: {
            display: false,
        },
        scales: {
            xAxes: [{'id': 'x-axis'}],
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});
});
}


drawChart('kintowe', 'cpu', 'CPU');
drawChart('kintowe', 'rps', 'RPS');
drawChart('kintowe', 'art', 'RT');
</script>

