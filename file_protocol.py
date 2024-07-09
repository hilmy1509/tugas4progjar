import json
import logging
import shlex
import base64
from file_interface import FileInterface

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def proses_string(self, string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk}")
        c = shlex.split(string_datamasuk.lower())
        try:
            c_request = c[0].strip()
            logging.warning(f"memproses request: {c_request}")
            params = [x for x in c[1:]]
            if c_request == 'upload':
                filename = params[0]
                filecontent = params[1]
                return self.upload_file(filename, filecontent)
            elif c_request == 'delete':
                filename = params[0]
                return self.delete_file(filename)
            else:
                cl = getattr(self.file, c_request)(params)
                return json.dumps(cl)
        except Exception:
            return json.dumps(dict(status='ERROR', data='request tidak dikenali'))

    def upload_file(self, filename, filecontent):
        try:
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(filecontent))
            return json.dumps(dict(status='OK', data=f"{filename} uploaded successfully"))
        except Exception as e:
            return json.dumps(dict(status='ERROR', data=str(e)))

    def delete_file(self, filename):
        try:
            os.remove(filename)
            return json.dumps(dict(status='OK', data=f"{filename} deleted successfully"))
        except Exception as e:
            return json.dumps(dict(status='ERROR', data=str(e)))

if __name__ == '__main__':
    # contoh pemakaian
    fp = FileProtocol()
    print(fp.proses_string("LIST"))
    print(fp.proses_string("GET pokijan.jpg"))
    # contoh upload file dengan konten yang diencode base64
    file_content_base64 = base64.b64encode(open("pokijan.jpg", "rb").read()).decode('utf-8')
    print(fp.proses_string(f"UPLOAD pokijan.jpg {file_content_base64}"))
    print(fp.proses_string("DELETE pokijan.jpg"))
