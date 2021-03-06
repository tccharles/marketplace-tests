#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from mocks.mock_application import MockApplication
from mocks.marketplace_api import MarketplaceAPI
from pages.desktop.developer_hub.home import Home
from tests.base_test import BaseTest


class TestAPI(BaseTest):

    @pytest.mark.credentials
    def test_assert_that_an_app_can_be_added_and_deleted_via_the_api(self, mozwebqa_devhub_logged_in):
        mock_app = MockApplication()  # generate mock app

        # init API client
        mk_api = MarketplaceAPI.get_client(mozwebqa_devhub_logged_in.base_url,
                                           mozwebqa_devhub_logged_in.credentials)

        mk_api.submit_app(mock_app)  # submit app

        app_status = mk_api.app_status(mock_app)  # get app data from API

        # check that app is pending
        Assert.equal(2, app_status['status'])

        # Check for app on the site
        dev_home = Home(mozwebqa_devhub_logged_in)

        app_status_page = dev_home.go_to_app_status_page(mock_app)
        Assert.contains(mock_app.name, app_status_page.page_title)

        # Delete the app
        mk_api.delete_app(mock_app)

        app_status_page = dev_home.go_to_app_status_page(mock_app)
        Assert.contains("We're sorry, but we can't find what you're looking for.",
                        app_status_page.app_not_found_message)
