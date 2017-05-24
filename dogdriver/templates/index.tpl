<%inherit file="base.tpl"/>
<script src="//code.jquery.com/jquery-3.2.1.min.js"></script>
<script
src="//cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.bundle.js"></script>


<div class="column-group gutters">
  <div class="all-33 small-100 tiny-100">
    <h3>CPU Load</h3>
    <canvas id="CPU"></canvas>
    <p class="quarter-top-space">Some comment about CPU</p>
  </div>
  <div class="all-33 small-100 tiny-100">
    <h3>Requests Per Minute</h3>
    <canvas id="RPM"></canvas>
    <p class="quarter-top-space">Some comment about RPM</p>
  </div>
  <div class="all-33 small-100 tiny-100">
    <h3>Average Response Time</h3>
    <canvas id="RT"></canvas>
    <p class="quarter-top-space">Some comment about Response Time</p>
  </div>
</div>

<script>

function drawChart(project, metric, target) {
var jsonData = $.ajax({
    url: 'http://localhost:8080/runs/' + project + '/' + metric,
    dataType: 'json',
  }).done(function (results) {

var labels = [], data = [];
var chart = {
        labels: labels,
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
      labels.push(run.label);
      data.push(run.value);
    });

   var ctx = document.getElementById(target);
   var myChart = new Chart(ctx, {
    type: 'line',
    data: chart,
    options: {
        legend: {
            display: false,
        },
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
});
}


drawChart('kintowe', 'cpu', 'CPU');
drawChart('kintowe', 'rpm', 'RPM');
drawChart('kintowe', 'art', 'RT');
</script>

