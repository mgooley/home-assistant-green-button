# Green Button

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Ruff][ruff-shield]][ruff]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

A [Home Assistant](https://www.home-assistant.io/) custom integration for
importing energy usage and cost data exported in the
[Green Button](https://www.energy.gov/data/green-button) / ESPI (Energy Services
Provider Interface) Atom format defined by the North American Energy Standards
Board.

Many US utilities let you download your interval usage as a "Green Button" XML
file. This integration parses that file, backfills Home Assistant's long-term
statistics so the data shows up in the **Energy Dashboard**, and exposes the
most recent reading and cost as entities.

**This integration sets up the following platforms:**

| Platform | Description                                                                             |
| -------- | --------------------------------------------------------------------------------------- |
| `number` | One entity for the most recent usage reading and one for its cost, per meter reading.    |

## Installation

### HACS (recommended)

1. Add this repository as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories/) in [HACS](https://hacs.xyz/), category **Integration**.
2. Install the **Green Button integration**.
3. Restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration** and search for **Green Button**.

### Manual

1. Copy `custom_components/green_button` into your Home Assistant `config/custom_components` directory.
2. Restart Home Assistant.
3. Add the integration from **Settings → Devices & Services**.

## Configuration

Configuration is done entirely in the UI.

1. Download your usage data from your utility in the Green Button / ESPI XML format.
2. Start the **Green Button** integration setup.
3. Give the usage point a name and paste the contents of the XML file.
4. The integration validates the XML (it must contain exactly one `UsagePoint`), creates the entities, and imports the historical statistics.

To add more data later (for example, a newer export from the same utility), call
the `green_button.import_espi_xml` action with the new XML. Statistics are
imported idempotently, so re-importing overlapping data is safe.

## Actions

| Action                          | Description                                                                 |
| ------------------------------- | --------------------------------------------------------------------------- |
| `green_button.import_espi_xml`  | Import additional usage data from an ESPI XML string.                        |
| `green_button.delete_statistics`| Delete a single Green Button long-term statistic by ID.                     |
| `green_button.reset`            | Reset the targeted entities and clear their long-term statistics.            |
| `green_button.log_statistics`   | Log the recorded statistics for the targeted entities over a range (debug). |

## Development

This project uses [`ruff`](https://docs.astral.sh/ruff/) for linting and
formatting and [`pytest`](https://docs.pytest.org/) with
[`pytest-homeassistant-custom-component`](https://github.com/MatthewFlamm/pytest-homeassistant-custom-component)
for tests. Python 3.14 is required to match current Home Assistant.

```bash
pip install -r requirements_test.txt
pre-commit install
pre-commit run --all-files
pytest tests
```

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[ruff]: https://docs.astral.sh/ruff/
[ruff-shield]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/vqvu/home-assistant-green-button.svg?style=for-the-badge
[commits]: https://github.com/vqvu/home-assistant-green-button/commits/master
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/vqvu/home-assistant-green-button.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40vqvu-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/vqvu/home-assistant-green-button.svg?style=for-the-badge
[releases]: https://github.com/vqvu/home-assistant-green-button/releases
[user_profile]: https://github.com/vqvu
