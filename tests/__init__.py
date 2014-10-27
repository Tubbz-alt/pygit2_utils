# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import shutil
import sys
import tempfile
import unittest

import pygit2


GITCONFIG = """
[user]
  name = foo
  email = foo@bar.com
"""


class BaseTests(unittest.TestCase):
    """ Base class for the unit-tests of pygit2.utils. """

    def setUp(self):
        """ Method run before each tests. """

        self.path = tempfile.mkdtemp(prefix='rpkg-tests.')
        self.gitroot = os.path.join(self.path, 'gitroot')

    def tearDown(self):
        """ Method run after each tests. """

        shutil.rmtree(self.path)

    def setup_git_repo(self):
        """ Create a basic git repo withing the tests folder that can be used
        then for the tests.
        """

        # Create a bare git repo
        bare_repo_path = os.path.join(self.gitroot, 'test_repo.git')
        os.makedirs(bare_repo_path)
        pygit2.init_repository(bare_repo_path, bare=True)

        # Clone the bare git repo and add the elements we need in it
        git_repo_path = os.path.join(self.gitroot, 'test_repo')
        pygit2.clone_repository(bare_repo_path, git_repo_path, bare=False)

        repo = pygit2.Repository(git_repo_path)

        # Add basic files needed
        open(os.path.join(git_repo_path, '.gitignore'), 'w').close()
        repo.index.add('.gitignore')
        open(os.path.join(git_repo_path, 'sources'), 'w').close()
        repo.index.add('sources')
        repo.index.write()

        with open(os.path.join(git_repo_path, '.git', 'config'), 'a') as stream:
            stream.write(GITCONFIG)

        # Commits the files added
        tree = repo.index.write_tree()
        author = pygit2.Signature('Alice Author', 'alice@authors.tld')
        committer = pygit2.Signature('Cecil Committer', 'cecil@committers.tld')
        repo.create_commit(
            'refs/heads/master', # the name of the reference to update
            author,
            committer,
            'Add basic file required',
            tree, # binary string representing the tree object ID
            [] # list of binary strings representing parents of the new commit
        )

        # Push to the remote repo
        master_ref = repo.lookup_reference('HEAD').resolve()
        refname = '%s:%s' % (master_ref.name, master_ref.name)
        ori_remote = repo.remotes[0]
        ori_remote.push(refname)