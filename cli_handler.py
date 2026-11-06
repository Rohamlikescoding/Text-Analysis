import click
from user_input_utils import handle_user_input
from file_handling_utils import read_file
from text_analysis_utils import calculate
from text_analysis_utils import text_transform



@click.command()
@click.option('--top-words', default=5, help='number of most frequent words')
@click.argument("file", default="default.txt")
@click.option("--uppercase", is_flag=True ,help='use uppercase')
@click.option("--lowercase", is_flag=True ,help='use lowercase')
@click.option("--capitalize", is_flag=True ,help='use capitalize')
@click.option("--clean-punctuation", is_flag=True ,help='clean punctuation')
@click.option("--stats", is_flag=True ,help='receive stats')


def cli(stats,top_words, file, uppercase, lowercase, capitalize, clean_punctuation):
    """Text analysis tool.

       FILE is the path to the file to be analyzed (default: default.txt).
    """

    ctx = click.get_current_context()
    top_words_provided = (
            ctx.get_parameter_source("top_words")
            == click.core.ParameterSource.COMMANDLINE
    )

    is_value =  uppercase or lowercase or capitalize or clean_punctuation or stats
    if file == "default.txt" and top_words==5  and not is_value:
        result =handle_user_input()
    else:
        text=text_transform(read_file(file), uppercase, lowercase, capitalize, clean_punctuation)
        if stats:
            result =calculate(text,top_words)
        elif top_words_provided:
            result = {"stats":calculate(text,top_words)['top_word_frequency']}
            print(result)
        else:
            result = {"text:": text}

    for key, value in result.items():
        click.echo(click.style(key, fg="cyan", bold=True))
        click.echo(click.style(str(value), fg="white"))


