    def test_gitrepo(self):
        """ Test the pygit2_utils.GitRepo() constructor
        """

        repo_path = os.path.join(self.gitroot, 'test_repo')

        self.assertRaises(
            OSError,
            pygit2_utils.GitRepo,
            repo_path,

        )

        # Commit with a list of (one) file
        with open(os.path.join(repo_path, 'sources'), 'w') as stream:
            stream.write('\nBoo!!2')

        # Commit with a single file
        commitid = repo.commit('Commit from the tests', 'sources')

        # Check that the commitid returned has an .hex attribute that is a
        # string
        self.assertTrue(isinstance(commitid.hex, str))

        # Check the latest commit has the same hash as the commitid returned
        self.assertEqual(
            commitid.hex,
            repo_obj.revparse_single('HEAD').oid.hex
        )

        # Check the information of the latest commit
        commit = repo_obj.get(repo_obj.revparse_single('HEAD').oid.hex)

        self.assertEqual(commit.message, 'Commit from the tests')
        self.assertEqual(commit.author.name, 'foo')
        self.assertEqual(commit.author.email, 'foo@bar.com')
