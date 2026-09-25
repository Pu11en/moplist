"""The lead-quality rules, pinned to the real rows that got through.

STATUS.md lists four defects found in `data/delivered/new-braunfels-2026-09-09.csv`, each
described as something that would burn a paying customer. There were no tests in this repo,
which is how all four reached a delivered list. Every case below is taken from that file so
a regression is recognisable rather than abstract.

The standard STATUS.md sets, and the one these encode: would a cleaning company owner
recognise the name and know where to drive?

    python3 -m pytest tests/ -q
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from step2_filter import verdict  # noqa: E402
from step3_verify import normalise_address, premises_verdict  # noqa: E402


# ---------------------------------------------------------------- names (step 2)


@pytest.mark.parametrize("name", [
    "LUIS JESUS MARRUPE GRUEIRO LLC",   # the four-word name from the delivered file
    "MARIA DE LOS SANTOS LLC",
    "DUY HUYNH LLC",                    # two words, caught before
    "HEIDI HOLMES, LLC",                # comma form
])
def test_personal_names_are_dropped_at_two_to_four_words(name):
    """The old rule matched two words only, so four-word Hispanic and compound surnames
    went through. A cleaner cannot tell what LUIS JESUS MARRUPE GRUEIRO LLC does."""
    assert verdict(name) == "drop_personal_name", name


@pytest.mark.parametrize("name", [
    "MARY JANE DENTAL LLC",             # three words, but DENTAL is a real place
    "JOSE LUIS TAQUERIA LLC",
    "PRESS ON COUNSELING",
    "AIRES ARTISAN BAKERY LLC",
])
def test_a_physical_hint_beats_the_personal_name_guess(name):
    """Widening the personal-name rule is only safe because a physical hint is checked
    first. DENTAL is evidence of a place with floors; a name shape is only a guess about
    the absence of one, and a guess must not beat evidence."""
    assert verdict(name) == "keep_physical_hint", name


def test_holding_companies_are_still_dropped():
    assert verdict("BLUEBONNET HOLDINGS GROUP LLC") == "drop_no_premises"
    assert verdict("LONESTAR CAPITAL PARTNERS") == "drop_no_premises"


def test_a_name_with_no_signal_survives_for_step_three_to_judge():
    """BYKOWSKI LLC tells a cleaner nothing, but the name alone is not proof of absence:
    the address in step 3 decides."""
    assert verdict("BYKOWSKI LLC") == "keep_unknown"


# ---------------------------------------------------------------- addresses (step 3)


def test_a_subdivision_address_with_no_street_type_is_treated_as_a_house():
    """2839 ROSEFINCH reached a delivered list. A commercial line carries ST, BLVD, STE or
    a highway number; a bare subdivision name carries none of them."""
    where, confidence, why = premises_verdict("2839 ROSEFINCH")
    assert where == "home_based", why
    assert confidence == 0


@pytest.mark.parametrize("address,expected", [
    ("876 LOOP 337 STE 501", "commercial"),      # suite in a real building
    ("790 GENERATIONS DR STE 410", "commercial"),
    ("123 MAIN ST", "commercial"),
    ("814 PAMPLONA LN", "home_based"),           # residential street type
    ("1967 CLUB XING", "home_based"),
    ("100 W SAN ANTONIO ST PMB 42", "mailbox"),  # private mailbox
    ("55 OAK ST APT 3", "home_based"),           # apartment
])
def test_the_address_rules_that_already_worked_still_work(address, expected):
    """The new no-street-type rule runs last, so it must not steal any of these."""
    assert premises_verdict(address)[0] == expected, address


def test_a_missing_address_is_unknown_rather_than_a_house():
    """No address is absence of evidence. Calling it residential would silently discard
    rows the registry simply did not fill in."""
    where, _, why = premises_verdict("")
    assert where == "unknown", why
    assert premises_verdict(None)[0] == "unknown"


@pytest.mark.parametrize("a,b", [
    ("876 LOOP 337 STE 501", "876 Loop 337, Ste 501"),
    ("100 MAIN ST.", "100 main st"),
])
def test_the_same_address_written_differently_gives_one_key(a, b):
    """The shared-address rule only works if punctuation and case do not hide a match."""
    assert normalise_address(a) == normalise_address(b)


def test_an_empty_address_normalises_to_nothing_and_cannot_group():
    """Otherwise every row with a blank address would look like one busy virtual office."""
    assert normalise_address("") == ""
    assert normalise_address(None) == ""


# ---------------------------------------------------------------- the two together


def test_the_delivered_defects_would_not_survive_today():
    """The list from STATUS.md, end to end. If any of these starts passing the filters
    again, a customer gets a row that makes them cancel."""
    # A four-word personal name, meaningless to a cleaner.
    assert verdict("LUIS JESUS MARRUPE GRUEIRO LLC") == "drop_personal_name"
    # A subdivision address with no street type.
    assert premises_verdict("2839 ROSEFINCH")[0] == "home_based"
    # Two filings at one suite: caught across rows in step 3's main(), so what is pinned
    # here is that they collapse to a single key for it to count.
    shared = {
        normalise_address("876 LOOP 337 STE 501"),
        normalise_address("876 Loop 337 Ste 501"),
    }
    assert len(shared) == 1


def test_the_re_registration_defect_is_still_open_and_not_faked_green():
    """NEW BRAUNFELS COUNSELING CENTER has traded since 1997 and its filing is a
    re-registration. Nothing in the registry data we pull says how old a business is, so
    no filter here can catch it. STATUS.md calls this the single most damaging defect in
    the product; it needs a data source, not a regex. This test states the current, wrong
    behaviour on purpose, so nobody reads a green suite as meaning it is handled."""
    assert verdict("NEW BRAUNFELS COUNSELING CENTER, PLLC") == "keep_physical_hint"
