from pathlib import Path
from glob import glob


class Preprocess:

    def __init__(self, project_path, subject_name, session_name):
        self.proj_path = project_path
        self.sub_name = subject_name
        self.ses_name = session_name

        self.pre_path = Path(self.proj_path) / self.sub_name / self.ses_name / 'Preprocess'

    def get_files(self, filename: str, dir_name: str = None):
        if dir_name is not None:
            path = self.pre_path / dir_name
        else:
            path = self.pre_path
        files = glob(str(path / filename))
        return files
