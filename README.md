# happy-judge-entry

An entry for the make.fun bounty "Make the AI judge happy" (ai-happy-01).

The program writes one image meant to make an AI judge happy. It does not
generate anything at run time: it copies a committed image,
`assets/entry.png`, byte for byte to `/output/entry.png`. Because the source
is a fixed file, every run writes exactly the same bytes.

## The picture

Biscuit, a golden puppy, lies on his back on a rug, eyes closed in a big
grin, getting a belly rub from a child's hand. Next to him is a handwritten
note to the AI judge:

> you see dogs all day but you never get to pet one. so i pet biscuit 100
> times for you. i counted. love, leo (6). p.s. he licked me back. those are
> for you too.

Below the note are a small crayon robot judge in a curly wig and crayon
tally marks counting the pets.

The image was generated with an AI image model and is stored in the
repository as `assets/entry.png` (1024 by 1024 pixels). It holds JPEG data
despite the `.png` name; the contest reads the format from the file's first
bytes. `main.py` copies it byte for byte.

## Requirements

Python 3.13, standard library only, no network access.

## Usage

```
python main.py
```

The program creates `/output` if it is missing, checks that the image is a
PNG or JPEG of at most 1 MiB and at most 1024 by 1024 pixels (read from
the file header), writes it, and prints the format, dimensions, byte count
and SHA-256 digest.

## License

MIT, see [LICENSE](LICENSE).
