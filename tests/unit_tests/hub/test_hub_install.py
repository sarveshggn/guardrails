import pytest
from unittest.mock import ANY, call, MagicMock

from guardrails.classes.credentials import Credentials
from guardrails.cli.server.module_manifest import ModuleManifest
from guardrails.hub.validator_package_service import (
    InvalidHubInstallURL,
)

from guardrails.hub.install import LocalModelFlagNotSet, install


@pytest.mark.parametrize(
    "use_remote_inferencing",
    [False, True],
)
class TestInstall:
    def setup_method(self):
        self.manifest = ModuleManifest.from_dict(
            {
                "id": "id",
                "name": "name",
                "author": {"name": "me", "email": "me@me.me"},
                "maintainers": [],
                "repository": {"url": "some-repo"},
                "namespace": "guardrails",
                "package_name": "test-validator",
                "module_name": "test_validator",
                "exports": ["TestValidator"],
                "tags": {"has_guardrails_endpoint": False},
            }
        )
        self.site_packages = "./.venv/lib/python3.X/site-packages"

    def test_exits_early_if_uri_is_not_valid(self, mocker, use_remote_inferencing):
        mocker.patch(
            "guardrails.hub.install.Credentials.has_rc_file",
            return_value=True,
        )
        with pytest.raises(InvalidHubInstallURL):
            install("not a hub uri")

    def test_install_local_models__false(self, mocker, use_remote_inferencing):
        mocker.patch(
            "guardrails.hub.install.Credentials.has_rc_file",
            return_value=True,
        )
        mocker.patch(
            "guardrails.hub.install.Credentials.from_rc_file",
            return_value=Credentials.from_dict(
                {"use_remote_inferencing": use_remote_inferencing}
            ),
        )

        mock_logger_log = mocker.patch("guardrails.hub.install.cli_logger.log")

        get_manifest_and_site_packages_mock = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_manifest_and_site_packages"
        )
        mock_pip_install_hub_module = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.install_hub_module"
        )
        mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_validator_from_manifest"
        )
        mock_add_to_hub_init = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.add_to_hub_inits"
        )

        get_manifest_and_site_packages_mock.return_value = (
            self.manifest,
            self.site_packages,
        )

        install(
            "hub://guardrails/test-validator",
            install_local_models=False,
            install_local_models_confirm=lambda: False,
        )

        log_calls = [
            call(level=5, msg="Installing hub://guardrails/test-validator..."),
            call(
                level=5,
                msg="Skipping post install, models will not be downloaded for local "
                "inference.",
            ),
            call(
                level=5,
                msg="✅Successfully installed hub://guardrails/test-validator!\n\nImport validator:\nfrom guardrails.hub import TestValidator\n\nGet more info:\nhttps://hub.guardrailsai.com/validator/id\n",  # noqa
            ),  # noqa
        ]
        assert mock_logger_log.call_count == 3
        mock_logger_log.assert_has_calls(log_calls)

        get_manifest_and_site_packages_mock.assert_called_once_with(
            "guardrails/test-validator"
        )

        mock_pip_install_hub_module.assert_called_once_with(
            self.manifest, self.site_packages, quiet=ANY, logger=ANY
        )
        mock_add_to_hub_init.assert_called_once_with(self.manifest, self.site_packages)

    def test_install_local_models__true(self, mocker, use_remote_inferencing):
        mocker.patch(
            "guardrails.hub.install.Credentials.has_rc_file",
            return_value=True,
        )
        mocker.patch(
            "guardrails.hub.install.Credentials.from_rc_file",
            return_value=Credentials.from_dict(
                {"use_remote_inferencing": use_remote_inferencing}
            ),
        )

        mock_logger_log = mocker.patch("guardrails.hub.install.cli_logger.log")

        get_manifest_and_site_packages_mock = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_manifest_and_site_packages"
        )
        mock_pip_install_hub_module = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.install_hub_module"
        )
        mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_validator_from_manifest"
        )
        mock_add_to_hub_init = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.add_to_hub_inits"
        )

        get_manifest_and_site_packages_mock.return_value = (
            self.manifest,
            self.site_packages,
        )

        install(
            "hub://guardrails/test-validator",
            install_local_models=True,
            install_local_models_confirm=lambda: True,
        )

        log_calls = [
            call(level=5, msg="Installing hub://guardrails/test-validator..."),
            call(
                level=5,
                msg="Installing models locally!",
            ),
            call(
                level=5,
                msg="✅Successfully installed hub://guardrails/test-validator!\n\nImport validator:\nfrom guardrails.hub import TestValidator\n\nGet more info:\nhttps://hub.guardrailsai.com/validator/id\n",  # noqa
            ),  # noqa
        ]
        assert mock_logger_log.call_count == 3
        mock_logger_log.assert_has_calls(log_calls)

        get_manifest_and_site_packages_mock.assert_called_once_with(
            "guardrails/test-validator"
        )

        mock_pip_install_hub_module.assert_called_once_with(
            self.manifest, self.site_packages, quiet=ANY, logger=ANY
        )
        mock_add_to_hub_init.assert_called_once_with(self.manifest, self.site_packages)

    def test_install_local_models__none(self, mocker, use_remote_inferencing):
        mocker.patch(
            "guardrails.hub.install.Credentials.has_rc_file",
            return_value=True,
        )
        mocker.patch(
            "guardrails.hub.install.Credentials.from_rc_file",
            return_value=Credentials.from_dict(
                {"use_remote_inferencing": use_remote_inferencing}
            ),
        )

        mock_logger_log = mocker.patch("guardrails.hub.install.cli_logger.log")

        get_manifest_and_site_packages_mock = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_manifest_and_site_packages"
        )
        mock_pip_install_hub_module = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.install_hub_module"
        )
        mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_validator_from_manifest"
        )
        mock_add_to_hub_init = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.add_to_hub_inits"
        )

        get_manifest_and_site_packages_mock.return_value = (
            self.manifest,
            self.site_packages,
        )

        install(
            "hub://guardrails/test-validator",
            install_local_models=None,
            install_local_models_confirm=lambda: True,
        )

        log_calls = [
            call(level=5, msg="Installing hub://guardrails/test-validator..."),
            call(
                level=5,
                msg="Installing models locally!",
            ),
            call(
                level=5,
                msg="✅Successfully installed hub://guardrails/test-validator!\n\nImport validator:\nfrom guardrails.hub import TestValidator\n\nGet more info:\nhttps://hub.guardrailsai.com/validator/id\n",  # noqa
            ),  # noqa
        ]
        assert mock_logger_log.call_count == 3
        mock_logger_log.assert_has_calls(log_calls)

        get_manifest_and_site_packages_mock.assert_called_once_with(
            "guardrails/test-validator"
        )

        mock_pip_install_hub_module.assert_called_once_with(
            self.manifest, self.site_packages, quiet=ANY, logger=ANY
        )
        mock_add_to_hub_init.assert_called_once_with(self.manifest, self.site_packages)

    def test_happy_path(self, mocker, use_remote_inferencing):
        mocker.patch(
            "guardrails.hub.install.Credentials.has_rc_file",
            return_value=True,
        )
        mocker.patch(
            "guardrails.hub.install.Credentials.from_rc_file",
            return_value=Credentials.from_dict(
                {"use_remote_inferencing": use_remote_inferencing}
            ),
        )

        mock_logger_log = mocker.patch("guardrails.hub.install.cli_logger.log")

        get_manifest_and_site_packages_mock = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_manifest_and_site_packages"
        )
        mock_pip_install_hub_module = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.install_hub_module"
        )
        mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_validator_from_manifest"
        )
        mock_add_to_hub_init = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.add_to_hub_inits"
        )

        get_manifest_and_site_packages_mock.return_value = (
            self.manifest,
            self.site_packages,
        )

        install(
            "hub://guardrails/test-validator",
            install_local_models_confirm=lambda: True,
        )

        log_calls = [
            call(level=5, msg="Installing hub://guardrails/test-validator..."),
            call(
                level=5,
                msg="Installing models locally!",  # noqa
            ),  # noqa
        ]

        assert mock_logger_log.call_count == 3
        mock_logger_log.assert_has_calls(log_calls)

        get_manifest_and_site_packages_mock.assert_called_once_with(
            "guardrails/test-validator"
        )

        mock_pip_install_hub_module.assert_called_once_with(
            self.manifest, self.site_packages, quiet=ANY, logger=ANY
        )
        mock_add_to_hub_init.assert_called_once_with(self.manifest, self.site_packages)

    def test_install_local_models_confirmation(self, mocker, use_remote_inferencing):
        mocker.patch(
            "guardrails.hub.install.Credentials.has_rc_file",
            return_value=False,
        )
        mocker.patch("guardrails.hub.install.cli_logger.log")
        mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.install_hub_module"
        )
        mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_validator_from_manifest"
        )
        mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.add_to_hub_inits"
        )

        mock_get_manifest_and_site_packages = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_manifest_and_site_packages"
        )

        manifest_with_endpoint = ModuleManifest.from_dict(
            {
                "id": "test-id",
                "name": "test-name",
                "author": {"name": "test-author", "email": "test@email.com"},
                "maintainers": [],
                "repository": {"url": "test-repo"},
                "namespace": "test-namespace",
                "package_name": "test-package",
                "module_name": "test_module",
                "exports": ["TestValidator"],
                "tags": {"has_guardrails_endpoint": True},
            }
        )

        mock_get_manifest_and_site_packages.return_value = (
            manifest_with_endpoint,
            self.site_packages,
        )

        mock_confirm = MagicMock()
        install(
            "hub://guardrails/test-validator",
            install_local_models_confirm=mock_confirm,
        )

        mock_confirm.assert_called_once()

    def test_install_local_models_confirmation_raises_exception(
        self, mocker, use_remote_inferencing
    ):
        mocker.patch(
            "guardrails.hub.install.Credentials.has_rc_file",
            return_value=False,
        )
        mocker.patch("guardrails.hub.install.cli_logger.log")
        mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.install_hub_module"
        )
        mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_validator_from_manifest"
        )
        mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.add_to_hub_inits"
        )

        mock_get_manifest_and_site_packages = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_manifest_and_site_packages"
        )

        manifest_with_endpoint = ModuleManifest.from_dict(
            {
                "id": "test-id",
                "name": "test-name",
                "author": {"name": "test-author", "email": "test@email.com"},
                "maintainers": [],
                "repository": {"url": "test-repo"},
                "namespace": "test-namespace",
                "package_name": "test-package",
                "module_name": "test_module",
                "exports": ["TestValidator"],
                "tags": {"has_guardrails_endpoint": True},
            }
        )

        mock_get_manifest_and_site_packages.return_value = (
            manifest_with_endpoint,
            self.site_packages,
        )

        with pytest.raises(LocalModelFlagNotSet):
            install(
                "hub://guardrails/test-validator",
            )

    def test_use_remote_endpoint(self, mocker, use_remote_inferencing: bool):
        mocker.patch(
            "guardrails.hub.install.Credentials.has_rc_file",
            return_value=True,
        )
        mocker.patch(
            "guardrails.hub.install.Credentials.from_rc_file",
            return_value=Credentials.from_dict(
                {"use_remote_inferencing": use_remote_inferencing}
            ),
        )

        mock_logger_log = mocker.patch("guardrails.hub.install.cli_logger.log")

        get_manifest_and_site_packages_mock = mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_manifest_and_site_packages"
        )
        mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.install_hub_module"
        )
        mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.get_validator_from_manifest"
        )
        mocker.patch(
            "guardrails.hub.validator_package_service.ValidatorPackageService.add_to_hub_inits"
        )

        manifest = ModuleManifest.from_dict(
            {
                "id": "id",
                "name": "name",
                "author": {"name": "me", "email": "me@me.me"},
                "maintainers": [],
                "repository": {"url": "some-repo"},
                "namespace": "guardrails",
                "package_name": "test-validator",
                "module_name": "test_validator",
                "exports": ["TestValidator"],
                "tags": {"has_guardrails_endpoint": True},
            }
        )
        get_manifest_and_site_packages_mock.return_value = manifest, self.site_packages

        install("hub://guardrails/test-validator")

        msg = (
            "Skipping post install, models will not be downloaded for local inference."
            if use_remote_inferencing
            else "Installing models locally!"
        )

        log_calls = [
            call(level=5, msg="Installing hub://guardrails/test-validator..."),
            call(
                level=5,
                msg=msg,  # noqa
            ),  # noqa
        ]

        assert mock_logger_log.call_count == 3
        mock_logger_log.assert_has_calls(log_calls)
