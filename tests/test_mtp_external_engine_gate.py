# SPDX-License-Identifier: Apache-2.0
"""MTP must report itself unavailable while an external engine serves a model.

Splash has no MTP path (it runs its own DFlash2 drafts), so a model saved
with ``external_engine`` set reported ``mtp_compatible: true`` while the
toggle silently did nothing (issue #5146).
"""

from types import SimpleNamespace

from omlx.admin.routes import (
    EXTERNAL_ENGINE_MTP_REASON,
    _demote_mtp_for_selected_engine,
)


def _engine(engine_id="splash", compatible=True):
    return {
        "id": engine_id,
        "label": "Splash",
        "compatible": compatible,
        "reason": "",
    }


class TestDemoteMtpForSelectedEngine:
    def test_no_engine_selected_keeps_compat(self):
        settings = SimpleNamespace(external_engine=None)
        ok, reason = _demote_mtp_for_selected_engine(True, "", settings, [_engine()])
        assert (ok, reason) == (True, "")

    def test_missing_settings_keeps_compat(self):
        ok, reason = _demote_mtp_for_selected_engine(True, "", None, [_engine()])
        assert (ok, reason) == (True, "")

    def test_selected_serving_engine_demotes(self):
        settings = SimpleNamespace(external_engine="splash")
        ok, reason = _demote_mtp_for_selected_engine(True, "", settings, [_engine()])
        assert not ok
        assert reason == EXTERNAL_ENGINE_MTP_REASON

    def test_selected_unavailable_engine_keeps_compat(self):
        settings = SimpleNamespace(external_engine="splash")
        ok, reason = _demote_mtp_for_selected_engine(
            True, "", settings, [_engine(compatible=False)]
        )
        assert (ok, reason) == (True, "")

    def test_models_the_engine_cannot_serve_keep_compat(self):
        settings = SimpleNamespace(external_engine="splash")
        ok, reason = _demote_mtp_for_selected_engine(True, "", settings, [])
        assert (ok, reason) == (True, "")

    def test_incompatible_model_keeps_original_reason(self):
        settings = SimpleNamespace(external_engine="splash")
        ok, reason = _demote_mtp_for_selected_engine(
            False, "checkpoint has no mtp.* tensors", settings, [_engine()]
        )
        assert not ok
        assert reason == "checkpoint has no mtp.* tensors"
