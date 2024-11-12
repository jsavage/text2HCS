# text2HCS
Drawing a Hierarchical Control Structure from constrained text.
![image](https://github.com/user-attachments/assets/13f7a290-102f-43d1-8b4f-ad6b5510cb1e)
![image](https://github.com/user-attachments/assets/681cf206-da9a-4f04-9536-d99033d16a87)

![image](https://github.com/user-attachments/assets/ef5a9e4f-19c3-4296-afd3-c084e08d4ed0)


Entities Parsing:

Entities are recognized as text before the first colon (:). Multiple entities on the same line are separated by spaces.
Hyphenated words without spaces (e.g., warm-food) are treated as single entities.

Actions Parsing:

Text after a colon (:) is interpreted as Actions and are associated with the first two entities mentioned before the colon. text after a second colon is interpreted as Actions associated with the second two entities mentioned before the colon.

Feedback Parsing:

Feedback is recognized as text following a slash (/) and is associated with the entities in reverse order.
Nested Entities Handling:

Entities enclosed in square brackets ([ and ]) are nested within the entity preceding the bracket.

To Do:

Entity Alignment:

Top to Bottom flow to represent how higher-level Entities control lower-level entities

Left to Right flow may be enabled by prefixing a descriptive line with a hyphen resulting in entities being aligned horizontally.
