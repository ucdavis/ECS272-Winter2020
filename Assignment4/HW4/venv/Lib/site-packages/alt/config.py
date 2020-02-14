import yaml
import os


class AbsoluteConfigFactory(object):
    def __init__(self, *secret_files, keep_secrets=False):
        data = ""
        for file in secret_files:
            with open(file, 'r') as fin:
                    data += fin.read() + '\n'
        self.secrets = data
        loaded = yaml.load(data)
        self.secret_keys = [] if keep_secrets or loaded is None else loaded.keys()

    def get(self, file):
        if not hasattr(self, file):
            with open(file, 'r') as fin:
                data = fin.read()
            decoded_yaml = yaml.load(self.secrets + data)
            for key in self.secret_keys:
                decoded_yaml.pop(key, None)
            setattr(self, file, decoded_yaml)
        return getattr(self, file)


class ConfigFactory(AbsoluteConfigFactory):
    def __init__(self, basedir, *secret_files, keep_secrets=False, secrets_absolute_path=False):
        self.basedir = basedir
        if not secrets_absolute_path:
            secret_files = [self.format_path(file) for file in secret_files]
        super().__init__(*secret_files, keep_secrets=keep_secrets)

    def get(self, file):
        file = self.format_path(file)
        return super().get(file)

    def format_path(self, file):
        return os.path.join(self.basedir, file if os.path.splitext(file)[1] is not '' else os.path.splitext(file)[0] + ".yaml")