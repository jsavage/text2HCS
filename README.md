# text2HCS
Drawing a Hierarchical Control Structure from constrained text.

Entities Parsing:

Entities are recognized as text before a colon (:). Multiple entities on the same line are separated by spaces.
Hyphenated words without spaces (e.g., warm-food) are treated as single entities.

Actions Parsing:

Actions are recognized as text after a colon (:) and are associated with the entities mentioned before the colon.
Feedback Parsing:

Feedback is recognized as text following a slash (/) and is associated with the entities in reverse order.
Nested Entities Handling:

Entities enclosed in square brackets ([ and ]) are nested within the entity preceding the bracket.
Entity Alignment:

Entities following a hyphen (-) with spaces on both sides are aligned horizontally.
