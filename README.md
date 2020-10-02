# Introduction
FastAPI + JWT + SQLAlchemy + SQLite(or MS SQL Server) demo.
The code follows the official document of [FastAPI OAuth2 JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/).


# Getting Started
1. View the automatically generated OpenAPI docs deployed on Azure: 
https://referral-web-app.azurewebsites.net/docs
2. If running the app for the first time, the *users* table in the database is empty. To be able to login and use the API, you can send a **POST** request to endpoint:
 https://referral-web-app.azurewebsites.net/auth/users/init with an empty body. This will create the default superuser defined in *./configurations.py*.


# Run Locally
1. Clone the repo
    ```bash
    $ git clone https://github.com/juveseason/fastapi-jwt.git
    ```
2. Create virtual env and activate
    ```bash
    $ cd fastapi-jwt-orm
    $ python -m venv .venv
    $ .venv\Scripts\activate
    ```
3. Install python packages in requirements.txt
    ```bash
    (venv) $ pip install -r requirements.txt
    ```
4. Set environment variable
    ```bash
    (venv) $ set ENV=LOCAL
    ```
5. Start FastAPI app locally
    ```bash
    (venv) $ uvicorn main:app --reload
    ```

# Use MS SQL Server (Optional)
 If you want to use MS SQL Server as the local database for the app:
 1. Install [SQL Server Express LocalDB](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/sql-server-express-localdb?view=sql-server-ver15).
 2. Create a database, named as "renewal_app" for example.
 3. Set the connection string **SQLSERVER_DATABASE_URL** in *./configuration.py*.
 4. In *utils/database.py*, comment out the SQLite engine line, and uncomment the MS SQL Server engine line. 
 5. Run the app using the same instructions in the previous section.
 6. No other code change required. This is also the benefit of using an ORM, it is a high level abstraction and decoupls the database details in code base.


# Test
FastAPI has a built-in **TestClient** class which is based on *pytest* and *requests*, this makes it very easy to write tests.
To run all test cases: 
```bash
(venv) $ pytest
```
This will create a test database named *fastapi_app_test.db* at the beginning of the test, run all test cases, then remove the database file after finishing the last test case. 


# Configurations for Deployment on Azure App Service
1. In Configuration -> Application Settings, create environment variable name "ENV", set value to "PROD".
2. To start the app server, We could use uvicorn directly. In Configuration -> General settings -> Startup Command:
`python -m uvicorn main:app --host 0.0.0.0`
3. But according to [uvicorn doc](https://www.uvicorn.org/#running-with-gunicorn), for production deployment, we should use **gunicorn with the uvicorn worker class**:
`gunicorn -b=0.0.0.0 -t 600 -k uvicorn.workers.UvicornWorker main:app`

# SQLite Issue on Azure App Service (Advanced)
1. The file system on App Service /home path is CIFS, it is a Network File Share (NFS) type. SQLite is a file based database and doesn't support writing on NFS. See this [article](https://daniellethurow.com/blog/2020/4/21/azure-app-services-and-sqllite3) for more information.
2. To workaround the problem and also to demo repeated task, I used a third-party libary [fastapi-utils](https://fastapi-utils.davidmontague.xyz/) with app *startup* event.
3. I use two kinds of file systems available in App Service
   - /mnt: Azure File Share mounted to the app, persistent, but does not support SQLite.
   - /tmp: Linux VM's temp folder, non-persistent, content will be lost after app reboot, but file system supports SQLite.
4. The idea is to find a way to automatically backup and restore the database file, see details in *routers/sched.py*.
5. Restore: On app *startup* event, copy database file from /mnt to /tmp.
6. Backup: repeating every minute, copy database file from /tmp to /mnt.
