# OpenChatDoc - opensource flask gpt boillerplate for talking with your documents


[![GitHub Repo stars](https://img.shields.io/github/stars/johnsmithm/openchatdoc?style=social)](https://github.com/johnsmithm/openchatdoc)
[![Twitter Follow](https://img.shields.io/twitter/follow/ionmosnoi?style=social)](https://twitter.com/ionmosnoi)

## Key Features 🎯

- **OpenChatDoc**: OpenChatDoc is a versatile open-source project for file management and conversation using Flask framework.
- **Simple UI**: The user interface of OpenChatDoc is designed to be straightforward and user-friendly.
- **OpenAI Integration**: OpenChatDoc harnesses the power of OpenAI to facilitate intelligent conversations and information retrieval.
- **Local Embeddings Storage**: OpenChatDoc utilizes the FAISS library to store embeddings locally, enabling efficient search and retrieval of data.
- **File Upload Support**: OpenChatDoc allows users to upload various file formats, including docx, doc, pdf, and txt files.
- **Multi-File Interactions**: OpenChatDoc supports conversations and interactions with multiple files simultaneously.

## Demo Highlights 🎥

https://github.com/johnsmithm/openchatdoc/assets/10476109/89e237ce-f206-4514-9338-3f5cefda47fe

## Connect with me

[linkedin]: https://img.shields.io/static/v1?label=&message=LinkedIn&&color=3B3B7A&logo=linkedin
[devdotto]: https://img.shields.io/static/v1?label=&message=Blog&color=3B3B7A&logo=devdotto
[telegram]: https://img.shields.io/static/v1?label=&message=Telegram&&color=3B3B7A&logo=telegram
[twitter]: https://img.shields.io/static/v1?label=&message=Twitter&&color=3B3B7A&logo=twitter

[![twitter]](https://twitter.com/ionmosnoi)
[![linkedin]](https://www.linkedin.com/in/ionmosnoi/)
[![telegram]](https://t.me/ionmosnoi/)

## How to Use OpenChatDoc 🚀

1. Clone the OpenChatDoc repository:
```
git clone https://github.com/johnsmithm/openchatdoc.git
```

2. Install the required dependencies using pip:
```
pip install -r requirements.txt
```

3. set env variable :
```
copy .env_example .env
OPENAI_API_KEY="sk-.."
```

4. Start the Flask server:
```
python app.py 5000
```

5. Access OpenChatDoc in your web browser at `http://localhost:5000`.

Note: Please ensure that you have Python and Flask installed on your system before running OpenChatDoc.

## Contributing 🤝

Contributions to OpenChatDoc are welcome! Here are a few ways you can contribute:
- Bug fixes and issue resolution
- Feature enhancements
- Documentation improvements
- Writing and optimizing tests

This project is built by amazing volunteers and you can be one of them! Here's a list of ways in [which you can contribute to this project](CONTRIBUTING.md).

If you want to make any change to this repository, please **make a fork first**.

If you see something that doesn't quite work the way you expect it to, open an Issue. Make sure to describe what you _expect to happen_ and _what is actually happening_ in detail.

If you would like to suggest new functionality, open an Issue and mark it as a __[Feature request]__. Please be specific about why you think this functionality will be of use. If you can, please include some visual description of what you would like the UI to look like, if you are suggesting new UI elements. 

Make sure the code format is ok 
```bash
pylint $(git ls-files '*.py')
```

## Built With

Flask

### Programming languages

Python 3.8.1

### Run & Development
#### Docker
Docker is used to run the development version, so you'll need to install [Docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/).

In case you are using WSL with Docker for Desktop (version 2.2.0.4) on Windows: you need to have your repository on the Windows file system rather than on the WSL one because otherwise the volume won't be mounted (solution inspired from this work around: https://github.com/docker/for-win/issues/2151#issuecomment-402163189)

```bash
sudo docker build -t chatfile:1 -f Dockerfile .
sudo docker run -it -d  -p 6017:6017 -v "$(pwd)":/app --name chatfile_ chatfile:1
sudo docker exec -ti chatfile_ bash
python app.py 6017
```
go to localhost 6017


#### Pycharm
To run the application using Pycharm you need to install MongoDB Community Edition following steps from [documentation](https://docs.mongodb.com/manual/installation/).
Steps below work for all OS where Pycharm is available.
1. Install pycharm community edition
2. Open the project in pycharm
3. Open terminal from pycharm Alt+F12 or View -> Tool Windows -> Terminal
4. Install pipenv from terminal if it's not installed yet:
    ```
    $ pip install pipenv
    ```
5. Install dependencies from Pipfile
    ```
    $ pipenv install
    ```
6. Add new configuration for python:
Run -> Edit Configurations... -> + -> Python
7. Change option "Script Path" to "Module Name"
8. Enter "flask" in input for "Module Name"
9. Enter **run** in input "Parameters"
10. Open and add new Environment variables:
    - OPENAI_API_KEY="sk-.."
10. Press Ok
11. To init databases execute command in terminal from Pycharm

## Feedback

* Request a new feature on GitHub.
* Vote for popular feature requests.
* File a bug in GitHub Issues.
* Email us with other feedback moshnoi2000[at]gmail.com

## License

This project is licensed under the MPL 2.0 License - see the [LICENSE](LICENSE) file for details



