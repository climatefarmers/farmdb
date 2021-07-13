# Contributing

Conventions and best practices for contributing to this project.

## Python conventions

We adhere to standard ([PEP8][pep8]) python conventions for the most part.
Here we address a few grey areas and stylistic choices.

- quotes
  - use `'` for fixed constant strings
  - use `"` for modifiable and format strings
  - break this rule if needed to avoid escaping
    - e.g., `re.compile(r'say "hi"')`

- multiline component imports should be in parens, one component per line,
  alphabetical
  
    ```python
	from foo import (
		bar,
		bazzle,
		otherstuff,
	)
	```

- try to put class-specific constants inside class 
  - e.g., `Membership.MEMBER_TYPE_PATIENT`

- same for class-specific exceptions
  - e.g., `MetricDefinition.MetricMissingData`

- use `foo.pk is None` instead of `foo._state.adding` to test for insertion in
  pre-save hooks
  - this is not totally obvious in public convention, but we decided we don't
    like accessing vars that start with `_` if we can help it
  - avoid use of `# pylint: disable=protected-access`

- add tests for any use of variables which start with `_`
  - whenever we access a variable like django's `model._meta`, we should make
    sure we write a test case which covers the particular use case so that we
    are informed of any behavior changes

### Lint

We use `pylint` to check for clean code, with a few minor variations:

- names of django migrations don't conform to PEP8, so we ignore naming conventions for migration
  modules

- auto-generated migrations may have long lines, so we ignore line length requirements there


Because of the automatic checks, it is tempting to use the `# pylint: disable` directive.  Some
guidelines on when to use or avoid this directive follow:

- don't disable `no-self-use` when you could use `@staticmethod` instead!

- instead of disabling `unused-argument`, prefix the arg (or kwarg) with `_`

- if you _do_ add disable directives, be aware of where you place them.  They can unintentially
  effect more code than you indend.  The order of precidence should be:

  1. inline (only affects the current line)
  1. wrap small bits of code in `# pylint: disable` ... `# pylint: enable` blocks
  1. scope to method calls by placing within the method
  1. scope to class defs by placing within the class definition
  1. last resort: scope to module


## Git Branching Strategy

Branch naming conventions:

*  Use `<desc>-<issue number>` for feature/topic branches
*  Use `wip-` as a prefix for branches are not stable and should not be branched off
*  Prefer hyphens to underscores and lowercase branch names
   - `csv-reports-142` not `CSV_Reports_142`

Merging with master:

1. File an issue if one does not exist already
2. Create a branch of the form `<desc>-<issue number>`
3. Make sure your branch is up to date, then push to GitHub
4. Create a pull request against `master`
5. Assign reviewers
6. Add commits to address feedback
7. Squash commits, as appropriate
8. Merge with master
9. Delete your branch on GitHub

An example of this flow would be:

1. Alice files issue #456 to build a CSV Reporting module
2. She creates the branch `csv-reports-456` with her commits
3. She opens a pull request against `master` with her branch
4. She assigns Bob to review it
5. Bob leaves feedback for Alice to address
6. Alice pushes additional commits to address the feedback
7. Bob gives it a thumbsup and Alice squashes some commits
8. Alice merges the pull request with master
9. Alice deletes branch `csv-reports-456`

In general, do not push directly to a branch unless you are the owner or have
previously discussed it with the branch owner.

To update someone else's branch:

1. Create `<branch name>-pr-<author>`
2. Add commits and create a PR against the original branch
3. Add the branch owner as a reviewer
4. Address feedback from the owner
5. The owner merges the branch when satisfied
6. Delete your branch

An example of this flow would be:

1. Given Alice's branch `csv-reports-456`, Bob creates `csv-reports-456-pr-bob`
2. Bob adds commits and opens a PR against Alice's branch
3. Bob adds Alice as a reviewer
4. Alice leaves feedback for Bob, which Bob addresses
5. Alice merges Bob's pull request
6. Bob deletes branch `csv-reports-456-pr-bob`

### Deploying

Staging and production are deployed by pushing to the `staging`/`production`
branches, respectively.

To deploy:

1. Create PR against `staging`/`production` of the form `deploy-<something>`
   * e.g. `deploy-csv-reports`
2. If making a non-trivial change, ask for a +1 from somebody
3. Merge the PR, which should kick off the deploy

### Git Commit Messages

*  Use the present tense in the subject
   -  "Add feature" not "Added feature"
*  Use the imperative mood in the subject
   -  "Move cursor to..." not "Moves cursor to..."
*  Leave a blank line between the subject and the body
*  Limit the subject to 50 characters or less
*  Limit the body to 72 columns or less (configure your editor to enforce this)
*  Reference issues and pull requests liberally in the description
*  When only changing documentation, include `[ci skip]` in the commit description
*  Include syntax to [automatically close][auto-close] issues
*  Squash commits to the extent that it improves clarity
   - but don't combine patches for two issues in one commit

Rationale behind this is [here][tpope], [here][blog1], [here][blog2],
[here][blog3], and [here][blog4]. For a contrarian view, see [here][holman].

Optional - consider starting the commit subject with an applicable emoji:

| emoji               | shorthand             | usage                       |
| ------------------- | --------------------- | --------------------------- |
| :art:               | `:art:`               | Cosmetic/style changes      |
| :racehorse:         | `:racehorse:`         | Performance                 |
| :recycle:           | `:recycle:`           | Refactoring                 |
| :sparkles:          | `:sparkles:`          | New feature                 |
| :books:             | `:books:`             | Documentation               |
| :card_index:        | `:card_index:`        | Metadata/fixtures           |
| :wrench:            | `:wrench:`            | Tooling                     |
| :floppy_disk:       | `:floppy_disk:`       | Data migration              |
| :wastebasket:       | `:wastebasket:`       | Remove code/files           |
| :bug:               | `:bug:`               | Bug fix                     |
| :fire:              | `:fire:`              | Hotfix                      |
| :poop:              | `:poop:`              | Deprecation                 |
| :green_heart:       | `:green_heart:`       | Fixing the CI build         |
| :white_check_mark:  | `:white_check_mark:`  | Adding tests                |
| :lock:              | `:lock:`              | Dealing with security       |
| :shirt:             | `:shirt:`             | Removing linter warnings    |
| :arrow_up:          | `:arrow_up:`          | Upgrading dependencies      |
| :arrow_down:        | `:arrow_down:`        | Downgrading dependencies    |
| :penguin:           | `:penguin:`           | Fixing something on Linux   |
| :apple:             | `:apple:`             | Fixing something on macOS   |
| :checkered_flag:    | `:checkered_flag:`    | Fixing something on Windows |
| :non-potable_water: | `:non-potable_water:` | Fix memory leaks            |



[auto-close]: https://help.github.com/articles/closing-issues-via-commit-messages/
[tpope]: https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
[blog1]: https://who-t.blogspot.co.at/2009/12/on-commit-messages.html
[blog2]: https://chris.beams.io/posts/git-commit/
[blog3]: https://robots.thoughtbot.com/5-useful-tips-for-a-better-commit-message
[blog4]: https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project
[holman]: https://zachholman.com/posts/git-commit-history/
[pep8]: https://www.python.org/dev/peps/pep-0008/
