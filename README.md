<a name="readme-top"></a>

<!-- PROJECT LOGO/HEADER -->
  <h1 align="center">THIS REPOSITORY IS NO LONGER UNDER ACTIVE USE OR DEVELOPMENT.  IT REMAINS HERE SOLELY FOR HISTORICAL PURPOSES!</h3>

  <h3 align="center">Degrees of Freedom Scouting</h3>

  <p align="center">
    The scouting system used by FRC Team 6413, Degrees of Freedom, for the 2023 through 2025 seasons.  It is a **heavily** modified version of the scouting system created by the CocoNuts (FRC Team 2486) which you can find 
    <a href="https://github.com/mikejed/CocoNuts-Scouting"><strong>here</strong></a> and is likely no longer closely aligned with the original codebase.
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About This Project

As most any FRC team who has done scouting can verify, scouting using paper is a massive pain.  A digital system for collecting scouting data is what every team needs.  FRC Team 6413 needed to find a system that worked for them.  During our search we saw the system built by FRC Team 2486 at an Arizona Robotics League event.  Since they offered to share it, we decided to give it a shot.  Our fork is a **very heavily** modified version of the one they used in 2023.  We updated it to suite our needs and to collect the data we wanted to see.

The biggest attraction initially was the ability to use our tablets to scout at an event without needing to use Wi-Fi which is not permitted.  The collected data is put into a QR code which we scan using a handheld barcode scanner.  The data is then saved into either a MySQL or MongoDB database and visualized using Tableau or Streamlit.

We also borrowed some scripts from the ScoutingPASS system created and maintained by PWNAGERobotics <a href="https://github.com/PWNAGERobotics/ScoutingPASS"><strong>here</strong></a>.  ScoutingPASS is used by several teams but its UX model did not quite fit with our needs so we only borrowed some bits related to reading and using team and schedule data from The Blue Alliance.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Scouting is done by simply loading the index.html file in the repo in a browser.  The page will load the 4 Javascript files it needs to configure itself and to get functionality to read from The Blue Alliance and generate QR codes.

There are 3 easy ways to use the page:

1: Grab a copy of the repo and simply double click on the index.html file to use it locally.  It will load up and let you scout for the configured event.
2: Run a local web server like the <a href="https://www.rebex.net/tiny-web-server/">Rebex Tiny Web Server</a> to host the file on your local network.
3: Put the index.html and all the .js files on an Internet accessible web server and then load it with any browser.

Once the page is loaded, fill out the various fields.  When you are done scouting, click on the **Get QR Code** button at the bottom.  All of the data on the page will be encoded as a JSON object in the QR code on the page.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Configuration

The page uses the TBA event code stored in the config.js file to decide what event data to load.  Simply change the **eventCode** value in that file to pick a different event.

If you want to change the year so you can have a 2023, 2024, etc config then you will also need to edit the script at the top of index.html to load the configuration file you want to use.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Add README.md
- [ ] Do well at the FIRST Championship in Houston

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Degrees of Freedom - [@dof6413](https://twitter.com/dof6413) - [Instagram](https://www.instagram.com/dof6413) - [Facebook](https://www.facebook.com/dof6413) - [YouTube](https://www.youtube.com/channel/UCoJrt-wiXr132q2F-QRBeTw) - dof6413@gmail.com

Project Link: [https://github.com/DoF-6413/Dof-Scouting](https://github.com/DoF-6413/Dof-Scouting)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

A very big Thank You to the following:

* [The Si Se Puede Foundation for sponsoring us](https://www.sisepuedefoundation.org/)
* [FRC Team 2486 - The CocoNuts for getting us started](https://github.com/coconuts2486-frc)
* [FRC Team 2451 - PWNAGERobotics for portions of their ScoutingPASS system](https://github.com/PWNAGERobotics/ScoutingPASS)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
