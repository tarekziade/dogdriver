<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>dogDriver ~ Performance tracking</title>
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
            header h1 img {
              vertical-align: middle;
            }
            header h1 {
              color: black;
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



<h1><img src="data:image/svg+xml;utf8;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTYuMC4wLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+CjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4PSIwcHgiIHk9IjBweCIgd2lkdGg9IjMycHgiIGhlaWdodD0iMzJweCIgdmlld0JveD0iMCAwIDk1Ny43NTEgOTU3Ljc1MSIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgOTU3Ljc1MSA5NTcuNzUxOyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+CjxnPgoJPGc+CgkJPHBhdGggZD0iTTE2Ni4xNzUsNDE0LjgxOGM4LTEwOC4yLDE1LjYtMjAyLjYwMSwxMDItMjEzLjJjMTAuNS0xNy42LDIzLjItMzMuOCwzNy44LTQ4LjRjMTQuOS0xNC45LDMxLjQtMjcuNiw0OS40LTM4LjEgICAgYy0xOC41LTIwLjktNDQuOS00Mi42LTc5LjEwMS01MWMtNzQuMy0xOC40LTIwMi42LTUuNC0yNjQuNywyNDVDLTUwLjQyNSw1NTkuNDE4LDE1Ni4zNzUsNTQ3LjgxOCwxNjYuMTc1LDQxNC44MTh6IiBmaWxsPSIjMDAwMDAwIi8+CgkJPHBhdGggZD0iTTY4MS40NzUsNjQuMDE4Yy0zNC41LDguNS02MSwzMC40LTc5LjQsNTEuNGMxNy43LDEwLjQsMzQsMjMsNDguNywzNy43YzE0LjYwMSwxNC42LDI3LjEwMSwzMC44LDM3LjUwMSw0OC4zICAgIGM4Ny42OTksOS44LDk1LjI5OSwxMDQuNiwxMDMuMjk5LDIxMy4zYzkuODAxLDEzMywyMTYuNjAyLDE0NC43LDE1NC42MDItMTA1LjhDODg0LjE3Niw1OC42MTgsNzU1Ljc3NSw0NS42MTgsNjgxLjQ3NSw2NC4wMTh6IiBmaWxsPSIjMDAwMDAwIi8+CgkJPHBhdGggZD0iTTY0Ni43NzQsMjAyLjUxOGMtMTcuNS0yMy45LTQwLTQ0LTY2LTU4LjdjLTMwLjM5OS0xNy4yLTY1LjM5OS0yNy0xMDIuNzk5LTI3Yy0zNi44LDAtNzEuNCw5LjUtMTAxLjQsMjYuMiAgICBjLTI2LjUsMTQuNy00OS4zOTksMzUtNjcuMTk5LDU5LjJjLTI1LjQsMzQuNi00MC40LDc3LjItNDAuNCwxMjMuM3YxMjQuM2MtNTMsNDcuNjk5LTg0LjcsMTEzLjM5OS04NC43LDE4NiAgICBjMCwxNDAuNiwxMjIuNSwyNTUuNSwyNzYuNywyNjMuNnYtMjY5LjJjLTM2LjYtNS4xLTY0LTI1Ljg5OS02NC01MC44YzAtMjguNywzNi41LTUyLDgxLjUtNTJjNDUsMCw4MS41LDIzLjMsODEuNSw1MiAgICBjMCwyNC45LTI3LjQsNDUuNy02NCw1MC44djI2OS4yYzE1NC4yLTguMSwyNzYuNC0xMjMsMjc2LjQtMjYzLjZjMC03Mi41LTMzLjQtMTM4LjItODUuNC0xODZ2LTEyNC4zICAgIEM2ODYuOTc1LDI3OS41MTgsNjcyLjA3NCwyMzcuMDE4LDY0Ni43NzQsMjAyLjUxOHogTTI5Ny4wNzUsNzY4LjUxOGMtMTEuMzk5LDAtMjAuNy05LjMtMjAuNy0yMC42OTljMC0xMS40LDkuMy0yMC43LDIwLjctMjAuNyAgICBjMTEuNCwwLDIwLjcsOS4zLDIwLjcsMjAuN0MzMTcuNzc1LDc1OS4yMTgsMzA4LjQ3NSw3NjguNTE4LDI5Ny4wNzUsNzY4LjUxOHogTTMwMC40NzUsNjk0LjUxOGMtMTEuNCwwLTIwLjctOS4zLTIwLjctMjAuNjk5ICAgIGMwLTExLjQsOS4zLTIwLjcsMjAuNy0yMC43czIwLjcsOS4zLDIwLjcsMjAuN0MzMjEuMDc1LDY4NS4yMTgsMzExLjg3NSw2OTQuNTE4LDMwMC40NzUsNjk0LjUxOHogTTMyMi45NzUsMzk3LjQxOCAgICBjMC0xNi42LDEzLjQtMzAsMzAtMzBzMzAsMTMuNCwzMCwzMGMwLDE2LjYtMTMuNCwzMC0zMCwzMFMzMjIuOTc1LDQxNC4wMTgsMzIyLjk3NSwzOTcuNDE4eiBNMzYyLjY3NSw3MzUuNzE4ICAgIGMtMTEuNCwwLTIwLjctOS4zLTIwLjctMjAuN2MwLTExLjM5OSw5LjMtMjAuNjk5LDIwLjctMjAuNjk5YzExLjM5OSwwLDIwLjcsOS4zLDIwLjcsMjAuNjk5ICAgIEMzODMuMjc1LDcyNi40MTgsMzc0LjA3NSw3MzUuNzE4LDM2Mi42NzUsNzM1LjcxOHogTTU5NS4wNzQsNzM1LjcxOGMtMTEuMzk5LDAtMjAuNjk5LTkuMy0yMC42OTktMjAuNyAgICBjMC0xMS4zOTksOS4zLTIwLjY5OSwyMC42OTktMjAuNjk5YzExLjQsMCwyMC43LDkuMywyMC43LDIwLjY5OUM2MTUuNzc0LDcyNi40MTgsNjA2LjQ3NSw3MzUuNzE4LDU5NS4wNzQsNzM1LjcxOHogICAgIE02MDMuOTc1LDQyNy40MThjLTE2LjYsMC0zMC0xMy40LTMwLTMwYzAtMTYuNiwxMy40LTMwLDMwLTMwczMwLDEzLjQsMzAsMzBDNjMzLjk3NSw0MTQuMDE4LDYyMC41NzQsNDI3LjQxOCw2MDMuOTc1LDQyNy40MTh6ICAgICBNNjU3LjI3NCw2NTMuMjE4YzExLjQsMCwyMC43LDkuMywyMC43LDIwLjdzLTkuMywyMC43LTIwLjcsMjAuN2MtMTEuMzk5LDAtMjAuNy05LjMtMjAuNy0yMC43ICAgIEM2MzYuNTc0LDY2Mi40MTgsNjQ1Ljg3NSw2NTMuMjE4LDY1Ny4yNzQsNjUzLjIxOHogTTY2MC42NzUsNzY4LjUxOGMtMTEuNCwwLTIwLjctOS4zLTIwLjctMjAuNjk5YzAtMTEuNCw5LjMtMjAuNywyMC43LTIwLjcgICAgYzExLjM5OSwwLDIwLjcsOS4zLDIwLjcsMjAuN0M2ODEuMjc0LDc1OS4yMTgsNjcyLjA3NCw3NjguNTE4LDY2MC42NzUsNzY4LjUxOHoiIGZpbGw9IiMwMDAwMDAiLz4KCTwvZz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8L3N2Zz4K" />
                dogDriver<small>performance tracking</small></h1>
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
                    <li><a href="http://www.freepik.com">Dog Icon CC 3.0 BY</a></li>
                </ul>
            </div>

        </footer>

    </body>

</html>

