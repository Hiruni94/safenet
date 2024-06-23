from unittest import mock
from uuid import uuid4

from tests.providers.azure.azure_fixtures import (
    AZURE_SUBSCRIPTION_ID,
    set_mocked_azure_provider,
)


class Test_app_client_certificates_on:
    def test_app_no_subscriptions(self):
        app_client = mock.MagicMock
        app_client.apps = {}

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=set_mocked_azure_provider(),
        ), mock.patch(
            "prowler.providers.azure.services.app.app_client_certificates_on.app_client_certificates_on.app_client",
            new=app_client,
        ):
            from prowler.providers.azure.services.app.app_client_certificates_on.app_client_certificates_on import (
                app_client_certificates_on,
            )

            check = app_client_certificates_on()
            result = check.execute()
            assert len(result) == 0

    def test_app_subscription_empty(self):
        app_client = mock.MagicMock
        app_client.apps = {AZURE_SUBSCRIPTION_ID: {}}

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=set_mocked_azure_provider(),
        ), mock.patch(
            "prowler.providers.azure.services.app.app_client_certificates_on.app_client_certificates_on.app_client",
            new=app_client,
        ):
            from prowler.providers.azure.services.app.app_client_certificates_on.app_client_certificates_on import (
                app_client_certificates_on,
            )

            check = app_client_certificates_on()
            result = check.execute()
            assert len(result) == 0

    def test_app_client_certificates_on(self):
        resource_id = f"/subscriptions/{uuid4()}"
        app_client = mock.MagicMock

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=set_mocked_azure_provider(),
        ), mock.patch(
            "prowler.providers.azure.services.app.app_client_certificates_on.app_client_certificates_on.app_client",
            new=app_client,
        ):
            from prowler.providers.azure.services.app.app_client_certificates_on.app_client_certificates_on import (
                app_client_certificates_on,
            )
            from prowler.providers.azure.services.app.app_service import WebApp

            app_client.apps = {
                AZURE_SUBSCRIPTION_ID: {
                    "app_id-1": WebApp(
                        resource_id=resource_id,
                        auth_enabled=True,
                        configurations=None,
                        client_cert_mode="Required",
                        https_only=False,
                        identity=None,
                        location="West Europe",
                    )
                }
            }
            check = app_client_certificates_on()
            result = check.execute()
            assert len(result) == 1
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == f"Clients are required to present a certificate for app 'app_id-1' in subscription '{AZURE_SUBSCRIPTION_ID}'."
            )
            assert result[0].resource_id == resource_id
            assert result[0].resource_name == "app_id-1"
            assert result[0].subscription == AZURE_SUBSCRIPTION_ID
            assert result[0].location == "West Europe"

    def test_app_client_certificates_off(self):
        resource_id = f"/subscriptions/{uuid4()}"
        app_client = mock.MagicMock

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=set_mocked_azure_provider(),
        ), mock.patch(
            "prowler.providers.azure.services.app.app_client_certificates_on.app_client_certificates_on.app_client",
            new=app_client,
        ):
            from prowler.providers.azure.services.app.app_client_certificates_on.app_client_certificates_on import (
                app_client_certificates_on,
            )
            from prowler.providers.azure.services.app.app_service import WebApp

            app_client.apps = {
                AZURE_SUBSCRIPTION_ID: {
                    "app_id-1": WebApp(
                        resource_id=resource_id,
                        auth_enabled=True,
                        configurations=None,
                        client_cert_mode="Ignore",
                        https_only=False,
                        identity=None,
                        location="West Europe",
                    )
                }
            }
            check = app_client_certificates_on()
            result = check.execute()
            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == f"Clients are not required to present a certificate for app 'app_id-1' in subscription '{AZURE_SUBSCRIPTION_ID}'."
            )
            assert result[0].resource_id == resource_id
            assert result[0].resource_name == "app_id-1"
            assert result[0].subscription == AZURE_SUBSCRIPTION_ID
            assert result[0].location == "West Europe"
