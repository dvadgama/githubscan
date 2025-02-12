[![CircleCI](https://circleci.com/gh/uktrade/githubscan/tree/master.svg?style=svg)](https://circleci.com/gh/uktrade/githubscan/tree/master)

# Github Vulnerabilities Reporter

### Purpose
---
Purpose of this project is to scan all organisation repository and, report them to interested teams/individuals on following platforms

 - Gecko board
 - Email(s)
 - Slack

<br>

---
#### **Prerequisites**
---
- Enable Graph dependency in github
- Enable Aleters in github
- Access to
  - GOV.UK Notify for Email alers
  - Gecko board for publishing gecko reports
  - SLACK to publish report in chosen slack channel

<br>

---
### GOV.UK Notify
---

Got to https://www.notifications.service.gov.uk/register where an account can be
created in order to test sending notification emails. You will need to create
two email templates

<br>

---
### Production Environment Setup ( Cloud Foundry environment )
---
You need to set up following variables , apart from the default setup.

```bash
DJANGO_SECRET_KEY=<Secret Key>
GITHUB_LOGIN=<GitHub Login>
GITHUB_AUTH_TOKEN=<GitHub Auth Token>

SLACK_URL=<Slack Post Message Url>
SLACK_AUTH_TOKEN=<Slack Auth Token>
SLACK_CHANNEL=<Slack Channel Code>

GECKO_BOARD_TOKEN=<Gecko Board Token>

GOV_NOTIFY_API_KEY=<GOV.UK Notify Prod API Key>
GOV_NOTIFY_SUMMARY_REPORT_TEMPLATE_ID=<GOV.UK Template ID>
GOV_NOTIFY_DETAILED_REPORT_TEMPLATE_ID=<GOV.UK Template ID>

EMAIL_SIGNAURE=<Email Signature>

AUTHBROKER_CLIENT_ID=<OAuth Client ID>
AUTHBROKER_CLIENT_SECRET=<OAuth Client Secret>

```

<br>

---
## User Commands ( for production environment)
---
<br>

Update vulnerabilities information
```bash
$python manage.py refresh_vulnerability_data
```

Push updates to Gecko board
```bash
$python manage.py dispatch_gecko_reports
```

Dispatch Email reports.
```bash
$python manage.py dispatch_email_reports
```

Dispatch Slack report.
```bash
$python manage.py dispatch_slack_report
```
---
<br>

### **Web End Points**
In order to be able to execute commands using PaaS task runner one, need to have a web end points since,task runner container can not access application hosts file system, it would not have access to report files

Please be aware endpoints listed below are disabled by default. To enable 'em you need to set

```bash
ENABLE_REPORT_ENDPOINT = True
ALLOWED_REPORT_ENDPOINT_HOST = <your.internal.domain>
```

Please ensure your internal domain is as sequre as possible and could not be access by anything but just host running this app

 - Update Vulnerability Information ```common/refresh_vulneranility_data```
 - Push updates to Gecko Board ```common/dispatch_gecko_reports```
 - Dispatch Email reports ```common/dispatch_email_reports```
 - Dispatch Slack report ```common/dispatch_slack_report```


## Setup Dev environment (non-Cloud Foundry environments)
---
#### **Pre-requisites**

if you are going to use the non-virtualised environment , you need following tools installed

- ```pip install pip-tools pre-commit```
- ```pre-commit install```
-  postgres database


 If you are going to use docker environment all you need is a  ```docker-compose```

<br>

#### **Without Docker**


1) install dev dependencies

    ```bash
    $pip install -r requirements-dev.txt
    ```

2) *if you were to add your own dependencies do not forget to compile it with*
    ```bash
    $pip-compile requirements-dev.in
    ```

3) Create a database instance and user:
    ```bash
    $sudo su - postgres
    postgres $createdb githubdb
    postgres $psql -c "CREATE USER <username> SUPERUSER PASSWORD '<password>';"
    ```

    Make a note of the `<username>` and `<password>` for use in the `DATABASE_URL` environment variable.

    You may also wish to import from a dump of an existing development database, if you do so , remember to flush the email data or you would end up spamming everyone with your test emails

    ```bash
    $sudo su - postgres
    postgres $psql -d githubdb -f /tmp/githubscan-db-dump.sql
    ```
6) set environment variables in .env file
    ```bash
    DEPLOYMENT_ENVIRONMENT='dev'
    DJANGO_DEBUG='True'
    DJANGO_RESTRICT_ADMIN='False'
    DJANGO_DEBUG_LEVEL='DEBUG'
    DJANGO_SECRET_KEY=<Django Secret key>

    DATABASE_URL=<Database URL>

    GITHUB_LOGIN=<GitHubLogin>
    GITHUB_AUTH_TOKEN=<GithubAuthToken>
    GITHUB_TEAMS_ARE_NOT_A_SSO_TARGET=<list of teams not part of sso target i.e. users of those team will not receive an automatic vulnerability report>
    SLACK_URL=<Slack Post Message Url>
    SLACK_AUTH_TOKEN=<Slack Test Auth Token>
    SLACK_CHANNEL=<Slack Test Channel Code>

    GECKO_BOARD_TOKEN=<Gecko Board Token>

    GOV_NOTIFY_API_KEY=<GOV.UK Prod Key>
    GOV_NOTIFY_FAKE_TEST_API_KEY=<GOV.UK Test API Key>
    GOV_NOTIFY_REAL_TEST_API_KEY=<GOV.UK Test With Guest List>
    EMAIL_SIGNAURE=<Test Signature>

    GOV_NOTIFY_SUMMARY_REPORT_TEMPLATE_ID=<GOV.UK Template ID>
    GOV_NOTIFY_DETAILED_REPORT_TEMPLATE_ID=<GOV.UK Template ID>

    ENABLE_SSO=False
    ```

    for postgres db named ```githubdb``` on local  development environment DATABASE_URL should be set to ```postgres://127.0.0.1/githubdb```

5) Ensure all database migrations have been applied:

    ```bash
    $python manage.py migrate
    ```

<br>


#### **With Docker**


1) Create environment variables as suggested in section above

2) run ```docker-compose up```. For first time it will take a little longer to install dependencies, however subsequent
 Run should be much faster until you remove the container for any given reason.

<br>


#### **Superuser account**


Once a local database instance is configured, create a user with superuser
privileges:

before you create super user, make sure you  ``` set ENABLE_SSO=False in .env ``` ( docker already takes care of this ,however it would not hurt to do it anyway)

```bash
$python manage.py createsuperuser
```

It should now be possible to navigate to the admin site (http://localhost:8000/admin/)

<br>


#### **Development Commands**

These commands are here to simply help you test one featire at a time and, you can use them as needed instead of running combined/batched commands for production environment

- Download fresh vulnerability data from github

    ```bash
    $python manage.py refresh_scan
    ```

- Process downloaded data and add reporting elemnts to it

    ```bash
    $python manage.py refresh_processed_information
    ```

- Dispatch Organisation summary email
    ```bash
    $python manage.py dispatch_organization_email
    ```

 - Dispatch Teams summary email
   ```bash
    $python manage.py dispatch_team_email
    ```

- Dispatch Teams detailed email
    ```bash
    $python manage.py dispatch_team_detailed_email
    ```

- Dispatch Slack report
    ```bash
    $python manage.py dispatch_to_slack
    ```

- Dispatch Gecko Organisation level report
    ```bash
    $python manage.py dispatch_organization_gecko_report
    ```

- Dispatch Gecko Team level report(s)
    ```bash
    $python manage.py dispatch_teams_gecko_report
    ```

<br>

---
### Testing
---

#### **At glance**

 - Both github scanner and report data are validated against schema
 - Reporting functionalities are tested with mock data, you can look at the  file [mock_test_data.py](report/tests/mock_test_data.py) to see how mock data are generated
 - tests are configured in following manner
   - when DEPLOYMENT_ENVIRONMENT is set to any thing but 'prod' a set of mock tests executes which does not need access to any secrets executes, which is what we aim to run in CI ( circleci )
   - when DEPLOYMENT_ENVIRONMENT is set to 'real_fast_test' it does need access to some secrets such as slack and GOV.UK Notify auth tokens for test environment, we can use this most times , however we don't need to
   - when DEPLOYMENT_ENVIRONMENT is set to 'real_test' it executes every test including the slower tests , specifically one testing scanner integration and unit testing with production token, use this with caution only when you want to test end to end results, which normally involves modifying scanner source code
- We can certainly add more of Integration testing with real and mock data

<br>

#### **Running Tests**


```bash
pytest
```

<br>

#### **Known issues**
- At the moment team_repositories.query.graphql is not optimum enough and, if we try to execute all of scanner test ( with DEPLOYMENT_ENVIRONMENT set to real_test ). It may result in exhausting hourly limits, i would suggest not to set  DEPLOYMENT_ENVIRONMENT to 'real_test' until we resolve issue.

<br>

---
### Things You should know ( as a Contributor/Developer )
---
 -  Django settings file will automatically read .env file in both Docker and Non-Virtualised environment
 - It sends following type email reports
    - Organization wide Summary report
    - Team specific Summary report
    - Team Specific detailed report
- It publishes following Gecko reports ( they are all datasets ) with top 20 repositories
    - Organisational overview
    - Per team overview report
- Slack report which goes to single selected channel

- The list of organisation wide and team wide email recipients is stored in database , to update this you will need to have access to admin view, which is normally protected by SSO ( unless you disable it )

- Reports are stored in files and can be set to use any name.
    - The raw data that we fetch from github is stored in ```.scanner_data.json``` file and, it can be changed/updated by setting variable ``SCANNER_DATA_FILE_NAME`` in ```.env`` file or in environment directly
    - The raw data is then processed to be in more report friendly form which is called ```.processed_data.json``` and can be updated/changed by setting variable ```PROCESSED_DATA_FILE_PATH``` in ```.env``` file or in environment directly


- [ full list of environment variables ](all_vars.env)
- [ mimum variables to get started ](sample.env)

- To understand scannder data collection flow look at [scanner.py](scanner/scanner.py)
- To under stand how report data is processsed and, what reports are dispatched you can start with [report.py](report/report.py)

<br>

---
Key features
----
 - configrable Severity escalation  time in working days
 - considers UK public holidays and weekends while calculating severity escalation
 - configurable email recipients
 - if desired, we can disable team from receiving any emails, this is useful feature in an event when you have team X than , team X-Admin in github both managing same set of repositories however only few are Admin and they will receive a duplicate email if emailing capacity was assigned to both Team X and Team X-Admin
- if desired, certain end users can be configured to have only red alerts, this is a useful feature if email is received by a specfic group which only takes care of high priority events
