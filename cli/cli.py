from typing import Optional

import click
from gui.app import TextualApp
from models.chat import Chat
from integrations.ollama_manager import OllamaManager
from database.clean_db import clean_db
from database.init_db import init_db


@click.group()
def cli():
    pass


@click.command()
def gui():
    """Run the LIAB GUI application."""
    TextualApp().run()


@click.command()
@click.option('--default_model', type=str, help='What downloaded LLM that is going to be used in the chat')
@click.option('--name', type=str, help='Name of the chat')
def add_chat(default_model: str, name: Optional[str] = None):
    """Add a chat."""
    try:
        created_chat = Chat(default_model=default_model, name=name).save()
        click.echo(f'✅ Chat {created_chat.id} was successfully created!')
    except Exception as e:
        click.echo(f'❌ {e}')


@click.command()
@click.option('--chat_id', type=int, help='ID of the chat you want to remove')
def remove_chat(chat_id: int) -> None:
    """Remove a chat."""
    try:
        Chat.get_one(id=chat_id).delete()
        click.echo(f'✅ Chat {chat_id} was successfully removed!')
    except Exception as e:
        click.echo(f'❌ {e}')


@click.command()
def list_chats():
    """List all chats."""
    try:
        chats = Chat.get_multiple()
        for chat in chats:
            click.echo(chat.name)
    except Exception as e:
        click.echo(f'❌ {e}')


@click.command()
@click.option('--chat_id', type=int, help='ID of chat')
def list_chat_history(chat_id: int):
    """List a chats message history."""
    try:
        chat = Chat.get_one(id=chat_id)
        message_history = chat.get_chat_history()

        for message in message_history:
            actor = message.model if message.model else 'You'
            click.echo(actor)
            click.echo('-' * len(actor))
            click.echo(message.content + '\n\n')
    except Exception as e:
        click.echo(f'❌ {e}')


@click.command()
@click.option('--content', type=str, help='Message to send to the LLM.')
@click.option('--chat_id', type=int, help='ID of chat.')
@click.option('--model', type=str, help='Name of model that will answer.')
@click.pass_context
def chat(ctx, chat_id: int, content: str, model: Optional[str] = None):
    """List a chats message history."""
    try:
        manager = OllamaManager()

        ctx.invoke(list_chat_history, chat_id=chat_id)

        chat = Chat.get_one(id=chat_id)

        click.echo('You\n---')
        click.echo(content + '\n\n')

        if not model:
            click.echo(chat.default_model + '\n' + '-' * len(chat.default_model))
        else:
            click.echo(model + '\n' + '-' * len(model))

        for x in manager.chat(chat_id=chat_id, content=content, model=model):
            click.echo(x, nl=False)
        click.echo('\n\n')
    except Exception as e:
        click.echo(f'❌ {e}')


@click.command()
@click.option(
    '--model',
    type=str,
    help='Name of the model you want to download (see options at https://ollama.com/library). If you abort the progress will be saved.',
)
def download_model(model: str):
    """Download LLM model."""
    manager = OllamaManager()

    current_progress = 0
    try:
        with click.progressbar(length=1000, label=f'Downloading model {model}...') as bar:
            for progress in manager.download_model(model=model):
                if progress.completed:
                    new_progress = progress.completed
                    bar.length = progress.total
                else:
                    new_progress = current_progress + 1

                increment = new_progress - current_progress
                bar.update(increment)
                current_progress = new_progress
    except Exception as e:
        click.echo(f'❌ {e}')
        return

    click.echo(f'✅ {model} was successfully downloaded!')


@click.command()
@click.option(
    '--model',
    type=str,
    help='Name of the model you want to delete.',
)
def remove_model(model: str):
    """Remove model."""
    try:
        manager = OllamaManager()
        response = manager.delete_model(model)
        if response.status == 200:
            click.echo(f'✅ {model} was successfully removed!')
        else:
            click.echo(f'❌ {model} was not successfully removed!')
    except Exception as e:
        click.echo(f'❌ {e}')
        return


@click.command()
def list_models():
    """List all downloaded models."""
    try:
        downloaded_models = OllamaManager().get_downloaded_models().models
        for model in downloaded_models:
            click.echo(model.model)
    except Exception as e:
        click.echo(f'❌ {e}')


@click.command()
@click.option('--model', type=str)
def show_model(model: str):
    """Get model information."""
    try:
        response = OllamaManager().get_model_information(model)
        click.echo(response.json)
    except Exception as e:
        click.echo(f'❌ {e}')


@click.command()
def nuke_db():
    """Clean the database."""
    try:
        clean_db()
        click.echo('✅ Database tables cleared successfully!')
    except Exception as e:
        click.echo(f'❌ {e}')


@click.command()
def build_db():
    """Create the database."""
    try:
        init_db()
        click.echo('✅ Database tables created successfully!')
    except Exception as e:
        click.echo(f'❌ {e}')


# Add commands to the main CLI group
cli.add_command(gui)

cli.add_command(add_chat)
cli.add_command(remove_chat)
cli.add_command(list_chats)
cli.add_command(list_chat_history)
cli.add_command(chat)

cli.add_command(download_model)
cli.add_command(list_models)
cli.add_command(remove_model)
cli.add_command(show_model)

cli.add_command(nuke_db)
cli.add_command(build_db)
