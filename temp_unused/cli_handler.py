import click

from file_handling_utils import read_file
from text_analysis_utils import calculate, handle_summary,text_transform
from user_input_utils import handle_user_input


@click.command()
@click.argument("filename", default=None, required=False ,type=click.Path(exists=True, dir_okay=False))
@click.option('--top-words', default=5, help='number of most frequent words' , type=click.IntRange(min=1))
@click.option("--uppercase", is_flag=True ,help='use uppercase')
@click.option("--lowercase", is_flag=True ,help='use lowercase')
@click.option("--capitalize", is_flag=True ,help='use capitalize')
@click.option("--clean-punctuation", is_flag=True ,help='clean punctuation')
@click.option("--stats", is_flag=True ,help='receive stats')
@click.option("--summary", is_flag=True ,help='receive summary')


def cli(stats,top_words, filename, uppercase, lowercase, capitalize, clean_punctuation, summary):
    """Text analysis tool.

       Enter the path to the file to be analyzed like the line below.

       python main.py {From/where/fileurl.txt} --stats
    """

    ctx = click.get_current_context()
    top_words_provided = (
            ctx.get_parameter_source("top_words")
            == click.core.ParameterSource.COMMANDLINE
    )

    is_value =  uppercase or lowercase or capitalize or clean_punctuation or stats or summary or top_words_provided


    if not filename and not is_value:
        result =handle_user_input()
    elif not filename and is_value:
        click.secho("you can not use cli commands without a file!", fg="red")
        return
    else:
        try:
            text =read_file(filename)

            if stats:
                result = calculate(text,top_words)
            elif summary:
                result = handle_summary(text)
            elif top_words_provided:
                result = {"stats":calculate(text,top_words)['top_word_frequency']}
            else:
                text =text_transform( text,uppercase, lowercase, capitalize,clean_punctuation)
                result = {"text": text}
        except (OSError, UnicodeDecodeError) as e:
                click.secho(f"Can't read {filename}: {e}", fg="red", err=True)
                ctx.exit(1)

    for key, value in result.items():
        click.secho(key, fg="cyan", bold=True)
        click.secho(str(value), fg="white")

