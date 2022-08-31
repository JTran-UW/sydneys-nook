# Sydney Lai Blog, Sydney's Nook
Blog and potential portfolio site for Sydney Lai

## Table of Contents

 - [Working with the code](#Working-with-the-code)
 - [Troubleshooting](#Troubleshooting)

## Working with the code

This project requires Python 3.5 or later.

First, in a terminal windodw, clone the repository and cd into it
```
https://github.com/ProfJAT/sydneys-nook.git
cd sydneys-nook
```

It is highly recommended that you use a virtual environment. In your project directory, enter the following for Linux.
```
python -m venv venv
source venv/bin/activate
```

For Windows, open a Powershell window, and run:
```
python -m venv venv
venv/Scripts/activate.ps1
```

Next, you need to set a couple environment variables: NOTION_SECRET, KANBAN_ID, MAIN_ID, and SECRET_KEY.

All of these can be found in the Python app cPanel dashboard. To locate it, start by entering cPanel from the Namecheap user dashboard.
![Screenshot_20220829_225951](https://user-images.githubusercontent.com/46096425/187361222-416e3b57-1934-4023-9997-c325ad117501.png)

From there, scroll to where you see the "Software" section and click "Setup Python App".
![Screenshot_20220829_230127](https://user-images.githubusercontent.com/46096425/187361436-ce579408-6f58-4136-8b5f-87a138cc57d1.png)

Select the edit icon on the sydneysnook.com app.
![Screenshot_20220829_230325](https://user-images.githubusercontent.com/46096425/187361594-67b8a474-1b49-4a83-a21d-2c98a82754de.png)

From there, scroll to the Environmental Variables section.
![Screenshot_20220829_230610](https://user-images.githubusercontent.com/46096425/187361980-20be9fa2-60b5-4c5a-ba50-a7d44f0ef7d5.png)

All environment variables shown, besides "DEPLOYMENT", should be set in your terminal with the command:
```
export VARIABLE_NAME='VARIABLE_VALUE'
```

From there, install necessary packages.
```
pip install -r requirements.txt
```

You are ready to run the development server!
```
python manage.py runserver
```

The site will be available at http://127.0.0.1:8000

Use typical git versioning but remember: due to our CI/CD pipeline, committing directly to main will change the website on the web!

## Troubleshooting

Problems could come from anywhere. However, there could be a few likely culprits.

### Uploaded images or static files throwing 404

If this is the case, the startup script may not be collecting static files properly.  Enter the cPanel dashboard, scroll down to the "Advanced" section, and select "Terminal"
![Screenshot_20220830_175815](https://user-images.githubusercontent.com/46096425/187569804-fbdc23b7-624c-427f-9ae4-dc5cbdc3d1c4.png)

In the terminal, run the below commands.
```
source /home/sydnpljf/virtualenv/sydnook_app/3.9/bin/activate && cd /home/sydnpljf/sydnook_app
python manage.py collectstatic
```

### Changes to settings.py or main site files cause breaking issues

Sometimes this could be remedied with a simple "turn it off and on again".  In the cPanel dashboard, scroll down to the "Software" section, and select "Setup Python App".
![Screenshot_20220830_180639](https://user-images.githubusercontent.com/46096425/187570562-4fb04279-3073-438f-893a-33ad3dc1d2cf.png)

Then, find the "sydneysnook.com" app, and click the restart icon.
![Screenshot_20220830_180823](https://user-images.githubusercontent.com/46096425/187570717-9f6dd37e-f431-49dc-9645-820a317ef4bb.png)
