=============================
France - OCA Chart of Account
=============================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:ed9d3f34e8dc90f210af3ee28d573e4e9fa917c6d56af792571392804c78a527
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fl10n--france-lightgray.png?logo=github
    :target: https://github.com/OCA/l10n-france/tree/16.0/l10n_fr_oca
    :alt: OCA/l10n-france
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/l10n-france-16-0/l10n-france-16-0-l10n_fr_oca
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/l10n-france&target_branch=16.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module provides the chart of accounts, taxes and fiscal positions for companies based in France mainland. It doesn't apply to
companies based in the DOM-TOMs (Guadeloupe, Martinique, Guyane, Réunion, Mayotte, etc.).

This module is a fork of the **l10n_fr** module from the official addons. The decision to maintain a fork was taken after the merge of this huge `pull request <https://github.com/odoo/odoo/pull/84918>`_ on Odoo version 14.0 on October 6th 2022. This pull request increased the number of taxes to 67 (!) and suffer the contrains of the VAT module of Odoo Enterprise. It broke 2 OCA modules: **l10n_fr_account_tax_unece** and the test suite of **l10n_fr_account_vat_return**.

The goals of the fork are:

* provide a reasonable number of taxes (35 taxes, compared to 67 which is about half the number of taxes provided by the **l10n_fr** module !),
* provide a clean and up-to-date chart of account for France (up-to-date with official chart of account of the `ANC <https://www.anc.gouv.fr/>`_ published on January 1st 2019),
* provide taxes, fiscal positions and a chart of accounts properly configured for the OCA module **l10n_fr_account_vat_return**, the opensource VAT module for France,
* keep compatibility with **l10n_fr** (you can have both **l10n_fr** and **l10n_fr_oca** installed on the same Odoo database).

**Table of contents**

.. contents::
   :local:

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/l10n-france/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/l10n-france/issues/new?body=module:%20l10n_fr_oca%0Aversion:%2016.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Akretion
* Odoo SA

Contributors
~~~~~~~~~~~~

* Alexis de Lattre <alexis.delattre@akretion.com>

Contributors on the module before the fork:

* Odoo SA
* Sistheo
* Zeekom
* CrysaLEAD
* Akretion
* Camptocamp

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-alexis-via| image:: https://github.com/alexis-via.png?size=40px
    :target: https://github.com/alexis-via
    :alt: alexis-via

Current `maintainer <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-alexis-via| 

This module is part of the `OCA/l10n-france <https://github.com/OCA/l10n-france/tree/16.0/l10n_fr_oca>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
