
# Welcome to your CDK Python project!

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## How to run this
 * Configure your [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
 * Go to [app.py](app.py) and set your account number
 * `cdk deploy <STACK> -c version=<VERSION> -c graphs=<GRAPHS>`
deploy this stack to your default AWS account/region. 
   * Valid values for STACK
     * MonolithStack
     * MicroservicesStack
   * Valid values for VERSION
     * java
     * dotnet
     * cpp
   * Valid values for GRAPHS
     * big-dense
     * big-sparse
     * small-dense
     * small-sparse
 * At the end of the output you will see a link
 * Use it with port `8001` to connect to the app
   
## Remember to destroy your stacks when you're not using them!
  `cdk destroy stack <STACK> -c version=<VERSION> -c graphs=<GRAPHS>` - will save you a lot of money
  

## How to add a new config?

* Go to your config file in [configs](cdk/configs) directory and fill the function
  * You need to create all of your microservices containers
  * You need to create links between your containers
  * You can base on Java config
* Go to [architecture_factory](cdk/factories/architecture_factory.py) file and fill path to your monolith image
* Go to [listener_factory](cdk/factories/listener_factory.py) file and fill name of
  * Api gateway container in _create_microservices_listener_ function
  * Monolith container in _create_monolith_listener_ function