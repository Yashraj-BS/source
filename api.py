import os
import os.path
from github import Github
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth, ServiceAccountCredentials

class GoogleDriveAPI:
    def __init__(self, service_account_json):
        self.gauth = GoogleAuth()
        self.service_account_json = service_account_json
        self.scope = ["https://www.googleapis.com/auth/drive"]
        self.folder_id = None

    def authenticate(self):
        self.gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.service_account_json, self.scope
        )
        return self.gauth

    def get_drive(self):
        self.authenticate()
        return GoogleDrive(self.gauth)

    def create_folder(self, folder_name, drive):
        folder_metadata = {
            "title": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        self.folder_id = folder["id"]
        return self.folder_id

    def upload_file_to_drive(self, local_file_path, folder_name):
        drive = self.get_drive()
        self.authenticate()

        folder_id = None
        folder_list = drive.ListFile(
            {
                "q": "title='"
                + folder_name
                + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            }
        ).GetList()
        if folder_list:
            folder_id = folder_list[0]["id"]
        else:
            folder_id = self.create_folder(folder_name, drive)

        # Upload the file to the folder
        file = drive.CreateFile(
            {"title": os.path.basename(local_file_path), "parents": [{"id": folder_id}]}
        )
        file.SetContentFile(local_file_path)
        try:
            file.Upload()
            return "Uploaded"
        except Exception as e:
            return f"Error on Upload: {str(e)}"


"""if __name__ == "__main__":
    service_account_json = '/path/to/your/service_account.json'
    local_file_path = '/path/to/your/local/file'
    folder_name = 'Folder name'
    
    uploader = GoogleDriveUploader(service_account_json)
    result = uploader.upload_file_to_drive(local_file_path, folder_name)
    print(result)"""


class GitHubAPI:
    """
    This class provides an interface to interact with the GitHub API.
    """

    TOKEN = os.getenv("TOKEN")

    def __init__(self):
        """
        Initialize the GitHub API client.

        Args:
            None

        Returns:
            None
        """
        self.branch = "main"
        self.repo_name = "ybs-data"
        self.repo_owner = "Yashraj-BS"
        self.g = Github(GitHubAPI.TOKEN)
        self.repo = self.g.get_repo(f"{self.repo_owner}/{self.repo_name}")

    def create(self, file_path: str, file_content: str):
        """
        Create a new file in the GitHub repository.

        Args:
            file_path (str): The path of the file to create, including the file name.
            file_content (str): The content of the file to create.

        Returns:
            None
        """
        try:
            self.repo.create_file(
                file_path, "Creating file", file_content, branch=self.branch
            )
            print(f"File '{file_path}' created successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def update(self, file_path: str, new_content: str):
        """
        Update an existing file in the GitHub repository.

        Args:
            file_path (str): The path of the file to update, including the file name.
            new_content (str): The new content of the file.

        Returns:
            bool: True if the file was updated, False otherwise.
        """
        try:
            file_content = self.repo.get_contents(file_path, ref=self.branch)
            self.repo.update_file(
                file_path,
                "Updating file",
                new_content,
                file_content.sha,
                branch=self.branch,
            )
            return True
        except Exception as e:
            return False
        
    def delete(self, file_path: str):
        """
        Delete a file from the GitHub repository.

        Args:
            file_path (str): The path of the file to delete, including the file name.

        Returns:
            None
        """
        try:
            file_content = self.repo.get_contents(file_path, ref=self.branch)
            self.repo.delete_file(
                file_path,
                "Deleting file",
                file_content.sha,
                branch=self.branch,
            )
            print(f"File '{file_path}' deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def isexist(self, path: str):
        """
        Check if a file exists in the GitHub repository.

        Args:
            path (str): The path of the file, including the file name.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        try:
            self.repo.get_contents(path, ref=self.branch)
            return True
        except Exception as e:
            return False

    def list(self, filepath: str = ""):
        """
        List the files in the GitHub repository.

        Args:
            filepath (str): The path of the directory to list, including the directory name.

        Returns:
            list: A list of file names.
        """
        try:
            contents = self.repo.get_contents(filepath)
            files = [file.name for file in contents if file.type == "file"]
            return files
        except Exception as e:
            print(f"An error occurred: {e}")

    def read(self, file_path: str):
        """
        Read the content of a file from the GitHub repository.

        Args:
            file_path (str): The path of the file, including the file name.

        Returns:
            str: The content of the file.
        """
        try:
            file_content = self.repo.get_contents(file_path)
            return file_content.decoded_content.decode()
        except Exception as e:
            print(f"An error occurred: {e}")


git = GitHubAPI()
#git.create("LR.txt", "Tanmay BehenkaLoda")
#git.isexist("test_file.txt")
#print(git.read("README.md"))
print(git.list())

from datetime import datetime

# Get the current date
current_date = datetime.now()

# Format the date
formatted_date = current_date.strftime("%b, %Y")

print(formatted_date)

