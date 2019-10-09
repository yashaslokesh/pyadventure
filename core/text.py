import os

import pygame


def load_font(path, size) -> pygame.font.Font:
    """ Navigates into fonts/ directory, caller must supply path to file from here """
    font = pygame.font.Font(os.path.join("assets", "fonts", path), size)
    return font


class ScrollingText(object):
    """ Create a different ScrollingText object for each new text snippet
    you want to show """

    def __init__(
        self, font, text, color=(255, 255, 255), initial_pos=[50, 400], nl_offset=50
    ):
        """ Form a ScrollingText object

        font        -- should be an already-loaded font that is passed in. Load using pygame.font.Font()
        text        -- the text that should be displayed by this object, currently cannot be changed
        initial_pos -- the initial position text is printed at, chosen to be (50, 600) by default on 800x800 display
        nl_offset   -- 'new line offset', the vertical spacing between consecutive lines of text. Pygame does not
                        handle new lines in text rendering by default
        """
        self.font = font
        self.text = []

        # Initialize with zero, because we check for this in the generator
        self.backspace_count = 0

        # Start off with initial position of (50, 600)
        position = initial_pos
        for substring in text.split("\n"):
            # print(position[1])
            self.text.append((substring.strip(), tuple(position)))
            # Lower position of printing for next substring of text
            position[1] += nl_offset

    def start_scroll(self):
        self.finished_text_generation = False
        self.text_generator = self._generate_text()
        self.update()

    def _generate_text(self):
        """ Generator that creates the self.rendered_text list
        """
        rendered_text = [None] * len(self.text)
        for line_index, line in enumerate(self.text):
            # print(line)
            temp = "|"
            # We turn the words into a list so that we can modify the list in the iterator if
            # needed. That capability is only applicable if we want to use the backspace
            # animation feature
            words = list(line[0])
            for char_index, char in enumerate(words):

                # Remove the cursor character from end of string so string can be modified
                temp = temp[:-1]

                # Process backspace animation
                # All backspace animations are triggered by >{##}, where ## is the number of backspaces
                # The number must be the length of the word you want to delete, not counting the angle bracket
                # and the number inside and the two curly brackets.

                if char == ">":
                    # Get the int for backspace count from the list of chararacters
                    self.backspace_count = int(
                        "".join(words[char_index + 2 : char_index + 4])
                    )
                    # Expand the list by the amount to skip so that the iterator's length is extended
                    # This prevents skipping characters after the backspace command
                    # We remove the angle bracket and the numbers entirely from the list here
                    words[char_index:] = ["+"] * self.backspace_count + words[
                        char_index + 5 :
                    ]

                if self.backspace_count != 0:
                    # If we are still supposed to backspace, then remove the last character
                    temp = temp[:-1]
                    self.backspace_count -= 1
                else:
                    # Else, we will just add the next character
                    temp += char

                # Add cursor animation if we are not at the end, yet
                if char_index != len(words) - 1:
                    temp += "|"
                # Skip spaces
                if char != " ":  # White font
                    font_render = self.font.render(temp, True, (255, 255, 255))
                    rendered_text[line_index] = (font_render, line[1])
                    yield rendered_text

    def update(self):
        """ Updates the self.rendered_text list of tuples of text & position """
        if not self.finished_text_generation:
            try:
                self.rendered_text = next(self.text_generator)
            except StopIteration:
                self.finished_text_generation = True

    def draw(self, screen: pygame.surface.Surface):
        """ Draws all text from the self.rendered_text list. Each entry in this list
        is a tuple with a rendered string first followed by its position. The rendered
        string is a surface, so we draw it onto the screen, our main surface. """

        for line in self.rendered_text:
            if line != None:
                screen.blit(line[0], line[1])
