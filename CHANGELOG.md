# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [2.1.0](https://github.com/yaph/charla/releases/tag/2.1.0) - 2024-12-13

<small>[Compare with 2.0.0](https://github.com/yaph/charla/compare/2.0.0...2.1.0)</small>

### Added

- Add support for local settings file. ([87e8387](https://github.com/yaph/charla/commit/87e8387f424e5008575cd8a06a10cdea7fc2b2bf) by Ramiro Gómez).

### Removed

- Remove unused import. ([35b6ba5](https://github.com/yaph/charla/commit/35b6ba506bd5e7ccf6225ccf37e151b49ff9c17c) by Ramiro Gómez).
- Remove isinstance checks to prevent errors resulting from type changes. ([65a0005](https://github.com/yaph/charla/commit/65a0005ffccf2c869e333913b5b451bdb78408d2) by Ramiro Gómez).

## [2.0.0](https://github.com/yaph/charla/releases/tag/2.0.0) - 2024-10-16

<small>[Compare with 1.2.0](https://github.com/yaph/charla/compare/1.2.0...2.0.0)</small>

### Added

- Add CLI help text. ([42cdd55](https://github.com/yaph/charla/commit/42cdd55d395a1cd67c0b8d4786222a59fb2b89b9) by Ramiro Gómez).
- Add message_limit setting to limit number of messages sent to GitHub Models service. Add kwargs to Client constructors. Use deque for automatically managing context (number of messages) for GitHub Models. Update project info. ([818b07f](https://github.com/yaph/charla/commit/818b07f80aa070f296fd20b96b3443543e0af815) by Ramiro Gómez).
- Add CLI test. ([c48ec68](https://github.com/yaph/charla/commit/c48ec686c53b57e77c5b49b9a01c9308ed1dd3e1) by Ramiro Gómez).
- Add tests for client classes. ([05be788](https://github.com/yaph/charla/commit/05be788ef644e94ed2fabf7b9ad4b840f16b42e7) by Ramiro Gómez).
- Add todos. ([5e65e47](https://github.com/yaph/charla/commit/5e65e4799325d00a13e2c0edd48f0f6d1d77fce4) by Ramiro Gómez).
- Add support for Github models. Add provider setting. Add client module with clients for ollama and azure. ([d7b7359](https://github.com/yaph/charla/commit/d7b73593f584aefe299df5f91cc7c05a84193cd7) by Ramiro Gómez).

### Fixed

- Fix linting issues. ([05f147b](https://github.com/yaph/charla/commit/05f147b826f846f2a8fe5890a42b3589a72b3082) by Ramiro Gómez).
- Fix import and test. Add dependencies. ([95d2375](https://github.com/yaph/charla/commit/95d2375ea54b42f234b697df5d361b3fc1d1bcae) by Ramiro Gómez).
- Fix git command. ([d0ea71c](https://github.com/yaph/charla/commit/d0ea71c580d87d6314b2beccbc77f6c1ec2face5) by Ramiro Gómez).

### Changed

- Change Configuration to Settings. ([37a6cdc](https://github.com/yaph/charla/commit/37a6cdc7c59669418a248d3842447ff864787cd0) by Ramiro Gómez).
- Change sample config. ([7eb589c](https://github.com/yaph/charla/commit/7eb589c5698223d0bb98d07a780f1688039ca315) by Ramiro Gómez).

### Removed

- Remove dataclass and write __init__ method. Only call add_message in Client classes. ([4ac0d3b](https://github.com/yaph/charla/commit/4ac0d3bd95817887cf8df611e209721fc202e147) by Ramiro Gómez).
- Remove obsolete file. ([45a91c1](https://github.com/yaph/charla/commit/45a91c1d40c05a1a4d6151dfd0161d107d25f6f1) by Ramiro Gómez).
- Remove models sub command, model_list and available_models functions. Remove check for available models and unused code. Bump version. ([531b125](https://github.com/yaph/charla/commit/531b1258b074b86d3cf72855410ad9101b36adf4) by Ramiro Gómez).

## [1.2.0](https://github.com/yaph/charla/releases/tag/1.2.0) - 2024-07-24

<small>[Compare with 1.1.0](https://github.com/yaph/charla/compare/1.1.0...1.2.0)</small>

### Added

- Add commands to release task. ([f1a2634](https://github.com/yaph/charla/commit/f1a2634d14aa2d879adfb5f3988c6a0a600cce15) by Ramiro Gómez).
- Add info to help. ([428fd77](https://github.com/yaph/charla/commit/428fd7791b77f96c8863931582952157bc411e82) by Ramiro Gómez).
- Add type info. ([db33e43](https://github.com/yaph/charla/commit/db33e43bed2ede04f43379abe69cdbb34bc92c8a) by Ramiro Gómez).
- Add support for opening web pages. ([d0f6431](https://github.com/yaph/charla/commit/d0f6431631bcdccc7c5f2d177af7f763bbb1aa2a) by Ramiro Gómez).
- Add and improve documentation. ([849f4f2](https://github.com/yaph/charla/commit/849f4f2f0e8a08ad5aa4ec75f60ede100b7f2185) by Ramiro Gómez).
- Add CTRL-O keybinding to load content from a file into prompt. ([0a5bc98](https://github.com/yaph/charla/commit/0a5bc9819ce462991fd40621757187e57c076d87) by Ramiro Gómez).

### Fixed

- Fix linting issues. Add tests. ([485cf49](https://github.com/yaph/charla/commit/485cf497d0451520cf16b2799d8225637d94a24a) by Ramiro Gómez).
- Fix import and formatting. ([e722f26](https://github.com/yaph/charla/commit/e722f2694864ebab31984dc8868504ee8d5c4e60) by Ramiro Gómez).

## [1.1.0](https://github.com/yaph/charla/releases/tag/1.1.0) - 2024-07-11

<small>[Compare with 1.0.0](https://github.com/yaph/charla/compare/1.0.0...1.1.0)</small>

### Added

- Add CHANGELOG.md and generate it in publish task. Edit features. Bump version. ([57c8231](https://github.com/yaph/charla/commit/57c8231888f5a0747a05050c1dc8cbd7acda9626) by Ramiro Gómez).
- Add hatch scripts ([4341099](https://github.com/yaph/charla/commit/4341099c1c7f63ca53e322250c515b63e8c104c0) by Ramiro Gómez).
- Add multiline setting Less restrictive type annotations Add test_configy.py ([f26a30e](https://github.com/yaph/charla/commit/f26a30e46214a1a81ec0e1319333d747cba4e903) by Ramiro Gómez).
- Add models sub command to show info about models. Simplify settings sub command. ([1b68bd4](https://github.com/yaph/charla/commit/1b68bd46ec711d4531b9de7e7b8bac22f2d19baa) by Ramiro Gómez).

### Fixed

- Fix typing issues Rename env ([b09b5b0](https://github.com/yaph/charla/commit/b09b5b0df5aff716af8c9b4cc3340671db468d16) by Ramiro Gómez).
- Fix and ignore linting errors ([5af18a3](https://github.com/yaph/charla/commit/5af18a34462b6ddc868fa55dcb4f2c9dc6411801) by Ramiro Gómez).

### Removed

- Remove todo ([f5edef7](https://github.com/yaph/charla/commit/f5edef75b6499ac4a7232885c6f979a735f50e48) by Ramiro Gómez).
- Remove repeated settings processing. Add settings sub command. ([dc34e4d](https://github.com/yaph/charla/commit/dc34e4d2f3718c0f63b3f3a6cfeb03eeccd64ae3) by Ramiro Gómez).
- Remove todo and add more info ([9aec9ff](https://github.com/yaph/charla/commit/9aec9fff0595af7e84afa41304b689caf19fbae3) by Ramiro Gómez).
- Remove __name__ attribute Improve code ([4c78ae9](https://github.com/yaph/charla/commit/4c78ae93e11b7c715acc649b7a31c064e5fc0295) by Ramiro Gómez).

## [1.0.0](https://github.com/yaph/charla/releases/tag/1.0.0) - 2024-06-27

<small>[Compare with first commit](https://github.com/yaph/charla/compare/b7f1493840aab4b017d49cb55749fe4b50156275...1.0.0)</small>

### Added

- Add development documentation. Handle keyboard interrupt. Remove rich dependency. Add todo.md ([d18dc32](https://github.com/yaph/charla/commit/d18dc32c8392795073a7122a71e7b35cf0c1d225) by Ramiro Gómez).
- Add files for PyPI project. Move logic to util.py ([01be6de](https://github.com/yaph/charla/commit/01be6de6d2c52c6cc0946eefea8b22fb7ba2387f) by Ramiro Gómez).
- Add README ([b9fc3e7](https://github.com/yaph/charla/commit/b9fc3e70cbf5f80d1056b73f4186c27663a0c0bd) by Ramiro Gómez).

### Fixed

- Fix syntax ([1c683c3](https://github.com/yaph/charla/commit/1c683c3b6ba66f6707e2d24b53e42d1219cf6223) by Ramiro Gómez).
- Fix model check after type change ([05808ed](https://github.com/yaph/charla/commit/05808ed893711dc8353324aaaa70fb1bbf676c5e) by Ramiro Gómez).
- Fix test ([16d8664](https://github.com/yaph/charla/commit/16d8664682a055c4ed86ee3c3a0357728b189937) by Ramiro Gómez).
- Fix import ([74af167](https://github.com/yaph/charla/commit/74af167b51787ae2f1591629ec7007ad2489172e) by Ramiro Gómez).

