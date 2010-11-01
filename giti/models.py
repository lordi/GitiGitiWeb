from git import Repo, Blob, BaseIndexEntry
import gitdb
from StringIO import StringIO

class Repository:
    git_repo = None

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __unicode__(self):
        return self.name

    def get_git_repo(self):
        if not self.git_repo:
            self.git_repo = Repo(self.path)
        return self.git_repo

    def index_store(self, path, data, mode):
        udata = data.encode("utf-8")
        istream = gitdb.IStream(Blob.type, len(udata), StringIO(udata))
        self.get_git_repo().odb.store(istream)
        entry = BaseIndexEntry((mode, istream.binsha, 0, path))
        #index.add([entry])
        #f = open(blob.abspath, 'w')
        #f.write(request.POST['data'].encode("utf-8"))
        #f.close()
        self.get_git_repo().index.add([entry])

    def index_delete(self, path):
        self.get_git_repo().index.remove([path])
