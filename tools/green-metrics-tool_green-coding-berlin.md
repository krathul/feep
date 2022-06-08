# Green Coding Berlin's Open-Source (AGPL v.3) Green Metrics Tool

## Overview (June 2022)

See: <https://github.com/green-coding-berlin/green-metrics-tool>

See also: <https://metrics.green-coding.org/>

Here are some example measurements and more information for demonstration purposes of the tool.

A website as a static site and as a Wordpress site were set up in Docker containers. The Green Metrics Tool was run to measure them. Results can be found at:

 * Static version: <https://metrics.green-coding.org/stats.html?id=c64aebc7-5bde-4e17-a8ad-1dd2e01f587a>
 * Wordpress version: <https://metrics.green-coding.org/stats.html?id=1de1058e-5956-4414-a9ec-ec8dff6b10f5>

As expected the static site puts almost the same load on the browser. But in the static site the Server does nearly zero load, whereas the Wordpress container experiences significant load.

The values should be only be looked at in comparison to each other and not in absolute values, as we ran the tests with only the Docker-Stats as measurement provider and not with higher resolution in terms of CPU / Memory.

The energy metrics provider is currently with Intel RAPL only and does not run on the cloud service.

We included a Dockerfiles installation method in the revamped Readme (https://github.com/green-coding-berlin/green-metrics-tool) which now should get the tool locally up and running in under 5 minutes.

A slide deck was also included which highlights some of the key features as we envision the tool to include the Open Data API. This will be useful to answer questions such as "How much more energy does a static site use compared to a Wordpress site?" or "How much more energy does React consume against Vue.js for the same task?"

An example of how the API can be used currently and how much more granularity it allows in terms of data drilldown you can see in our example Jupyter Notebooks on Deepdown:

 * Deep Dive in a single measurement: <https://deepnote.com/workspace/gmt-8c072e35-bfaf-49e7-a465-43515ce582b3/project/Green-Metrics-API-example-Single-Measurement-d8b7eee6-6d81-4774-96fe-1405babd2a0a/%2Fnotebook.ipynb>

 * Comparing the static and the Wordpress variant of the Green Web Foundation Website in terms of Mean and StdDev: <https://deepnote.com/workspace/gmt-8c072e35-bfaf-49e7-a465-43515ce582b3/project/Green-Metrics-API-example-Single-Measurement-Duplicate-ee5162cd-03ab-49e2-aaaa-02c3f5741429/%2Fnotebook.ipynb>
