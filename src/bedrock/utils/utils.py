import json
from typing import Iterable, Mapping, Literal


def numeric(value: str) -> float:
    """
    Converts a string into an integer or if that fails into a floating
    point.

    The major reason to use this instead of :external+python:class:`float`
    is for usage within game commands such as ``teleport`` where an integer
    coordinate like ``42`` is parsed as ``42.50`` whereas floating points
    are interpreted as is so that ``21.0`` means ``21.0``. You may override
    this behaviour by overriding this function which affects the parsing of
    :meth:`WorldCoordinate.from_string` and :meth:`LocalCoordinate.from_string`:

    Parameters
    ----------
    value
        The string to converr into a numeric.

    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError as e:
            raise e from None


def rawtext(
        text: str | Iterable[
                        Mapping[Literal["text", "selector", "translate"], str]
                  | Mapping[Literal["score"], Mapping[Literal["name", "objective"], str]]
                  ]
) -> str:
    """
    Wraps text inside a rawtext JSON object which can be used for
    ``/tellraw``, ``/titleraw`` etc.

    .. seealso:: https://wiki.bedrock.dev/commands/tellraw.html

    Parameters
    ----------
    text
        Either just a string or an iterable of mappings beeing
        valid rawtext parts.

    Examples
    --------

     code-block:: python
        >>> rawtext('Hello World')
        '{"rawtext": [{"text": "Hello World"}]}'
        >>> rawtext([{'text': 'Hello '}, {'selector': '@p[r=10]'}])
        '{"rawtext": [{"text": "Hello "}, {"selectors": "@p[r=10]}]}'

    """
    if isinstance(text, str):
        return json.dumps({"rawtext": [{"text": text}]})
    return json.dumps({"rawtext": text})
