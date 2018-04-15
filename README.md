# CL Scholar Portal

We present _CL Scholar_, the ACL Anthology knowledge graph miner to facilitate high-quality search and exploration of current research progress in the computational linguistics community. In contrast to previous works, periodically crawling, indexing and processing of new incoming articles is completely automated in the current system. _CL Scholar_ utilizes both textual and network information for knowledge graph construction. 

As an additional novel initiative, _CL Scholar_ supports more than 1200 scholarly natural language queries along with standard keyword-based search on constructed knowledge graph. It answers _binary_, _statistical_ and _list_ based natural language queries. 

The current system is deployed at [http://cnerg.iitkgp.ac.in/aclakg](http://cnerg.iitkgp.ac.in/aclakg). We also provide REST API support along with bulk download facility. To know more checkout http://cnerg.iitkgp.ac.in/aclakg/api/

### Tech

CL Scholar uses a number of open source projects to work properly:

* [React JS](https://reactjs.org/) - JS framework for web apps!
* [node.js](https://nodejs.org/) - evented I/O for the backend
* [Twitter Bootstrap](http://twitter.github.com/bootstrap/) - great UI boilerplate for modern web apps
* [Express](http://expressjs.com/) - fast node.js network app framework
* [ReCharts](http://recharts.org/en-US/) - the streaming build system


## Requirements for Development

- `node`
- `npm`

## Setup for Development

The whole pipeline is as follow - 
`MongoDB Database  --> NodeJS API Server --> React Frontend`

In order to install the website and frontend part

- `git clone https://github.com/CLScholar/CL-Scholar-Client.git`
- `cd CL-Scholar-Client`
- `npm install`
- `npm start`

### Customizing Your Development Environment

In order to install the full pipeline

Set up the database

1. Download all the data from https://github.com/CLScholar/data
2. Install `MongoDB` server
3. Create a database with name `acl`
4. Create `authors`, `papers` and `conferences` collections and import the downloaded data.

Set up the API server

- Install `python 3.5`
- `pip install nltk`
- `git clone https://github.com/CLScholar/CL-Scholar-Client.git`
- `cd CL-Scholar-Client`
- `npm install`
- `npm start`
- Go to `CL-Scholar-Client/src/config.js` and edit `ACL_API` link.

License
----
MIT

