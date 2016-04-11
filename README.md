# codeclimate-test-reporter

[![Code Climate](https://codeclimate.com/github/codeclimate/python-test-reporter/badges/gpa.svg)](https://codeclimate.com/github/codeclimate/ruby-test-reporter)

Collects test coverage data from your Python test suite and sends it to Code
Climate's hosted, automated code review service.

Code Climate - [https://codeclimate.com](https://codeclimate.com)

# Important FYIs

Across the many different testing frameworks, setups, and environments, there are lots of variables at play. Before setting up test coverage, it's important to understand what we do and do not currently support:

* **Default branch only:** We only support test coverage for your [default branch](http://docs.codeclimate.com/article/151-glossary-default-branch). Be sure to check out this branch before running your tests.
* **Single payload:** We currently only support a single test coverage payload per commit. If you run your tests in multiple steps, or via parallel tests, Code Climate will only process the first payload that we receive. If you are using a CI, be sure to check if you are running your tests in a parallel mode.

  **Note:** If you've configured Code Climate to analyze multiple languages in the same repository (e.g., Python and JavaScript), we can nonetheless only process test coverage information for one of these languages. We'll process the first payload that we receive.
* **Invalid File Paths:** By default, our test reporters expect your application to exist at the root of your repository. If this is not the case, the file paths in your test coverage payload will not match the file paths that Code Climate expects.

## Troubleshooting

If you're having trouble setting up or working with our test coverage feature, [see our detailed help doc](http://docs.codeclimate.com/article/220-help-im-having-trouble-with-test-coverage), which covers the most common issues encountered.

## Contributions

Patches, bug fixes, feature requests, and pull requests are welcome on the
GitHub page for this project: [https://github.com/codeclimate/python-test-reporter](https://github.com/codeclimate/python-test-reporter)

## Copyright

See LICENSE.txt
