<br><br>

# Newcomer's Guide
<br><br><br>
<p align="center">
<img src="https://github.com/NeRF-or-Nothing/vidtonerf/raw/master/pics/logo.png" width="100" height="100" /></p>
<p align="center">This is a guideline for those who newly got into the project<br>for everyone to start from the same place in the beginning.<br>Follow these steps and reach out with any questions.</p>

<br><br><br><br><br><br><br><br><br><br>

## Section 1: Getting Started

<br><br>

### Step 1: Make sure to set up SSH
Take time to read through [**SSH_SETUP.md**](https://github.com/NeRF-or-Nothing/vidtonerf/blob/master/SSH_SETUP.md "SSH_SETUP.md") and make sure to set up and understand the relationship between **your local machine**, your generated <ins>SSH key</ins> on your machine, <ins>keychain</ins> for your convenience, <ins>Github</ins>, and pushing from your local machine **to our Github repository**.<br><br>

<br>

---

<br>

### Step 2: Create A New Fork

<br>

<p align="center">
  <br>
<img src="https://user-images.githubusercontent.com/113729242/222869116-608f1dc6-ce35-4d1d-b5fe-8fe6c32f2981.png" width="700" height="400" /></p>
<p align="center">In the repository you plan to work on, click on 'fork'.</p>
<br>

<p align="center">
<img src="https://user-images.githubusercontent.com/113729242/222869927-09e3376f-b998-4ea2-999d-3f6caf8ed8ba.png" width="700" height="400" /></p>
<p align="center">By default, the repository name will be set the same as the repository you are working on. <br />Go on, and click 'Create fork'.</p>
<br>

<p align="center">
<img src="https://user-images.githubusercontent.com/113729242/222870211-ae015a82-a7a5-4226-92fd-76bee7e2db64.png" width="700" height="400" /></p>
<p align="center">You should see the page simillar to this. <br />The name of the repository will be different with me if you are working on another repository.</p>
<br>

<p align="center">
<img src="https://user-images.githubusercontent.com/113729242/222918283-bbf34fbf-3af9-4259-baf2-3581ccaa32ac.png" width="700" height="400" /></p>
<p align="center">Click on 'Code', and the copy symbol. Make sure to choose option 'SSH'.</p>
<br>

<br><br><br>

---

<br>

### Step 3: Create Local Work Directory

<br><br>

<p align="center">
  <br>
<img src="https://user-images.githubusercontent.com/113729242/222919692-09e669c2-cfd4-47fe-9b76-df4a38ee76d1.png" width="700" height="400" /></p>
<p align="center">Create your local folder that you will be working on. <br>I created the folder 'Nerf' on my Desktop. <br>It doesn't have to be on the Desktop, but your choice of preference.</p>
<br>

<p align="center">
  <br>
<img src="https://user-images.githubusercontent.com/113729242/222921042-61bb2cc0-247a-4ed7-a51b-d7d9828bee87.png" width="700" height="400" /></p>
<p align="center">Open your terminal, go to the directory you just created.<br>In my case, I am now in the Nerf folder.</p>
<br>

<p align="center">
  <br>
<img src="https://user-images.githubusercontent.com/113729242/222921259-2778d4c5-d991-48a3-8bc8-50c9c5fffa6f.png" width="700" height="170" /></p>
<p align="center">Do git clone and paste the link you just copied in Step 2, in the fork page.<br></p>
<br>

<p align="center">
  <br>
<img src="https://user-images.githubusercontent.com/113729242/222922573-a9542703-cd95-4e5c-8d1b-c8daf1d15a94.png" width="700" height="270" /></p>
<p align="center">Since in my case I cloned into vidtonerf, <br>I will now have 'vidtonerf' folder in the directory 'Nerf'.
<br>If your fork repository name is different, you cloned into that repository name.<br>Go to that folder, in my case, vidtonerf.<br>And do the commands 'git fetch' and 'git pull'.</p>
<br><br><br>

---

<br><br>

## Section 2: Docker Installation

<br>

The important part in the project is you know **how to use Docker**.<br>
First, [<ins>**Install Docker desktop**</ins>](https://docs.docker.com/get-docker/ "Install Docker desktop") and make sure you can start it up and it says running.<br>If you are using Mac, make sure you know whether you have an intel chip inside or an Apple sillicon chip. There are two versions for Mac.<br><br>
In the configuration screen within the Installer,<br>
check `Use WSL 2 instead of Hyper-V (recommended)`, Click `OK`, `Install`<br>`Close` and log out to your computer.<br>
Log in back to your computer and reboot the system (recommended)<br>Log in to your computer again, open Docker Desktop.<br>
Click `Accept` to the agreement, and you will see it says 'Docker desktop is starting...' (click done installation).

[[I have an isse with the installation](#installation-issue-keep-updated)] | [[done installation](#start-docker-desktop)]

<br>

---

<br>

### Installation Issue (keep updated)
These are installation issues we know of right now. Please reach out with any further issues and let it documented.
<br><br><br>


#### Case 1: You have Windows and Docker is starting forever instead of actually booting up.
> In this case, this is likely due to an out of date WSL (WSL and docker share the same hypervisor).<br>
> First, you should make sure you are on WSL2 which can be checked in the command line by entering `wsl -l -v` on your terminal.<br>
> If you don't have WSL, open up Powershell as an admininstrator and do `wsl --install`.<br>
> If you see in the command line that you have the version 1, you can update from 1 to 2 by `wsl --update`.<br> 
> Try the same if you are on version 2 and having this issue as well, as WSL could be out of date.<br>
> If you are still having the issue, you should let us know.<br>
> If you need more info about installing WSL, check out [installing](https://learn.microsoft.com/en-us/windows/wsl/install).

[[ready to install Docker again](#section-2-docker-installation) | [[done installation](#start-docker-desktop)]

<br>

#### Case 2: next possible issue.
> In this case,
> <br>
> <br>

[[ready to install Docker again](#section-2-docker-installation) | [[done installation](#start-docker-desktop)]




...

<br><br><br><br><br>










> <ins>Below is the quick overview of possible other cases for Windows.</ins> <br>
> Docker can use either Windows Subsystem for Linux (WSL2) or Hyper-V as backend. (WSL2 recommended)<br>
> The current version of a Docker Desktop only works on the 64-bit edition of Windows. Both Windows 10 and Windows 11 are supported.
>
>`requirements for Windows:`<br>
>**Windows 10** - Home/Pro 21H1 (build19403) or higher, or Enterprise/Education 20H2 (build 19402) or higher<br>
>**Windows 11** -Home/Pro 21H2 or higher, or Enterprise/Education 21H2 or higher WSL2 feature must be installed and enabled.<br>
>Linux kernel update package for **WSL2** must be installed.<br>
>You need **64-bit CPU** (with second-level adress translation - SLAT) enabled<br>
>You need **4 GB of RAM**.<br>

[[ready to install Docker again](#section-2-docker-installation) | [[done installation](#start-docker-desktop)]

<br><br><br>

---

<br>

### Start Docker Desktop

<br>

<p align="center">
  <br>
<img src="https://user-images.githubusercontent.com/113729242/222935005-7ce639b8-69b2-4185-9f9a-407eb17ce9bc.png" width="700" height="400" /></p>
<p align="center">When you are done with the installation and open Docker, <br>you might see 'Docker Desktop Starting' for few seconds.<br></p>
<br>

<p align="center">
  <br>
<img src="https://user-images.githubusercontent.com/113729242/222935112-bb55b6ce-bce9-48f0-baf2-3a9c31548879.png" width="700" height="400" /></p>
<p align="center">Next, it asks you to start the tutorial, but you can skip it. <br>Instead, click on 'sign in' and log in to your account or, <br>create a new Docker account and sign in.<br></p>
<br>

<p align="center">
  <br>
<img src="https://user-images.githubusercontent.com/113729242/222935221-df08e937-5f47-484a-b310-1248940b4648.png" width="700" height="400" /></p>
<p align="center">After that, you will see this screen as mine.<br>Installation completed, Docker successfully started.</p>
<br>

<br><br>

---

<br><br>

## Section 3: Download Docker Image of Our Project

<br><br>


<p align="center">When the Docker is started, pull up the terminal again.<br>
  Make sure you are on the same cloned (your working) directory.<br>
  This time, do the command `docker compose build`.<br>
  This will download all of the components and dependencies needed to work on our project.<br>
  It will take some time, expect 10 minutes minimum for a comparably fast laptop.<br>
  (Make sure you have enough time)<br>
  <br></p>

<p align="center">
  <br>
<img src="https://user-images.githubusercontent.com/113729242/222937542-d06f2067-aa10-462e-a61a-4de117ac47fa.png" width="700" height="400" />
<img src="https://user-images.githubusercontent.com/113729242/222937569-49381587-6cba-41db-8155-f73766e34021.png" width="700" height="400" /><img src="https://user-images.githubusercontent.com/113729242/222937588-3db32124-a181-4958-a957-328ffe71eb5b.png" width="700" height="400" /></p>
<p align="center">You have successfully done setting up Docker, and working on our project.</p>
<br>

<br><br>

---

<br><br>

## Section 4: Understanding Docker

<br><br>
Before working on the project, you might have wondered what it was all about<br>
when you were following `Installing Docker`, `Starting Docker` or, `Downloading Docker Image`,<br>
If it was your first time hearing Docker.
<ins>[[I have enough knowledge on Docker, I can skip this part.](#section-5-start-working-with-docker)]</ins>
<br><br>
<ins>We recommend you to take time understanding Docker</ins><br>otherwise, it must be hard to understand why we run Docker everytime.<br>
We have a <ins>[[Wiki Page](https://github.com/NeRF-or-Nothing/vidtonerf/wiki/Understanding-Docker)]</ins> in our project page for understanding Docker, that you can ask questions about Docker Desktop.<br>You can also read through other questions to understand what you might be missing as well.<br>Making this page active help other newcomers as well, please don't hesitate to put any questions on Docker.<br>

<br>

> <br>
> 
> **`Short introduction on What is Docker:`**
> 
> (Docker is a tool that lets you package your application and all of its dependencies,<br> including all the necessary components to run an  application, including code, libraries, and system tools,<br>into a single, portable container that you can develop and deploy easily ... )<br><br>  Think of it like a **shipping container** that you can easily move from one place to another. For us in this case, is our application.<br> See  that boxed application as an `image`. This a delivery package that can be shipped to anywhere<br>(that image can be shipped to any computer, whatever dependencies they might have).<br>If we had to download each of the dependencies separately getting issues within the installation process for each,<br>after Docker, now all of the dependencies are in the 'image' and Docker runs them for us. <br>That for us, Docker creates a unified devlopment environment that is consistent across all of our developer's machines.<br><br>
> <ins>[[the official Docker guide](https://docs.docker.com/get-started/overview/)]</ins> | <ins>[[official Docker Manual](https://docs.docker.com/desktop/)]</ins><br>
> <br>

<br>

If you prefer searching on Youtube over reading lengthy documents,<br>
check on these videos based on your preferences or time you have.<br>
> <ins>[[What is Docker? Easy way](https://www.youtube.com/watch?v=-LeV_c1zG-s)]</ins> | <ins>[[Image Guide on What is Docker](https://www.youtube.com/watch?v=wi-MGFhrad0)]</ins> | <ins>[[Beginner Course (1 hour)](https://www.youtube.com/watch?v=pg19Z8LL06w)}</ins> | <ins>[[Complete Course (3 hours)](https://www.youtube.com/watch?v=3c-iBn73dDE)]</ins>




<br><br><br>

---

<br><br>

## Section 5: Start Working with Docker

<br><br>

> **`Base Knowledge:`**<br><br>
> With the command `docker compose up`,<br>
> a container for each process: web-server, sfm-worker, rabbitmq, and mongodb was installed.<br>
> One was for the web-server, <br>one was for the sfm-worker,<br> 
> another was for the RabbitMQ our scheduling serice, <br>and the other was for MongoDB our database.<br><br>
> **web-server and sfm-worker is our code** and the other two are dependencies we rely on.<br><br>
> The directory of the web-server is the web-server <br>and the directory of the sfm worker is the colmap folder.<br>
> Basically, sfm-worker is all the code in the colmap folder which is for figuring out where the user camera was.<br><br>
> Each time when the web-server and sfm-worker are started (run),<br>
> they copy their directories (source code) into the containers and run `python main.py`.<br>
> Pretty much the containers with our code just auto run `main` every time they are started.<br><br>
> Since we are commiting and pushing our work to Github, when each time these source codes are run,<br>
> we get to run our application updated with the newly pushed work up to just before we started running.<br>
> On top of this, the volumes are shared between the host machine and the docker container<br> 
> meaning anything saved in the web-server container will also be saved in the web-server directory.<br>
> These containers are built to just toally mirror the host machine.<br>
> So, you can work on it as you did on your local machine not worrying about handling dependencies.

<br><br><br>

---

<br>
