# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

### Changed
* Fixed bug [#212](https://github.com/compas-dev/compas_view2/issues/212).
### Removed


## [0.11.0] 2023-12-17

### Added


* Added `viewport` and `camera` in the config
* Added the update method for the `textobject`.


### Changed

* Change the str options in `view_port` into all lower case.
* Change naming `view_mode` to `viewport_mode`, `view_port` to `viewport`. 
* Doc building using `sphinx_compas2_theme `.
* Fix the documentation: title lines, comments.
* Fix a bug when camera is looking straight up or down.

### Removed

## [0.10.1] 2023-12-12

### Added

### Changed

### Removed

* Removed dependency on `cython`.

## [0.10.0] 2023-11-27

### Added

* Added keyboard diagram in the doc.
* Add example `example_custom_keys.py` in the examples/control.
* Action class which controls all the key actions.
* Added `ryven` version specification (0.3.1.4).
* Added example: `example_image_display`.
* Added `fullscreen` option to `App` and the corresponding config file.
* Option to pass in App init parameters through config file (with an example)
* Add `Developer Guide` section in the documentation.
* Update the example files in the tutorial.
* Update the software architecture diagram in the documentation.
* Update the UI naming conventions diagram in the documentation.
* Add the `Tutorial Software Concepts` section in the documentation.
* Add the `Tutorial Configuration` section in the documentation.
* Multi-selection in scene form.
* Added an example `example_pair_object_form.py`.
* Added `absolute_height` option to the `TextObject`.
* Added `font` option to `TextObject`.
* Multi-cursor visual effects.
* Added `F` key for focusing the selected objects. If no object is selected, it will focus the whole scene geometries.
* Added all the examples based on the `scripts` file.
* All the examples are categorized into different folders.

### Changed

* Update the `README.md`
* Move mouse and key actions to controller.
* Categorize all the view settings in to one config file.
* Changed the language settings in the `config.py` file for better `invoke docs` generation.
* Remove `modindex` in the index page of the documentation as the file no longer exists.
* Changed `sphinx` requirement for the development environment. Otherwise, there will be a bug similar to [this](https://github.com/compas-dev/sphinx_compas_theme/issues/20).
* Bug fixed when pressing `F` multiple times, the camera angle shifts.
* Bug fixed in `Camera.zoom_extents` when one single point is selected.

### Removed

## [0.9.4] 2023-08-30

### Added

### Changed

* Fixed issue of thread keep running after raising errors.

### Removed

## [0.9.3] 2023-08-24

### Added

### Changed

* Fix robot object visulisation bug.

### Removed

## [0.9.2] 2023-03-27

### Added

### Changed

### Removed

## [0.9.1] 2023-01-11

### Added

### Changed

* Updated workflows to v2.
* Updated dev dependencies.
* Uses `compas_invocations` for `task.py`.

### Removed

## [0.9.0] 2022-11-06

### Added

* Added `Scale` factor for `Camera`.
* Added `look_at` function to `Camera`
* Added `compas_view2.values.Value` class.
* Added `compas_view2.values.BoolValue` class.
* Added `compas_view2.values.IntValue` class.
* Added `compas_view2.values.FloatValue` class.
* Added `compas_view2.values.StrValue` class.
* Added `compas_view2.values.ListValue` class.
* Added `compas_view2.values.DictValue` class.
* Added `compas_view2.values.Settings` class.

### Changed

### Removed

## [0.8.0] 2022-10-07

### Added

* Added `RobotObject`.
* Added `datastore` to `TreeForm`.
* Added `TabsForm`.
* Added `BRepObject`.
* Added `zoom_extents` to `Camera`.
* Added `expanded` option for `TreeForm` data entries.
* Added `striped_rows` option for `TreeForm`.
* Added `option` to display drop down list for `TreeForm` item editing.
* Added `on_object_selected` event listener.
* Added `use_vertex_color` option to `MeshObject`.

### Changed

* Give access to `self` in `TreeForm` click events.
* Allow `TreeForm` columns to be editable.
* Auto adjust first column width in `TreeForm`.
* Allow set colums individually in `TabsForm`.
* Fix `TabsForm` top margin display issue on macos.
* Fixed a `Ghostmode` bug.
* Allow `TabsFrom` to update.

### Removed

## [0.7.0] 2022-08-22

### Added

### Changed

* Moved `pointcolor`, `linecolor`, `facecolor` to `Object` from `BufferObject`.
* Exposing `pointcolor`, `linecolor`, `facecolor` at `App.add` for pylance linting.
* `pointcolor`, `linecolor`, `facecolor` now accept both single value or dictionary of values.

### Removed

* `pointcolors`, `linecolors`, `facecolors` are removed, use `pointcolor`, `linecolor`, `facecolor` instead.
* `treeform` is now more customizable.
* Removed placeholder menu items.

## [0.6.0] 2022-07-21

### Added

* Added dedicated Scene objects form.
* Added dedicated object property form.
* Added custom tree form.
* Added option to run multi-threading function.
* Added sidedock options.
* Added option to change App title.
* Added matplotlib integration.

### Changed

### Removed

## [0.5.0] 2022-03-22

### Added

* Added (optional) Ryven flow integration.
* Added Vector object.
* Separate shaders for background, model, and overlay objects.
* Collection object for large numbers of individual objects.

### Changed

* Changed blending of opacity to be based on camera distance.
* Updated workflow to latest.
* Reconstructed Camera class.
* Switch build workflow to run with conda.

### Removed
