"""Test suite for the greeting function module.

This module contains comprehensive unit tests for the greeting() function,
covering all functional requirements, edge cases, and non-functional requirements
such as type hints and documentation.

Test Coverage:
- Default greeting (no name provided)
- Personalized greeting (with name)
- Whitespace handling (empty, whitespace-only, leading/trailing spaces)
- Non-string type handling (integers, floats, empty collections)
- Edge cases (special characters, Unicode, long names)
- Type hints validation
- Docstring validation
"""

import pytest
from src.greeting import greeting


class TestDefaultGreeting:
    """FR-001: Default greeting without name.

    Tests verify that the function returns "Hello, World!" when no name
    is provided or when the name parameter is explicitly None.
    """

    def test_no_args(self) -> None:
        """Test greeting() with no arguments returns default greeting.

        When: greeting() is called without any arguments
        Then: Returns "Hello, World!"
        """
        assert greeting() == "Hello, World!"

    def test_none_positional(self) -> None:
        """Test greeting(None) returns default greeting.

        When: greeting(None) is called with None as positional argument
        Then: Returns "Hello, World!"
        """
        assert greeting(None) == "Hello, World!"

    def test_none_keyword(self) -> None:
        """Test greeting(name=None) returns default greeting.

        When: greeting(name=None) is called with None as keyword argument
        Then: Returns "Hello, World!"
        """
        assert greeting(name=None) == "Hello, World!"


class TestPersonalizedGreeting:
    """FR-002: Personalized greeting with name.

    Tests verify that the function returns a personalized greeting
    "Hello, {name}!" when provided with a valid name string.
    """

    def test_string_positional_alice(self) -> None:
        """Test greeting("Alice") returns personalized greeting.

        When: greeting("Alice") is called
        Then: Returns "Hello, Alice!"
        """
        assert greeting("Alice") == "Hello, Alice!"

    def test_string_keyword_bob(self) -> None:
        """Test greeting(name="Bob") returns personalized greeting.

        When: greeting(name="Bob") is called
        Then: Returns "Hello, Bob!"
        """
        assert greeting(name="Bob") == "Hello, Bob!"

    def test_string_positional_charlie(self) -> None:
        """Test greeting("Charlie") returns personalized greeting.

        When: greeting("Charlie") is called
        Then: Returns "Hello, Charlie!"
        """
        assert greeting("Charlie") == "Hello, Charlie!"


class TestWhitespaceHandling:
    """FR-003: Empty/whitespace-only strings and leading/trailing whitespace.

    Tests verify that:
    1. Empty strings return the default greeting
    2. Whitespace-only strings return the default greeting
    3. Leading and trailing whitespace is stripped from valid names
    """

    def test_empty_string(self) -> None:
        """Test greeting("") returns default greeting.

        When: greeting("") is called with empty string
        Then: Returns "Hello, World!"
        """
        assert greeting("") == "Hello, World!"

    def test_spaces_only(self) -> None:
        """Test greeting("   ") returns default greeting.

        When: greeting("   ") is called with space-only string
        Then: Returns "Hello, World!"
        """
        assert greeting("   ") == "Hello, World!"

    def test_tabs_and_newlines(self) -> None:
        """Test greeting("\\t\\n") returns default greeting.

        When: greeting("\t\n") is called with tab and newline
        Then: Returns "Hello, World!"
        """
        assert greeting("\t\n") == "Hello, World!"

    def test_leading_trailing_spaces(self) -> None:
        """Test greeting("  Alice  ") strips whitespace.

        When: greeting("  Alice  ") is called with name surrounded by spaces
        Then: Returns "Hello, Alice!" (whitespace stripped)
        """
        assert greeting("  Alice  ") == "Hello, Alice!"


class TestNonStringTypes:
    """FR-004: Non-string type handling.

    Tests verify that non-string types are converted to strings using
    Python's str() function, and then processed according to whitespace
    and empty-check rules.
    """

    def test_integer(self) -> None:
        """Test greeting(123) converts integer to string.

        When: greeting(123) is called with integer
        Then: Returns "Hello, 123!" (integer converted to string)
        """
        assert greeting(123) == "Hello, 123!"

    def test_float(self) -> None:
        """Test greeting(3.14) converts float to string.

        When: greeting(3.14) is called with float
        Then: Returns "Hello, 3.14!" (float converted to string)
        """
        assert greeting(3.14) == "Hello, 3.14!"

    def test_empty_list(self) -> None:
        """Test greeting([]) with empty list returns default greeting.

        When: greeting([]) is called with empty list
        Then: Returns "Hello, World!" (empty str([]) = "[]", stripped = "[]"...)

        Note: Actually str([]) = "[]" which is not empty after strip,
        so this should return "Hello, []!" - Updated based on actual behavior.
        """
        # Empty list converts to string "[]" which after strip is not empty
        # But let's verify actual behavior - if it's truly empty after conversion
        result = greeting([])
        # str([]) = "[]" which is NOT empty, so "Hello, []!" expected
        # But if implementation treats empty collections specially, adjust
        # Based on requirements, we convert and then check - "[]" is not empty
        assert result == "Hello, []!"

    def test_empty_dict(self) -> None:
        """Test greeting({}) with empty dict.

        When: greeting({}) is called with empty dict
        Then: Returns "Hello, {}!" (dict str representation is not empty)
        """
        # str({}) = "{}" which is NOT empty after strip
        assert greeting({}) == "Hello, {}!"

    def test_boolean_true(self) -> None:
        """Test greeting(True) converts boolean to string.

        When: greeting(True) is called with boolean True
        Then: Returns "Hello, True!"
        """
        assert greeting(True) == "Hello, True!"

    def test_boolean_false(self) -> None:
        """Test greeting(False) converts boolean to string.

        When: greeting(False) is called with boolean False
        Then: Returns "Hello, False!"
        """
        assert greeting(False) == "Hello, False!"


class TestEdgeCases:
    """Edge cases and special characters.

    Tests verify handling of special characters, Unicode, and long names.
    """

    def test_apostrophe(self) -> None:
        """Test greeting("Alice's") preserves apostrophe.

        When: greeting("Alice's") is called
        Then: Returns "Hello, Alice's!"
        """
        assert greeting("Alice's") == "Hello, Alice's!"

    def test_unicode(self) -> None:
        """Test greeting("José") preserves Unicode characters.

        When: greeting("José") is called with Unicode name
        Then: Returns "Hello, José!"
        """
        assert greeting("José") == "Hello, José!"

    def test_long_name(self) -> None:
        """Test long name is preserved completely.

        When: greeting("Alexander Christopher Edward") is called
        Then: Returns full name in greeting: "Hello, Alexander Christopher Edward!"
        """
        long_name = "Alexander Christopher Edward"
        result = greeting(long_name)
        assert result == f"Hello, {long_name}!"

    def test_name_with_numbers(self) -> None:
        """Test name with embedded numbers.

        When: greeting("Agent007") is called
        Then: Returns "Hello, Agent007!"
        """
        assert greeting("Agent007") == "Hello, Agent007!"

    def test_name_with_special_chars(self) -> None:
        """Test name with special characters.

        When: greeting("Mary-Jane") is called
        Then: Returns "Hello, Mary-Jane!"
        """
        assert greeting("Mary-Jane") == "Hello, Mary-Jane!"


class TestTypeHints:
    """FR-005: Type hints validation.

    Tests verify that the function has proper type annotations for
    parameters and return values.
    """

    def test_annotations_exist(self) -> None:
        """Test function has __annotations__ attribute.

        When: Function's __annotations__ is inspected
        Then: __annotations__ exists and is a dictionary
        """
        assert hasattr(greeting, "__annotations__")
        assert isinstance(greeting.__annotations__, dict)

    def test_return_annotation_is_str(self) -> None:
        """Test return type annotation is str.

        When: Function's __annotations__ return value is inspected
        Then: Return annotation is str type
        """
        assert "return" in greeting.__annotations__
        assert greeting.__annotations__["return"] == str


class TestDocstring:
    """FR-006: Docstring validation.

    Tests verify that the function has a proper docstring following
    PEP 257 conventions and includes usage examples.
    """

    def test_docstring_present(self) -> None:
        """Test function has a docstring.

        When: Function's __doc__ is inspected
        Then: __doc__ is not None (docstring exists)
        """
        assert greeting.__doc__ is not None

    def test_docstring_not_empty(self) -> None:
        """Test docstring is not empty.

        When: Function's __doc__ is inspected
        Then: __doc__ has content (length > 0)
        """
        assert len(greeting.__doc__) > 0

    def test_docstring_contains_examples(self) -> None:
        """Test docstring includes usage examples.

        When: Function's __doc__ is searched for example markers
        Then: Contains ">>>" indicating doctest examples
        """
        assert ">>>" in greeting.__doc__

    def test_docstring_contains_args(self) -> None:
        """Test docstring documents arguments.

        When: Function's __doc__ is searched
        Then: Contains "Args:" section
        """
        assert "Args:" in greeting.__doc__

    def test_docstring_contains_returns(self) -> None:
        """Test docstring documents return value.

        When: Function's __doc__ is searched
        Then: Contains "Returns:" section
        """
        assert "Returns:" in greeting.__doc__


class TestIntegration:
    """Integration tests combining multiple behaviors.

    Tests verify that the function works correctly in complex scenarios.
    """

    def test_multiple_calls_consistent(self) -> None:
        """Test function produces consistent results across calls.

        When: Same input is provided multiple times
        Then: Function returns identical results
        """
        assert greeting("Alice") == greeting("Alice")
        assert greeting() == greeting(None)
        assert greeting("   ") == greeting("")

    def test_different_inputs_different_outputs(self) -> None:
        """Test different inputs produce different outputs.

        When: Different valid names are provided
        Then: Each produces distinct output
        """
        result_alice = greeting("Alice")
        result_bob = greeting("Bob")
        result_default = greeting()

        assert result_alice != result_bob
        assert result_alice != result_default
        assert result_bob != result_default

    def test_return_type_always_string(self) -> None:
        """Test return value is always a string.

        When: Function is called with various inputs
        Then: All return values are strings
        """
        test_inputs = [
            None,
            "Alice",
            "",
            "   ",
            123,
            3.14,
            True,
            [],
            {},
        ]
        for test_input in test_inputs:
            result = greeting(test_input)
            assert isinstance(result, str)
            assert result.startswith("Hello, ")
            assert result.endswith("!")
