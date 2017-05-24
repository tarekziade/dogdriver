<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Dogdriver ~ Performance tracking</title>
        <meta name="HandheldFriendly" content="True">
        <meta name="MobileOptimized" content="320">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">

        <!-- Place favicon.ico and apple-touch-icon(s) here  -->
        <link rel="apple-touch-icon" type="image/png" sizes="180x180" href="//www.mozilla.org/media/img/favicon/apple-touch-icon-180x180.8772ec154918.png">
        <link rel="icon" type="image/png" sizes="196x196" href="//www.mozilla.org/media/img/favicon/favicon-196x196.c80e6abe0767.png">
        <link rel="shortcut icon" href="//www.mozilla.org/media/img/favicon.d4f1f46b91f4.ico">

        <!-- load Ink's css from the cdn -->
        <link rel="stylesheet" type="text/css" href="//cdn.ink.sapo.pt/3.1.10/css/ink-flex.min.css">
        <link rel="stylesheet" type="text/css" href="//cdn.ink.sapo.pt/3.1.10/css/font-awesome.min.css">
        <!-- test browser flexbox support and load legacy grid if unsupported -->
        <script type="text/javascript" src="//cdn.ink.sapo.pt/3.1.10/js/modernizr.js"></script>
        <script type="text/javascript">
            Modernizr.load({
              test: Modernizr.flexbox,
              nope : '//cdn.ink.sapo.pt/3.1.10/css/ink-legacy.min.css'
            });
        </script>

        <!-- load Ink's javascript files from the cdn -->
        <script type="text/javascript" src="//cdn.ink.sapo.pt/3.1.10/js/holder.js"></script>
        <script type="text/javascript" src="//cdn.ink.sapo.pt/3.1.10/js/ink-all.min.js"></script>
        <script type="text/javascript" src="//cdn.ink.sapo.pt/3.1.10/js/autoload.js"></script>


        <style type="text/css">

body {
                background: #ededed;
            }

            header h1 small:before  {
                content: "|";
                margin: 0 0.5em;
                font-size: 1.6em;
            }

            footer {
                background: #ccc;
            }

        </style>
    </head>

    <body>
      <div class="ink-grid">
            <header class="vertical-space">
                <h1>moz://a dogdriver<small>performance tracking</small></h1>
                <nav class="ink-navigation">
                    <ul class="menu horizontal black">
                        <li class="active"><a href="#">kintowe</a></li>
                        <li><a href="#">absearch</a></li>
                        <li><a href="#">sync</a></li>
                    </ul>
                </nav>
            </header>
            <div class="ink-grid vertical-space">
                ${self.body()}
            </div>
            <div class="push"></div>
        </div>

        <footer class="clearfix">
            <div class="ink-grid">
                <ul class="unstyled inline half-vertical-space">
                    <li class="active"><a href="#">About</a></li>
                    <li><a href="#">Mozilla QA</a></li>
                </ul>
            </div>
        </footer>

    </body>

</html>

