# Open Netra Dashboard (Backend)

Open Netra is a platform ...

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Beforehand, you **MUST** know these prerequisites installation could be different depend on your local machine OS types (Windows/MAC/Linux). **BUT** it does not really matter, you could use many tutorials out there on the internet to help you install these prerequisites.

First things need to be installed on your local machine:
1. Python
2. Git
3. Text Editor (e.g., Visual Studio Code, Atom, Sublime, etc.)


### Installing

Step by step series of how to get a development env running

#### A. Clone Project Repository Into Local Machine
1. Specify the PATH where you want to locate the project repository, for example:
> D:\AN_OPEN_NETRA
2. Open the PATH using command prompt/terminal/Git bash.
> It is the easy one, I will not explain to you on how to do it, please do it yourself.
3. Cloning project repository into your machine with the following command:
```
git clone https://github.com/praszxc/AN_OPEN_NETRA_BE.git
```
> Once it is done, project repository is cloned at the following PATH: 
> 
> D:\AN_OPEN_NETRA\AN_OPEN_NETRA_BE

#### B. Setup Virtual Environment
1. Install python virtual environment on your machine by opening command prompt/terminal and run the following command:
```
pip install virtualenv
```
2. Create a virtual environment inside the project directory.
> On your command prompt/terminal, point to the PATH where project directory located (in this case "D:\AN_OPEN_NETRA\AN_OPEN_NETRA_BE") and run the following command:
```
python -m venv env
```
3. Before getting ready to operate with the project, don't forget to **ALWAYS** activate the virtual environment. 
> (*You could do this using your Text Editor terminal instead, rather using your machine's command prompt/terminal*).
4. So, open project directory using your Text Editor you have installed, then open a new terminal inside it. Lastly activate the virtual environment using the following command:
> Activate on Windows:
```
source env/Scripts/activate
```
> Activate on Mac/Linux:
```
source env/bin/activate
```
> Deactivate on Windows/Mac/Linux:
```
deactivate
```
#### C. Project Setup
1. Inside project directory, you will see a file named *requirements.txt*, you need this file to install dependencies needed by the project. On the Text Editor terminal, run the following command:
```
pip install -r requirements.txt
```
> Once all the requirements already installed, you need to check whether the project could run on your local machine or not by running the project 
2. Run the project
```
python manage.py runserver
```

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Django](https://www.djangoproject.com/) - Web framework used
* [Django REST Framework (DRF)](https://maven.apache.org/) - Web APIs toolkit
* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) - Provides a JSON Web Token authentication backend for the Django REST Framework. 
* [Kubernetes Python Client](https://github.com/kubernetes-client/python) - Official Python client library for kubernetes.

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Bagus Dwi Prasetyo** - *Initial work* - [praszxc](https://github.com/praszxc)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

