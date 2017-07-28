<%inherit file="base.tpl"/>
<script src="//code.jquery.com/jquery-3.2.1.min.js"></script>

<div class="column-group gutters">
  % for project in projects:
  <div class="all-33 small-100 tiny-100" style="font-size: 200%">
    <a href="/dogdriver/${project['name']}">${project['name']}</a>
    <span id="${project['name']}Trend">TREND</span>
  </div>
  <script>
    var jsonData = $.ajax({
      url: '/dogdriver/trend/${project['name']}?source=${source}',
    dataType: 'json',
  }).done(function (results) {
    $('#${project['name']}Trend').html(results["trend"]);
   });

  </script>
  % endfor
</div>

