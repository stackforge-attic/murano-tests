======================
FunkLoad_ bench report
======================


:date: 2013-10-31 06:08:55
:abstract: Glazier API Performance Tests
           Bench result of ``TestSuite.mix_for_load_testing``: 
           The complex test with different random requests

.. _FunkLoad: http://funkload.nuxeo.org/
.. sectnum::    :depth: 2
.. contents:: Table of contents
.. |APDEXT| replace:: \ :sub:`1.5`

Bench configuration
-------------------

* Launched: 2013-10-31 06:08:55
* From: tempest-node
* Test: ``test_rest.py TestSuite.mix_for_load_testing``
* Target server: http://172.18.78.92:8082/environments
* Cycles of concurrent users: [1, 5, 10, 20, 50, 100]
* Cycle duration: 200s
* Sleeptime between request: from 0.0s to 0.5s
* Sleeptime between test case: 0.01s
* Startup delay between thread: 0.01s
* Apdex: |APDEXT|
* FunkLoad_ version: 1.16.1


Bench content
-------------

The test ``TestSuite.mix_for_load_testing`` contains: 

* 6 page(s)
* 0 redirect(s)
* 0 link(s)
* 0 image(s)
* 0 XML RPC call(s)

The bench contains:

* 2592 tests, 69 error(s)
* 8647 pages, 69 error(s)
* 11091 requests, 69 error(s)


Test stats
----------

The number of Successful **Tests** Per Second (STPS) over Concurrent Users (CUs).

 .. image:: tests.png

 ================== ================== ================== ================== ==================
                CUs               STPS              TOTAL            SUCCESS              ERROR
 ================== ================== ================== ================== ==================
                  1              0.190                 38                 38             0.00%
                  5              0.980                197                196             0.51%
                 10              1.905                383                381             0.52%
                 20              3.025                619                605             2.26%
                 50              3.340                690                668             3.19%
                100              3.175                665                635             4.51%
 ================== ================== ================== ================== ==================



Page stats
----------

The number of Successful **Pages** Per Second (SPPS) over Concurrent Users (CUs).
Note that an XML RPC call count like a page.

 .. image:: pages_spps.png
 .. image:: pages.png

 ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                CUs             Apdex*             Rating               SPPS            maxSPPS              TOTAL            SUCCESS              ERROR                MIN                AVG                MAX                P10                MED                P90                P95
 ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                  1              0.888               Good              0.655              4.000                131                131             0.00%              0.023              0.969              3.895              0.031              0.579              2.686              3.056
                  5              0.889               Good              3.275              9.000                656                655             0.15%              0.023              0.948              3.920              0.030              0.589              2.632              2.738
                 10              0.884               Good              6.235             16.000               1249               1247             0.16%              0.021              1.012              4.854              0.031              0.618              2.656              2.851
                 20              0.863               Good             10.475             24.000               2109               2095             0.66%              0.023              1.207              5.271              0.037              0.814              2.939              3.196
                 50              0.727               FAIR             11.300             31.000               2282               2260             0.96%              0.025              2.800             12.528              0.191              2.235              6.187              7.292
                100              0.446       UNACCEPTABLE             10.950             37.000               2220               2190             1.35%              0.029              5.986             27.982              0.857              3.526             13.011             15.649
 ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================

 \* Apdex |APDEXT|

Request stats
-------------

The number of **Requests** Per Second (RPS) successful or not over Concurrent Users (CUs).

 .. image:: requests_rps.png
 .. image:: requests.png

 ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                CUs             Apdex*            Rating*                RPS             maxRPS              TOTAL            SUCCESS              ERROR                MIN                AVG                MAX                P10                MED                P90                P95
 ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                  1              0.888               Good              0.845              4.000                169                169             0.00%              0.023              0.751              3.355              0.030              0.078              2.443              2.633
                  5              0.889               Good              4.195             11.000                839                838             0.12%              0.023              0.742              3.838              0.030              0.065              2.448              2.634
                 10              0.884               Good              8.045             19.000               1609               1607             0.12%              0.021              0.786              4.824              0.031              0.090              2.477              2.657
                 20              0.863               Good             13.480             30.000               2696               2682             0.52%              0.023              0.953              4.934              0.036              0.322              2.719              2.927
                 50              0.727               FAIR             14.655             37.000               2931               2909             0.75%              0.025              2.231             12.401              0.129              1.414              5.273              6.676
                100              0.446       UNACCEPTABLE             14.235             42.000               2847               2817             1.05%              0.029              4.863             26.651              0.539              3.249             11.804             14.842
 ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================

 \* Apdex |APDEXT|

Slowest requests
----------------

The 5 slowest average response time during the best cycle with **20** CUs:

* In page 006, Apdex rating: POOR, avg response time: 2.72s, delete: ``/environments/9fdd48ffa4e446e4b86316eb6c3bf8ba``
  `Delete Environment`
* In page 004, Apdex rating: POOR, avg response time: 1.98s, delete: ``/environments/9873cf167b854e1a853ecf92b1be3dc3``
  `Delete Environment`
* In page 001, Apdex rating: Good, avg response time: 1.24s, post: ``/environments``
  `Create Environment`
* In page 002, Apdex rating: Excellent, avg response time: 0.22s, post: ``/environments/b2de38fa92ed4005a96748f0c1732715/configure``
  `Get Session For Environment`
* In page 003, Apdex rating: Excellent, avg response time: 0.11s, post: ``/environments/85cc38f7e43c48b79c5f390ce65fffcc/services``
  `Create ASP.Net service`

Page detail stats
-----------------


PAGE 001: Create Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Req: 001, post, url ``/environments``

     .. image:: request_001.001.png

     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                    CUs             Apdex*             Rating              TOTAL            SUCCESS              ERROR                MIN                AVG                MAX                P10                MED                P90                P95
     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                      1              1.000          Excellent                 39                 39             0.00%              0.565              0.636              1.112              0.568              0.600              0.740              0.900
                      5              0.990          Excellent                198                197             0.51%              0.558              0.684              1.602              0.570              0.622              0.884              1.050
                     10              0.984          Excellent                383                381             0.52%              0.562              0.773              1.897              0.584              0.697              1.027              1.339
                     20              0.881               Good                629                615             2.23%              0.571              1.244              4.934              0.690              1.073              2.026              2.472
                     50              0.400       UNACCEPTABLE                682                660             3.23%              0.634              4.573             12.401              1.470              4.617              7.716              8.365
                    100              0.128       UNACCEPTABLE                666                636             4.50%              1.133             10.180             26.651              2.144             10.541             16.611             17.851
     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================

     \* Apdex |APDEXT|

PAGE 002: Get Session For Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Req: 001, post, url ``/environments/c7ec2b4507b5464c9ceedee055883683/configure``

     .. image:: request_002.001.png

     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                    CUs             Apdex*             Rating              TOTAL            SUCCESS              ERROR                MIN                AVG                MAX                P10                MED                P90                P95
     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                      1              0.936               Good                 39                 39             0.00%              0.023              0.365              3.271              0.028              0.033              2.368              2.481
                      5              0.976          Excellent                186                186             0.00%              0.023              0.167              2.982              0.027              0.033              0.079              1.023
                     10              0.966          Excellent                366                366             0.00%              0.021              0.219              3.204              0.027              0.036              0.100              2.426
                     20              0.982          Excellent                596                596             0.00%              0.023              0.221              3.568              0.030              0.066              0.377              1.038
                     50              0.945          Excellent                651                651             0.00%              0.025              0.861              5.603              0.066              0.717              1.530              2.669
                    100              0.649               POOR                631                631             0.00%              0.029              2.392             10.543              0.217              2.604              3.675              4.372
     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================

     \* Apdex |APDEXT|

PAGE 003: Create ASP.Net farm service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Req: 001, post, url ``/environments/c7ec2b4507b5464c9ceedee055883683/services``

     .. image:: request_003.001.png

     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                    CUs             Apdex*             Rating              TOTAL            SUCCESS              ERROR                MIN                AVG                MAX                P10                MED                P90                P95
     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                      1              1.000          Excellent                 34                 34             0.00%              0.029              0.046              0.375              0.029              0.035              0.040              0.094
                      5              1.000          Excellent                177                177             0.00%              0.027              0.047              0.303              0.030              0.036              0.064              0.096
                     10              1.000          Excellent                341                341             0.00%              0.025              0.058              1.106              0.031              0.041              0.089              0.120
                     20              1.000          Excellent                574                574             0.00%              0.025              0.114              1.188              0.034              0.064              0.292              0.384
                     50              0.941          Excellent                615                615             0.00%              0.029              0.787              1.980              0.065              0.790              1.516              1.636
                    100              0.634               POOR                599                599             0.00%              0.030              2.465              4.765              0.217              2.899              3.873              4.137
     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================

     \* Apdex |APDEXT|

PAGE 004: Delete Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Req: 001, delete, url ``/environments/fba54b3967b2421abc0f79ef250be567``

     .. image:: request_004.001.png

     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                    CUs             Apdex*             Rating              TOTAL            SUCCESS              ERROR                MIN                AVG                MAX                P10                MED                P90                P95
     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                      1              0.682               POOR                 33                 33             0.00%              0.028              1.674              3.355              0.032              2.370              2.960              3.127
                      5              0.649               POOR                175                175             0.00%              0.028              1.791              3.475              0.034              2.401              2.664              2.743
                     10              0.636               POOR                339                339             0.00%              0.027              1.884              4.824              0.036              2.427              2.741              3.054
                     20              0.646               POOR                567                567             0.00%              0.030              1.981              4.506              0.043              2.541              3.085              3.378
                     50              0.635               POOR                614                614             0.00%              0.032              2.779              5.924              0.416              2.864              4.643              4.876
                    100              0.321       UNACCEPTABLE                597                597             0.00%              0.031              5.058             10.276              1.762              5.161              8.526              9.110
     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================

     \* Apdex |APDEXT|

PAGE 005: Create AD service
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Req: 001, post, url ``/environments/431fdbeaa2f74e5bb0331c9a03909537/services``

     .. image:: request_005.001.png

     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                    CUs             Apdex*             Rating              TOTAL            SUCCESS              ERROR                MIN                AVG                MAX                P10                MED                P90                P95
     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                      1              1.000          Excellent                 12                 12             0.00%              0.030              0.119              1.041              0.030              0.037              0.042              1.041
                      5              1.000          Excellent                 52                 52             0.00%              0.030              0.043              0.148              0.032              0.037              0.063              0.071
                     10              1.000          Excellent                 92                 92             0.00%              0.030              0.052              0.154              0.033              0.042              0.083              0.099
                     20              1.000          Excellent                166                166             0.00%              0.029              0.113              0.625              0.034              0.062              0.321              0.418
                     50              0.981          Excellent                185                185             0.00%              0.030              0.558              1.758              0.038              0.467              1.306              1.441
                    100              0.716               FAIR                178                178             0.00%              0.035              1.702              4.502              0.076              1.729              3.327              3.527
     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================

     \* Apdex |APDEXT|

PAGE 006: Delete Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Req: 001, delete, url ``/environments/431fdbeaa2f74e5bb0331c9a03909537``

     .. image:: request_006.001.png

     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                    CUs             Apdex*             Rating              TOTAL            SUCCESS              ERROR                MIN                AVG                MAX                P10                MED                P90                P95
     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================
                      1              0.500               POOR                 12                 12             0.00%              2.358              2.469              2.633              2.365              2.424              2.632              2.633
                      5              0.500               POOR                 51                 51             0.00%              2.355              2.590              3.838              2.377              2.443              3.041              3.211
                     10              0.500               POOR                 88                 88             0.00%              2.365              2.562              3.137              2.388              2.491              2.863              3.117
                     20              0.500               POOR                164                164             0.00%              2.384              2.724              4.092              2.427              2.624              3.148              3.496
                     50              0.500               POOR                184                184             0.00%              2.381              3.084              5.514              2.481              2.878              4.027              4.421
                    100              0.429       UNACCEPTABLE                176                176             0.00%              2.362              4.298              9.885              2.597              3.817              6.902              7.725
     ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ================== ==================

     \* Apdex |APDEXT|

Failures and Errors
-------------------


Failures
~~~~~~~~

* 69 time(s), code: 500::

    No traceback.


Definitions
-----------

* CUs: Concurrent users or number of concurrent threads executing tests.
* Request: a single GET/POST/redirect/xmlrpc request.
* Page: a request with redirects and resource links (image, css, js) for an html page.
* STPS: Successful tests per second.
* SPPS: Successful pages per second.
* RPS: Requests per second, successful or not.
* maxSPPS: Maximum SPPS during the cycle.
* maxRPS: Maximum RPS during the cycle.
* MIN: Minimum response time for a page or request.
* AVG: Average response time for a page or request.
* MAX: Maximmum response time for a page or request.
* P10: 10th percentile, response time where 10 percent of pages or requests are delivered.
* MED: Median or 50th percentile, response time where half of pages or requests are delivered.
* P90: 90th percentile, response time where 90 percent of pages or requests are delivered.
* P95: 95th percentile, response time where 95 percent of pages or requests are delivered.
* Apdex T: Application Performance Index, 
  this is a numerical measure of user satisfaction, it is based
  on three zones of application responsiveness:

  - Satisfied: The user is fully productive. This represents the
    time value (T seconds) below which users are not impeded by
    application response time.

  - Tolerating: The user notices performance lagging within
    responses greater than T, but continues the process.

  - Frustrated: Performance with a response time greater than 4*T
    seconds is unacceptable, and users may abandon the process.

    By default T is set to 1.5s this means that response time between 0
    and 1.5s the user is fully productive, between 1.5 and 6s the
    responsivness is tolerating and above 6s the user is frustrated.

    The Apdex score converts many measurements into one number on a
    uniform scale of 0-to-1 (0 = no users satisfied, 1 = all users
    satisfied).

    Visit http://www.apdex.org/ for more information.
* Rating: To ease interpretation the Apdex
  score is also represented as a rating:

  - U for UNACCEPTABLE represented in gray for a score between 0 and 0.5 

  - P for POOR represented in red for a score between 0.5 and 0.7

  - F for FAIR represented in yellow for a score between 0.7 and 0.85

  - G for Good represented in green for a score between 0.85 and 0.94

  - E for Excellent represented in blue for a score between 0.94 and 1.

Report generated with FunkLoad_ 1.16.1, more information available on the `FunkLoad site <http://funkload.nuxeo.org/#benching>`_.