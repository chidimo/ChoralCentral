"""
Lorem Pysum: Name, email, title, sentence and paragraph generator
"""

from __future__ import unicode_literals
from random import randint, choice, sample, shuffle

class LoremPysum(object):
    """Generate random sentences and paragraphs
    
    parameters
    *args : any number of text files, optional
    """
    
    def __init__(self, *args, lorem=True):
        """Docstring"""
        self.lorem_ipsum = [
            'exercitationem', 'perferendis', 'perspiciatis', 'laborum', 'eveniet', 
            'sunt', 'iure', 'nam', 'nobis', 'eum', 'cum', 'officiis', 'excepturi',
            'odio', 'consectetur', 'quasi', 'aut', 'quisquam', 'vel', 'eligendi',
            'itaque', 'non', 'odit', 'tempore', 'quaerat', 'dignissimos',
            'facilis', 'neque', 'nihil', 'expedita', 'vitae', 'vero', 'ipsum',
            'nisi', 'animi', 'cumque', 'pariatur', 'velit', 'modi', 'natus',
            'iusto', 'eaque', 'sequi', 'illo', 'sed', 'ex', 'et', 'voluptatibus',
            'tempora', 'veritatis', 'ratione', 'assumenda', 'incidunt', 'nostrum',
            'placeat', 'aliquid', 'fuga', 'provident', 'praesentium', 'rem',
            'necessitatibus', 'suscipit', 'adipisci', 'quidem', 'possimus',
            'voluptas', 'debitis', 'sint', 'accusantium', 'unde', 'sapiente',
            'voluptate', 'qui', 'aspernatur', 'laudantium', 'soluta', 'amet',
            'quo', 'aliquam', 'saepe', 'culpa', 'libero', 'ipsa', 'dicta',
            'reiciendis', 'nesciunt', 'doloribus', 'autem', 'impedit', 'minima',
            'maiores', 'repudiandae', 'ipsam', 'obcaecati', 'ullam', 'enim',
            'totam', 'delectus', 'ducimus', 'quis', 'voluptates', 'dolores',
            'molestiae', 'harum', 'dolorem', 'quia', 'voluptatem', 'molestias',
            'magni', 'distinctio', 'omnis', 'illum', 'dolorum', 'voluptatum', 'ea',
            'quas', 'quam', 'corporis', 'quae', 'blanditiis', 'atque', 'deserunt',
            'laboriosam', 'earum', 'consequuntur', 'hic', 'cupiditate',
            'quibusdam', 'accusamus', 'ut', 'rerum', 'error', 'minus', 'eius',
            'ab', 'ad', 'nemo', 'fugit', 'officia', 'at', 'in', 'id', 'quos',
            'reprehenderit', 'numquam', 'iste', 'fugiat', 'sit', 'inventore',
            'beatae', 'repellendus', 'magnam', 'recusandae', 'quod', 'explicabo',
            'doloremque', 'aperiam', 'consequatur', 'asperiores', 'commodi',
            'optio', 'dolor', 'labore', 'temporibus', 'repellat', 'veniam',
            'architecto', 'est', 'esse', 'mollitia', 'nulla', 'a', 'similique',
            'eos', 'alias', 'dolore', 'tenetur', 'deleniti', 'porro', 'facere',
            'maxime', 'corrupti',]

        if args and lorem:
            self.words = self.lorem_ipsum
        elif args and (not lorem):
            self.words = []
        elif (not args) and lorem:
            self.words = self.lorem_ipsum
        if args:
            for file in args:
                with open(file, 'r+') as fhand:
                    text = fhand.read().split()
                new_words = (word.strip().lower() for word in text)
                self.words.extend(new_words)
                
            shuffle(self.words)
            self.words = (self.words)
            length = len(self.words)//3 # pick the first third of words to make common
            self.common = self.words[:length]
            self.standard = ' '.join(self.common)
        else:
            self.common = ('lorem', 'ipsum', 'dolor', 'sit', 'amet',
                        'consectetur', 'adipisicing', 'elit', 'sed',
                        'do', 'eiusmod', 'tempor', 'incididunt', 'ut',
                        'labore', 'et', 'dolore', 'magna', 'aliqua',)

            self.standard = ('Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod '
                            'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim '
                            'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea '
                            'commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '
                            'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint '
                            'occaecat cupidatat non proident, sunt in culpa qui officia deserunt '
                            'mollit anim id est laborum.')

    def title(self):
        """return a title consisting of between 2 to 6 words"""
        wordings = [(choice(self.words)).title() for i in range(randint(2, 6))]
        return ' '.join(list(wordings)).title()
        
    def word(self):
        """Return a single word"""
        return choice(self.words)
        
    def name(self):
        """Return any name with a middle initial."""
        initial = choice(self.words).upper()[0]
        return ("{} {}. {}".format(self.word(), initial, self.word())).title()
        
    def username(self):
        return "{}{}{}".format(choice(self.words), randint(1, 10), choice(self.words))

    def email(self):
        """Return an email address"""
        fpart = choice(self.words)
        lastpart = choice(self.words)
        ending = choice(['com', 'info', 'org', 'net'])
        return "{}@{}.{}".format(fpart, lastpart, ending)

    def sentence(self):
        """
        Return a sentence

        Notes
        The first word is capitalized, and the sentence ends in either a period or
        question mark. Commas are added at random.
        Determine the number of commaseparated sections and number of words in
        each section for this sentence.
        """
        sections = [' '.join(sample(self.words, randint(3, 12))) for i in range(randint(1, 5))]
        s = ', '.join(sections)
        # Convert to sentence case and add end punctuation.
        return "{}{}{}".format(s[0].upper(), s[1:], choice('?.'))
        
    def sentences(self, count=1):
        return "\n\n".join([self.sentence() for _ in range(count)])

    def paragraphs(self, count=1, common=True):
        """
        Return paragraphs

        Parameters
        count : int
            The number of required paragraph. Default is 1
        common : bool
            Whether the first paragraph will be the standard lorem ipsum text. Default is True
        """
        if count == 1:
            paragraph = ' '.join([self.sentence() for i in range(randint(3, 4))])
            return paragraph
        paragraphs = []

        if common:
            paragraphs.append(self.standard)
        else:
            paragraph = ' '.join([self.sentence() for i in range(randint(3, 4))])
            paragraphs.append(paragraph)

        for i in range(1, count):
            paragraph = ' '.join([self.sentence() for i in range(randint(3, 4))])
            paragraphs.append(paragraph)
        return "\n\n".join(paragraphs)
