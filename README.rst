Murano
======
Murano Project introduces an application catalog, which allows application
developers and cloud administrators to publish various cloud-ready
applications in a browsable‎ categorised catalog, which may be used by the
cloud users (including the inexperienced ones) to pick-up the needed
applications and services and composes the reliable environments out of them
in a “push-the-button” manner.

murano-tests
------------
murano-tests repository contains functional and performance tests for Murano
project. Functional tests are based on behave framework, performance tests
are based on FunkLoad framework. Please, refer to `How to Run`_ section for
details about how to run tests.

Project Resources
-----------------
* `Murano at Launchpad <http://launchpad.net/murano>`__
* `Wiki <https://wiki.openstack.org/wiki/Murano>`__
* `Code Review <https://review.openstack.org/>`__
* `Sources <https://wiki.openstack.org/wiki/Murano/SourceCode>`__
* `Developers Guide <http://murano-docs.github.io/latest/developers-guide/content/ch02.html>`__

How To Participate
------------------
If you would like to ask some questions or make proposals, feel free to reach
us on #murano IRC channel at FreeNode. Typically somebody from our team will
be online at IRC from 6:00 to 20:00 UTC. You can also contact Murano community
directly by openstack-dev@lists.openstack.org adding [Murano] to a subject.

We’re holding public weekly meetings on Tuesdays at 17:00 UTC
on #openstack-meeting-alt IRC channel at FreeNode.

If you want to contribute either to docs or to code, simply send us change
request via `gerrit <https://review.openstack.org/>`__.
You can `file bugs <https://bugs.launchpad.net/murano/+filebug>`__ and
`register blueprints <https://blueprints.launchpad.net/murano/+addspec>`__ on
Launchpad.

How to Run
==========

Tests For Web UI
----------------
The web UI tests allow to perform complex integration testing with REST API
service, REST API client, orchestrator component and Murano
dashboard component. The simplest way to execute webUI tests is to run tox.

Functional Tests For REST API service
-------------------------------------
To run all functional tests for REST API service need to run behave
with the following command::

   # cd murano-tests/rest_api_tests/functional <br>
   # behave rest_api_service.feature <br>

Note: need to set the correct configuration for REST API service. Please,
check config.ini file for more detailed information.


Performance Tests For REST API service
--------------------------------------
To run all performance tests for REAT API service need to run func
load banch with the following command::

   # cd murano-tests/rest_api_tests/load_and_performance <br>
   # fl-run-bench test_rest.py TestSuite.mix_for_load_testing <br>
   # fl-build-report --html --output-directory=html result-bench.xml <br>

After that we can find the html report in the same folder.

Note: need to set the correct configuration for REST API service.
Please, check config.ini file for more detailed information.
