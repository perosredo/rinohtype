# This file is part of RinohType, the Python document preparation system.
#
# Copyright (c) Brecht Machiels.
#
# Use of this source code is subject to the terms of the GNU Affero General
# Public License v3. See the LICENSE file or http://www.gnu.org/licenses/.


from .flowable import Flowable, GroupedFlowables
from .number import format_number, NUMBER
from .paragraph import Paragraph, ParagraphStyle
from .reference import Referenceable
from .text import SingleStyledText, NoBreakSpace


__all__ = ['Image', 'CaptionStyle', 'Caption', 'Figure']


class Image(Flowable):
    def __init__(self, filename, scale=1.0, style=None):
        super().__init__(style)
        self.filename = filename
        self.scale = scale

    def render(self, container, last_descender, state=None):
        image = container.canvas.document.backend.Image(self.filename)
        left = float(container.width - image.width) / 2
        top = float(container.cursor)
        container.canvas.place_image(image, left, top, scale=self.scale)
        container.advance(float(image.height))


class CaptionStyle(ParagraphStyle):
    attributes = {'numbering_style': NUMBER,
                  'numbering_separator': '.'}

    def __init__(self, base=None, **attributes):
        super().__init__(base=base, **attributes)


class Caption(Paragraph):
    style_class = CaptionStyle

    next_number = {}

    def __init__(self, category, number, text, style=None):
        super().__init__('', style)
        numbering_style = self.get_style('numbering_style')
        numbering_sep = self.get_style('numbering_separator')
        if numbering_style is not None:
            self.ref = format_number(number, numbering_style)
            number = self.ref
        else:
            self.ref = None
            number = ''
        label = category + ' ' + number + numbering_sep
        caption_text = label + NoBreakSpace() + text
        self.append(caption_text)


class Figure(GroupedFlowables, Referenceable):
    def __init__(self, document, filename, caption, scale=1.0, style=None,
                 caption_style=None, id=None):
        number = document.counters.setdefault(self.__class__, 1)
        document.counters[self.__class__] += 1
        image = Image(filename, scale=scale)
        caption = Caption('Figure', number, caption, style=caption_style)
        GroupedFlowables.__init__(self, [image, caption], style)
        Referenceable.__init__(self, document, id)

    def reference(self):
        return str(self.number)

    def title(self):
        return self.caption.text
