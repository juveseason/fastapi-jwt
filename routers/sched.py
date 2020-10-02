# scheduled jobs

# https://daniellethurow.com/blog/2020/4/21/azure-app-services-and-sqllite3
# azure /home file system is cifs (Network File System), don't support sqlite db
# this is a workaround to backup the db file to /mnt every 1 min
# and restore it on app start

import os
import shutil

from fastapi import APIRouter
from fastapi_utils.tasks import repeat_every

router = APIRouter()


@router.on_event("startup")
def restore_sqlite_db() -> None:
    print("On app startup event...")
    if os.environ["ENV"] == "PROD":
        print("Restoring sqlite db file to /mnt/logstore")
        shutil.copyfile("/mnt/logstore/fastapi_app.db", "/tmp/fastapi_app.db")


# https://fastapi-utils.davidmontague.xyz/user-guide/repeated-tasks/
@router.on_event("startup")
@repeat_every(seconds=60)  # 1 min
def backup_sqlite_db() -> None:
    print("On scheduled job...")
    if os.environ["ENV"] == "PROD":
        print("Copying sqlite db file to /mnt/logstore")
        shutil.copyfile("/tmp/fastapi_app.db", "/mnt/logstore/fastapi_app.db")


@router.on_event("shutdown")
def backup_sqlite_db() -> None:
    print("On app shutdown event...")
    if os.environ["ENV"] == "PROD":
        print("Copying sqlite db file to /mnt/logstore")
        shutil.copyfile("/tmp/fastapi_app.db", "/mnt/logstore/fastapi_app.db")
