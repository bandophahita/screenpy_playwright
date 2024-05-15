Release History
===============

0.0.3 (2024-05-15)
------------------

### New Features

- Added several new Actions: `RefreshThePage`, `Scroll`, `Select`, `SaveScreenshot`
- Added several new Questions: `Attribute`, `BrowserURL`, `Element`
- Added a new Resolution: `IsVisible`
- Added several aliases for the existing Actions, Questions, and Resolutions.
- `Target` now also fully supports all Playwright locator methods.

### Bug fixes

- Enabled multiple Actors to be able to `exit` without breaking Playwright for each other.

## Development Niceties

- ScreenPy: Playwright is now standardized with the other ScreenPy projects (thanks, @bandophahita)!


0.0.2 (2024-02-13)
------------------

### Improvements

- Made all the user-facing features of ScreenPy: Playwright importable from the root, like the other ScreenPy plugins.

### Development Niceties

- Added Poetry!
- Added ruff!
- It's nice!!!


0.0.1 (2022-09-18)
------------------

### Timeline

- Initial release!
