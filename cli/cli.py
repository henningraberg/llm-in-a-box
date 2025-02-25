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
def add_chat(default_model: str, name: str):
    """Add a chat."""
    Chat(default_model=default_model, name=name).save()


@click.command()
def list_chats():
    """List all chats."""
    chats = Chat.get_multiple()
    for chat in chats:
        click.echo(chat.name)


@click.command()
@click.option('--chat_id', type=int, help='ID of chat')
def list_chat_history(chat_id: int):
    """List a chats message history."""
    chat = Chat.get_one(id=chat_id)
    message_history = chat.get_chat_history()

    for message in message_history:
        click.echo(message.to_dict())


@click.command()
@click.option('--content', type=str, help='Message to send to the LLM.')
@click.option('--chat_id', type=int, help='ID of chat.')
@click.pass_context
def chat(ctx, chat_id: int, content: str):
    """List a chats message history."""
    manager = OllamaManager()

    ctx.invoke(list_chat_history, chat_id=chat_id)

    for x in manager.chat(chat_id=chat_id, content=content):
        click.echo(x, nl=False)


@click.command()
@click.option(
    '--model',
    type=str,
    help='Name of the model you want to install (see options at https://ollama.com/library). If you abort the progress will be saved.',
)
def install_model(model: str):
    """Install model."""
    manager = OllamaManager()

    current_progress = 0
    with click.progressbar(length=1000, label=f'Installing model {model}...') as bar:
        for progress in manager.install_model(model=model):
            if progress.completed:
                new_progress = progress.completed
                bar.length = progress.total
            else:
                new_progress = current_progress + 1

            increment = new_progress - current_progress
            bar.update(increment)
            current_progress = new_progress


@click.command()
@click.option(
    '--model',
    type=str,
    help='Name of the model you want to delete.',
)
def remove_model(model: str):
    """Remove model."""
    manager = OllamaManager()
    response = manager.delete_model(model)
    if response.status == 200:
        click.echo(f'✅ {model} was successfully removed!')
    else:
        click.echo(f'❌ {model} was not successfully removed!')


@click.command()
def list_models():
    """List all downloaded models."""
    installed_models = OllamaManager().get_installed_models().models
    for model in installed_models:
        click.echo(model.model)


@click.command()
def nuke_db():
    """Clean the database."""
    clean_db()
    click.echo('✅ Database tables cleared successfully!')


@click.command()
def build_db():
    """Create the database."""
    init_db()
    click.echo('✅ Database tables created successfully!')


# Add commands to the main CLI group
cli.add_command(gui)

cli.add_command(add_chat)
cli.add_command(list_chats)
cli.add_command(list_chat_history)
cli.add_command(chat)

cli.add_command(install_model)
cli.add_command(list_models)
cli.add_command(remove_model)

cli.add_command(nuke_db)
cli.add_command(build_db)
