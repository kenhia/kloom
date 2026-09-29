The first Colossus proved itself in February 1944, and Bletchley at once
wanted more, and better. Four of an improved design were ordered in March,
twelve by the end of April, and the Post Office engineers at Dollis Hill were
told to have the first working by 1 June. The invasion of France was coming,
and Tunny carried the German High Command's own view of it.

## The Mark 2

The first **Mark 2 Colossus** went to work at Bletchley at eight in the
morning of 1 June 1944, five days before the landings in Normandy. **Allen
Coombs** led its production. It had about 2,400 valves by Wikipedia's count;
GCHQ and the National Museum of Computing give about 2,500 for Colossus.
It read its tape as fast as the first machine did, 5,000 characters a
second, and yet it did the work five times faster.

The trick was to read each character once and use it five times. Flowers's
design held the last few characters from the tape in what would now be called
a _shift register_, a chain of stores through which each character moved one
place at every sprocket hole. Five processing units, each able to evaluate a
Boolean condition and count the result, took their input from different
places along the chain, so on one pass of the tape they tested five different
starting positions of a wheel at once. The plate draws that data path: the
tape, the register, the ring of stores standing in for the chi wheel, and
five processors, each with its counter.

![Bar chart of letters examined per second: Heath Robinson 2,000 at best, the Mark 1 Colossus 5,000, and the Mark 2 an effective 25,000](reading-speed.svg)

| Machine              | Letters examined per second            |
| -------------------- | -------------------------------------- |
| Heath Robinson, 1943 | 1,000 to 2,000                         |
| Colossus Mark 1      | 5,000                                  |
| Colossus Mark 2      | 5,000 read; an effective 25,000 tested |

For Tutte's first test, setting the first two chi wheels, that cut the passes
of the tape from 1,271 to 255, and a run of about eight minutes on an average
message to under two. The _General Report on Tunny_ calls the second machine
"the prototype of all later Colossi": it had quintuple testing from the first,
two tape frames so that one tape could be loaded while another ran, and
_spanning_, which confined a count to part of a tape and was soon found
indispensable. Most runs still went as the cryptanalyst on duty decided, but
Newman and then **Jack Good** and **Donald Michie** wrote decision trees that
let the Wren operators choose the next run themselves.

## What the decrypts said

What Colossus contributed to D-Day is told in more than one register. **Tony
Sale**, who later rebuilt one, wrote that the decrypts showed Hitler had
swallowed the Allies' deception, the phantom army in the south of England,
was convinced the attack would come across the Pas de Calais, and was
keeping Panzer divisions in Belgium.
GCHQ's own account is more careful: planning for D-Day was well advanced by
the time Colossus arrived, and it was one of the machines that helped show
Hitler had been convinced the invasion would come by the Pas de Calais.
**Tommy Flowers**, in his telling, went further: a note summarising a Colossus
decrypt was handed to Eisenhower at a staff meeting on 5 June, confirming that
Hitler wanted no more troops moved to Normandy, and Eisenhower said "We go
tomorrow"; an earlier decrypt of a report by Rommel, he said, moved an
American parachute drop away from a German tank division. Those are his
recollections, told long after the war, and they are the least certain of the
three accounts.

After the landings, the Resistance and Allied aircraft cut the German land
lines in northern France, and more traffic went by radio, in Sale's account,
so there was more for Bletchley to read. Colossi came from Dollis Hill at
about one a month.

![A wartime photograph of Colossus 10 in Block H at Bletchley Park: tall racks of valves and switch panels on the left, a sloping operator's panel and typewriter stand in the middle, and on the right the long bedstead of pulleys that took tapes of up to 30,000 characters](colossus-10.png)

## Ten Colossi and a report

By the German surrender in May 1945 there were ten Colossi at Bletchley and
an eleventh being assembled: seven for setting wheels and three for breaking
them. The first had been rebuilt as a Mark 2. Max Newman's section had grown
to 26 cryptographers, 28 engineers and 273 Wrens, with three Robinsons and
three Tunny machines beside the Colossi, and the report records 358 messages set on
their chi wheels in the single week ending 31 March. By Sale's figures and the museum's, 63 million characters of
German high-command traffic were decrypted by about 550 people.

In 1945 three of the Newmanry, **Jack Good**, **Donald Michie** and
**Geoffrey Timms**, wrote its history, the _General Report on Tunny_. It
covers the cipher, the statistics, the machines and the organisation, in a
voice not usually found in a secret report: it regrets that it cannot convey
"the fantastic speed of thin paper tape round the glittering pulleys". It was
kept secret for fifty-five years. What happened to the machines, and to the
people who had built them, in that time is the next frame.
