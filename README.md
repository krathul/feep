# FOSS Energy Efficiency Project

## Vision

The goal of the Free and Open Source Energy Efficiency Project (FOSSEEP) is to improve the energy efficiency of free and open source software.

Design and implementation of software has a significant impact on the energy consumption of the systems it is part of. By becoming aware of the factors how software affects energy consumption and providing tools to quantify them it is possibly to drive down energy consuption and increase energy efficiency. This contributes to a more sustainable use of energy as one of the shared resources of our planet. This project strives to achieve that for and through Free and Open Source Software (FOSS).

Let's make energy efficient software part of our story so we can live up to our responsibility for this and future generations.

## Strategy

As a first step we will develop a framework to measure energy consumption of FOSS applications using the [criteria for the Blue Angel environmental label](https://produktinfo.blauer-engel.de/uploads/criteriafile/en/DE-UZ%20215-202001-en-Criteria-2020-02-13.pdf) based on the [research by the Environmental Campus  Birkenfeld](https://www.umwelt-campus.de/en/research/projekte/green-software-engineering/projects/ufoplan-ssd-2015) and execute measurements on selected applications, starting with a set of KDE applications.

Later we intend to integrate measuring energy consumption into the development process of applications so that energy efficiency can become a quality metric for these applications.

To scale this to a wide variety of projects we envision a distributed network of FOSS energy measurement labs which provide energy consumption data to projects as a service which can be intergrated as quality gate in release processes and drive energy efficiency as a goal of the development process.

We start with KDE but are happy to welcome other projects to join the project. The current focus are desktop applications where the most solid and usable procedures exist for measuring energy consumption. This will likely be expanded in the future to other types of applications and systems.

## Resources

This repository contains the following resources:

* [Usage scenarios](usage_scenarios) - Detailed Descriptions of usage scenarios for specific application types. These are the scenarios for which energy consumption will be measured.
* [Measurement setup](measurement_setup.md) - Description of hardware and software setup for performing energy measurements. This defines comparable environments and tools how to do automated measurements.
* [Test runs](test_runs) - Automation for doing test runs of specific applications for their corresponding usage scenarios.

## License

The content of this repository is licensed under the [MIT license](https://opensource.org/licenses/MIT). See the file [LICENSE.txt](LICENSE.txt) for the full text of the license.
